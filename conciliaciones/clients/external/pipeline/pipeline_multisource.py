import io

import pandas as pd
from k_link.db.core import ObjectId
from k_link.db.daos import LinkServicesDAO
from k_link.db.models import LinkServices
from k_link.extensions.conciliation_type import ConciliationType
from k_link.extensions.pipeline import (
    DataFrameConfig,
    DataFrameSource,
    JsonSource,
    JsonSourceConfig,
)
from k_link.extensions.report_config import HeaderConfig
from loggerk import LoggerK

from conciliaciones.clients.external.pipeline.pipeline_manager import PipelineManager
from conciliaciones.utils.completion_handler.airflow_contex_exception import (
    AirflowContexException,
)
from conciliaciones.utils.headers.headers_types import HeadersTypes
from conciliaciones.utils.redis.redis_keys import RedisKeys
from conciliaciones.utils.redis.redis_storage import RedisStorage


class PipelineMultisource:
    def __init__(
        self,
        run_id: str,
        project_id_str: str,
        year: int,
        month: int,
        conciliation_type: ConciliationType,
        data_frame_source: DataFrameSource,
        data_sources_optional: list[str],
    ) -> None:
        self._logger = LoggerK(self.__class__.__name__)
        self._run_id: str = run_id

        self._project_id_str: str = project_id_str
        self._year: int = year
        self._month: int = month
        self._conciliation_type: ConciliationType = conciliation_type
        self._data_frame_source: DataFrameSource = data_frame_source
        self._data_sources_optional: list[str] = data_sources_optional

        self._link_services_dao = LinkServicesDAO()
        self.redis = RedisStorage()
        self.redis_keys = RedisKeys(
            run_id=self._run_id,
            project_id_str=self._project_id_str,
            month=self._month,
            year=self._year,
            conciliation_type=self._conciliation_type,
        )
        self._header_types = HeadersTypes(
            run_id=self._run_id,
            project_id_str=self._project_id_str,
            month=self._month,
            year=self._year,
            conciliation_type=self._conciliation_type,
        )
        self._airflow_fail_exception = AirflowContexException(
            year=self._year,
            month=self._month,
            project_id=self._project_id_str,
            run_id=self._run_id,
            conciliation_type=self._conciliation_type,
        )

        self._is_final_file: bool = False

    async def run_pipeline(self) -> None:
        link_services: LinkServices | None = await self._link_services_dao.get(
            project_id=ObjectId(self._project_id_str)
        )

        if link_services is None:
            self._airflow_fail_exception.handle_and_store_exception(
                f"No se encontro configuración de LinkServices para el proyecto: {self._project_id_str}"
            )

        data_frames_config: list[DataFrameConfig] = link_services.data_frames_config

        if not data_frames_config:
            return

        self._logger.info(f"Fuente ejecutada: {self._data_frame_source.value}")
        if self._data_frame_source == DataFrameSource.FILE:
            await self._get_configuration_from_file(data_frames_config)
        elif self._data_frame_source == DataFrameSource.JSON:
            await self._get_configuration_from_json(data_frames_config)
        else:
            self._airflow_fail_exception.handle_and_store_exception(
                f"Tipo de DataFrameConfig {self._data_frame_source} no soportado para el proyecto: {self._project_id_str}"
            )

    async def _get_configuration_from_file(
        self, data_frame_config: list[DataFrameConfig]
    ) -> None:
        self._logger.info(f"Data Sources optional: {self._data_sources_optional}")

        data_frame_base = [
            df_config
            for df_config in data_frame_config
            if df_config.source == DataFrameSource.FILE
        ]

        total: int = len(data_frame_base)
        for idx, df_info in enumerate(data_frame_base):
            self._logger.error(f"Data Frame: {df_info.name} de tipo {df_info.source}")

            # Si es el último elemento, marcar como archivo final
            if idx == total - 1:
                self._is_final_file = True

                self._logger.error(
                    f"Último DataFrame: {df_info.name} marcado como archivo final"
                )

            self._logger.info(
                f"Procesando DataFrame {idx + 1} de {total}: {df_info.name} - {df_info.source}"
            )

            await self._get_configuration_pipeline(data_frame_base=df_info)

    async def _get_configuration_from_json(
        self, data_frame_config: list[DataFrameConfig]
    ) -> None:
        data_frame_base: list[DataFrameConfig] = [
            df_config
            for df_config in data_frame_config
            if df_config.source == DataFrameSource.JSON
        ]

        for df_info in data_frame_base:
            await self._get_configuration_pipeline(data_frame_base=df_info)

    async def _get_configuration_pipeline(
        self, data_frame_base: DataFrameConfig
    ) -> None:
        self._logger.info(f"DataFrame Config: {data_frame_base}")
        self._logger.info(f"Data Source Base Name: {data_frame_base.name}")
        self._logger.info(f"Operaciones: {data_frame_base.pipeline}")

        df_base, redis_key = await self._get_data_redis(data_frame_base=data_frame_base)

        pipeline_manager = PipelineManager(
            run_id=self._run_id,
            project_id=ObjectId(self._project_id_str),
            month=self._month,
            year=self._year,
            name_df=data_frame_base.name,
            data=df_base,
            conciliation_type=self._conciliation_type,
            data_frame_source=self._data_frame_source,
        )

        df_base, _ = await pipeline_manager.get_configuration_pipeline(
            datasources_optional=self._data_sources_optional
        )

        if self._data_frame_source == DataFrameSource.FILE and self._is_final_file:
            headers_erp_final: list[HeaderConfig] = self._get_list_erp_final(
                df_erp=df_base
            )

            # Se guarda lista erp_final headers
            await self._header_types.save_redis_headers_list(
                redis_key=self.redis_keys.get_headers_erp_final_list_key(),
                headers_list=headers_erp_final,
            )

        await self._save_data_redis(
            df=df_base,
            redis_key=redis_key,
        )

    async def _get_data_redis(
        self, data_frame_base: DataFrameConfig
    ) -> tuple[pd.DataFrame, str]:
        source: DataFrameSource = data_frame_base.source
        source_config = data_frame_base.source_config
        sheet_config = None

        redis_key = None
        if source == DataFrameSource.FILE:
            redis_key = self.redis_keys.get_erp_data_source_redis_key(
                data_frame_base.name
            )
        elif source == DataFrameSource.JSON:
            if not isinstance(source_config, JsonSourceConfig):
                self._airflow_fail_exception.handle_and_store_exception(
                    f"La configuración de la fuente para JSON debe ser de tipo JsonSourceConfig, se recibió {type(source_config)} para eñ proyecto {self._project_id_str}"
                )

            json_source: JsonSource = source_config.json_source

            match json_source:
                case JsonSource.ERP_SAT:
                    redis_key = self.redis_keys.get_sat_erp_redis_key()
                case JsonSource.SAT_NO_ERP:
                    redis_key = self.redis_keys.get_sat_no_erp_periodo_key()
                case JsonSource.META_CANCELADA:
                    redis_key = self.redis_keys.get_sat_erp_meta_cancel_key()
                case JsonSource.META_PENDIENTE:
                    redis_key = self.redis_keys.get_sat_erp_meta_key()
                case JsonSource.SHEETS:
                    sheet_config = source_config.sheet_config
                    if not sheet_config:
                        self._airflow_fail_exception.handle_and_store_exception(
                            f"Se requiere la configuración de sheet para la fuente JSON de tipo {JsonSource.SHEETS.value}"
                        )

                    redis_key = self.redis_keys.get_sat_sheets_key(funcion=sheet_config)
                case JsonSource.GROUP_BY:
                    sheet_config = source_config.sheet_config
                    if not sheet_config:
                        self._airflow_fail_exception.handle_and_store_exception(
                            f"Se requiere la configuración de sheet para la fuente JSON de tipo {JsonSource.GROUP_BY.value}"
                        )

                    redis_key = self.redis_keys.get_dataframe_group_redis_key(
                        sheet_config
                    )
                case JsonSource.PIVOT_TABLE:
                    sheet_config = source_config.sheet_config
                    if not sheet_config:
                        self._airflow_fail_exception.handle_and_store_exception(
                            f"Se requiere la configuración de sheet para la fuente JSON de tipo {JsonSource.PIVOT_TABLE.value}"
                        )

                    redis_key = self.redis_keys.get_dataframe_pivot_redis_key(
                        sheet_config
                    )
                case JsonSource.CATALOGS:
                    sheet_config = source_config.sheet_config
                    if not sheet_config:
                        self._airflow_fail_exception.handle_and_store_exception(
                            f"Se requiere la configuración de sheet para la fuente JSON de tipo {JsonSource.CATALOGS.value}"
                        )

                    redis_key = self.redis_keys.get_erp_data_source_redis_key(
                        sheet_config
                    )
                case _:
                    self._airflow_fail_exception.handle_and_store_exception(
                        f"Tipo de fuente JSON no soportado: {json_source}"
                    )

        if redis_key is None:
            self._airflow_fail_exception.handle_and_store_exception(
                f"No se encontró la clave de Redis para el source {source} y configuración {sheet_config}"
            )

        df_base: pd.DataFrame | None = self.redis.get_df(redis_key=redis_key)
        if df_base is None:
            self._airflow_fail_exception.handle_and_store_exception(
                f"No se encontró DataFrame en Redis con la clave {redis_key} par el proyecto: {self._project_id_str}"
            )
        return df_base, redis_key

    async def _save_data_redis(
        self,
        df: pd.DataFrame,
        redis_key: str,
    ) -> None:
        if df.empty:
            return

        if self._data_frame_source == DataFrameSource.FILE and self._is_final_file:
            redis_key = self.redis_keys.get_erp_redis_key()

        df_info = io.StringIO()
        df.info(buf=df_info)

        self._logger.info(f"Data Frame: {df_info.getvalue()}")

        buffer_df: io.BytesIO = self.redis.set_parquet(df=df)
        self.redis.set(key=redis_key, value=buffer_df)
        self.redis.medir_tamano_valor(df=df, buffer_df=buffer_df)
        self._logger.error(f"DataFrame guardado con la Redis Key: {redis_key}")

    def _get_list_erp_final(self, df_erp: pd.DataFrame) -> list[HeaderConfig]:
        # Se recupera de redis lista de erp headers
        headers_erp: list[HeaderConfig] = self._header_types.get_headers_list(
            redis_key=self.redis_keys.get_headers_erp_list_key()
        )
        headers_erp_final: list[HeaderConfig] = []

        for header in headers_erp:
            found = False
            for col in df_erp.columns:
                nombre_base = col.split("_")[0]

                if col.endswith("_x") or col.endswith("_y"):
                    if header.nombre == nombre_base:
                        header_config: HeaderConfig = HeaderConfig(
                            nombre=col,
                            configuracion_tipo_dato=header.configuracion_tipo_dato,
                            origen=header.origen,
                            mostrar_reporte=header.mostrar_reporte,
                        )
                        headers_erp_final.append(header_config)
                        found = True
                        break
                elif header.nombre == nombre_base:
                    headers_erp_final.append(header)
                    found = True
                    break
            if found:
                continue

        self._logger.info(f"Numero de columnas ERP guardadas: {len(headers_erp)}")
        self._logger.info(f"Headers erp: {headers_erp}")

        return headers_erp_final
