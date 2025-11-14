import pandas as pd
from k_link.db.core import ObjectId
from k_link.db.daos import LinkServicesDAO
from k_link.db.models import LinkServices
from k_link.extensions.conciliation_type import ConciliationType
from k_link.extensions.pipeline import (
    DataFrameConfig,
    DataFrameSource,
    JsonSource,
    PipelineFileOperation,
    PipelineJsonOperation,
    PipelineOperation,
)
from k_link.extensions.report_config import HeaderConfig
from loggerk import LoggerK

from conciliaciones.clients.external.pipeline.pipeline_configuration import (
    PipelineConfiguration,
)
from conciliaciones.utils.redis.redis_keys import RedisKeys
from conciliaciones.utils.redis.redis_storage import RedisStorage


class PipelineManager:
    def __init__(
        self,
        run_id: str,
        project_id: ObjectId,
        month: int,
        year: int,
        name_df: str,
        conciliation_type: ConciliationType,
        data_frame_source: DataFrameSource,
        data: pd.DataFrame | dict,
    ) -> None:
        self._logger = LoggerK(self.__class__.__name__)
        self._project_id: ObjectId = project_id
        self._name_df: str = name_df
        self._data: pd.DataFrame | dict = data
        self._data_frame_source: DataFrameSource = data_frame_source
        self._year: int = year
        self._month: int = month

        self._link_services_dao = LinkServicesDAO()
        self.redis = RedisStorage()
        self._redis_key = RedisKeys(
            run_id=run_id,
            project_id_str=str(project_id),
            month=month,
            year=year,
            conciliation_type=conciliation_type,
        )

    async def get_configuration_pipeline(
        self, datasources_optional: list[str]
    ) -> tuple[pd.DataFrame, HeaderConfig]:
        link_services: LinkServices | None = await self._link_services_dao.get(
            project_id=self._project_id
        )

        if link_services is None:
            raise ValueError(
                f"No se encontraron servicios de enlace para el proyecto {self._project_id}"
            )

        data_frames_config: list[DataFrameConfig] = link_services.data_frames_config

        data_frame_config: DataFrameConfig | None = next(
            (
                df_config
                for df_config in data_frames_config
                if df_config.name == self._name_df
            ),
            None,
        )

        if data_frame_config is None:
            raise ValueError(
                f"No se encontró la configuración del DataFrame {self._name_df}"
            )

        if isinstance(self._data, dict):
            self._data = pd.DataFrame(self._data)

        pipelines_data_df: list[tuple[str, pd.DataFrame]] = []
        for pipeline in data_frame_config.pipeline:
            if isinstance(pipeline, PipelineFileOperation):
                if pipeline.df_base in datasources_optional:
                    continue

            pipeline_data_df, base_name = await self._get_redis_df_pipeline(
                pipeline=pipeline,
            )
            if pipeline_data_df is None:
                continue

            pipelines_data_df.append((base_name, pipeline_data_df))

        pipeline_configuration = PipelineConfiguration(
            data_frame_config=data_frame_config,
            data=self._data,
            pipeline_data_df=pipelines_data_df,
            datasources_optional=datasources_optional,
            year=self._year,
            month=self._month,
            redis_key=self._redis_key,
        )

        return await pipeline_configuration.apply_configuration_pipeline()

    async def _get_redis_df_pipeline(
        self, pipeline: PipelineOperation
    ) -> tuple[pd.DataFrame, str]:
        redis_key: str | None = None
        base_name: str | None = None

        if self._data_frame_source == DataFrameSource.FILE:
            if not isinstance(pipeline, PipelineFileOperation):
                raise ValueError(
                    f"Pipeline {pipeline} no es del tipo PipelineFileOperation"
                )

            redis_key = self._redis_key.get_erp_data_source_redis_key(pipeline.df_base)
            base_name = pipeline.df_base
        elif self._data_frame_source == DataFrameSource.JSON:
            if not isinstance(pipeline, PipelineJsonOperation):
                raise ValueError(
                    f"Pipeline {pipeline} no es del tipo PipelineJsonOperation"
                )

            json_source: JsonSource = pipeline.json_source

            match json_source:
                case JsonSource.ERP_SAT:
                    redis_key = self._redis_key.get_sat_erp_redis_key()
                    base_name = JsonSource.ERP_SAT.value
                case JsonSource.SAT_NO_ERP:
                    redis_key = self._redis_key.get_sat_no_erp_periodo_key()
                    base_name = JsonSource.SAT_NO_ERP.value
                case JsonSource.META_CANCELADA:
                    redis_key = self._redis_key.get_sat_erp_meta_cancel_key()
                    base_name = JsonSource.META_CANCELADA.value
                case JsonSource.META_PENDIENTE:
                    redis_key = self._redis_key.get_sat_erp_meta_key()
                    base_name = JsonSource.META_PENDIENTE.value
                case JsonSource.SHEETS:
                    if not pipeline.fuction_name:
                        raise ValueError(
                            "El campo 'fuction_name' es requerido cuando 'json_source' es 'sheets'"
                        )

                    function_name: str = pipeline.fuction_name
                    redis_key = self._redis_key.get_sat_sheets_key(function_name)
                    base_name = JsonSource.SHEETS.value
                case JsonSource.GROUP_BY:
                    if not pipeline.fuction_name:
                        raise ValueError(
                            "El campo 'fuction_name' es requerido cuando 'json_source' es 'sheets'"
                        )

                    function_name: str = pipeline.fuction_name
                    redis_key = self._redis_key.get_dataframe_group_redis_key(
                        function_name
                    )
                    base_name = JsonSource.GROUP_BY.value
                case JsonSource.PIVOT_TABLE:
                    if not pipeline.fuction_name:
                        raise ValueError(
                            "El campo 'fuction_name' es requerido cuando 'json_source' es 'sheets'"
                        )

                    function_name: str = pipeline.fuction_name
                    redis_key = self._redis_key.get_dataframe_pivot_redis_key(
                        function_name
                    )
                    base_name = JsonSource.PIVOT_TABLE.value
                case JsonSource.CATALOGS:
                    if not pipeline.fuction_name:
                        raise ValueError(
                            "El campo 'fuction_name' es requerido cuando 'json_source' es 'catalogs'"
                        )
                    function_name: str = pipeline.fuction_name
                    redis_key = self._redis_key.get_erp_data_source_redis_key(
                        function_name
                    )
                    base_name = JsonSource.CATALOGS.value
                case _:
                    raise ValueError(f"Tipo de fuente JSON no soportado: {json_source}")

        if redis_key is None:
            raise ValueError(
                f"No se pudo determinar la clave de Redis para el pipeline {pipeline}"
            )

        pipeline_df: pd.DataFrame | None = self.redis.get_df(redis_key=redis_key)

        if pipeline_df is None:
            raise ValueError(f"No se encontró el DataFrame en Redis {redis_key}")

        if base_name is None:
            raise ValueError(
                f"No se pudo determinar el nombre base para el pipeline {pipeline}"
            )

        return pipeline_df, base_name
