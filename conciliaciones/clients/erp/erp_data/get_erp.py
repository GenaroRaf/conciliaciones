"""
Clase para extraer datos de erp desde S3 y colocarlos en redis
Valida las columnas de los archivos Vs la configuración
"""

import io
from io import BytesIO

import httpx
import pandas as pd
from k_link.db.core import ObjectId
from k_link.db.daos import ERPFilesDAO, ProjectDAO
from k_link.db.models import ERPFiles
from k_link.extensions import ConciliationType
from k_link.extensions.datasources import (
    Config,
    DataSourceCatalog,
    DataSourceCatalogMetadata,
    DataSources,
    Uploads,
)
from k_link.extensions.parameters import (
    AccumulatedParameters,
    MonthlyParameters,
    UnitParameters,
)
from k_link.utils.bucket import BucketManager
from k_link.utils.files import DataSource
from k_link.utils.pydantic_types import Date
from loggerk import LoggerK

from conciliaciones.utils.completion_handler.airflow_contex_exception import (
    AirflowContexException,
)
from conciliaciones.utils.data.normalize import normalize_date, normalize_df
from conciliaciones.utils.redis.redis_keys import RedisKeys
from conciliaciones.utils.redis.redis_storage import RedisStorage

# DAO instances
PROYECTO = ProjectDAO()
ERP_FILES = ERPFilesDAO()


class DatosERP:
    _logger: LoggerK
    """
        Clase para manejar la extracción y validación de datos ERP.
    """

    def __init__(
        self,
        run_id: str,
        project_id_str: str,
        conciliation_type: ConciliationType,
        year: int,
        month: int,
    ) -> None:
        """
        Inicializa la instancia.

            Args:
                project_id_str (str): ID del proyecto como cadena.
                year (int): Año de los datos.
                month (int): Mes de los datos.
        """

        self._logger = LoggerK(self.__class__.__name__)

        self.project_id_str = project_id_str
        self.year: int = year
        self.month: int = month
        self.conciliation_type: ConciliationType = conciliation_type

        self.redis = RedisStorage()
        self.redis_keys = RedisKeys(
            run_id=run_id,
            project_id_str=self.project_id_str,
            month=self.month,
            year=self.year,
            conciliation_type=self.conciliation_type,
        )

        self._airflow_fail_exception = AirflowContexException(
            year=self.year,
            month=self.month,
            project_id=project_id_str,
            run_id=run_id,
            conciliation_type=self.conciliation_type,
        )

    async def extraer_datos_erp(
        self,
    ) -> list[str]:
        """
        Extrae y valida datos ERP desde la configuración del proyecto.
        """

        today = normalize_date(self.year, self.month)

        self._logger.info(f"Proyect ID: {self.project_id_str}   Fecha: {today} ")

        erp_files: ERPFiles | None = await ERP_FILES.get(
            project_id=ObjectId(self.project_id_str)
        )

        if erp_files is None:
            self._airflow_fail_exception.handle_and_store_exception(
                f"No se encontró configuración de ERP para el proyecto {self.project_id_str}"
            )

        datasources: list[DataSources] | None = erp_files.data_sources

        if datasources is None:
            self._airflow_fail_exception.handle_and_store_exception(
                f"No se encontraron data sources para el proyecto {self.project_id_str}"
            )

        data_sources_catalogs: list[DataSourceCatalog] = erp_files.data_sources_catalogs

        datasources_optional: list[str] = await self.extraer_datos_datasources(
            data_sources=datasources, today=today
        )

        await self.extraer_datos_catalogos(data_sources_catalog=data_sources_catalogs)

        return datasources_optional

    async def extraer_datos_datasources(
        self, data_sources: list[DataSources], today: Date
    ) -> list[str]:
        datasources_optional: list[str] = []
        for data_source in data_sources:
            data_source_name: str = data_source.config.datasource_name

            self._logger.info(f"Data Source: {data_source}")
            self._logger.info(f"Data Source Name: {data_source_name}")

            if data_source.uploads is None:
                self._airflow_fail_exception.handle_and_store_exception(
                    f"No se encontraron uploads para el data source {data_source_name}"
                )

            # Obtiene datos de s3 del archivo de la ejecución actual
            datasource_upload: Uploads = await self.get_data_source_erp(
                data_source.uploads, today, conciliation_type=self.conciliation_type
            )

            if datasource_upload.is_optional:
                datasources_optional.append(data_source_name)
                continue

            self._logger.info(f"final_row: {data_source.config.final_row}")

            # Obtiene Data Frame del archivo de s3
            df_base: pd.DataFrame = await self.get_data_frame_erp(
                datasource_upload=datasource_upload, dataframe_config=data_source.config
            )

            self._logger.info(f"Dataframe erp columns: {df_base.columns.to_list()}")
            self._logger.info(
                f"Mongo columns: {data_source.config.header_types.keys()}"
            )

            headers_config: dict[str, ObjectId] = data_source.config.header_types

            # Selecciona solo columnas configuradas en Mongo
            df_base = await self.select_columns(df_base, config_columns=headers_config)

            # Almacena en redis archivos con columnas configuradas
            redis_key: str = self.redis_keys.get_erp_data_source_redis_key(
                datasource=data_source_name
            )

            self._logger.info(f"DF Base: {df_base}")

            self.save_redis(df_erp=df_base, redis_key=redis_key)

        return datasources_optional

    async def extraer_datos_catalogos(
        self, data_sources_catalog: list[DataSourceCatalog]
    ) -> None:
        for catalog in data_sources_catalog:
            self._logger.info(f"Data Source Name: {catalog.name}")

            catalog_metadata: DataSourceCatalogMetadata | None = (
                catalog.catalog_metadata
            )

            if catalog_metadata is None:
                self._airflow_fail_exception.handle_and_store_exception(
                    f"No se encontró metadata para el catálogo {catalog.name} del proyecto {self.project_id_str}"
                )

            df_base: pd.DataFrame = await self.catalog_bucket_to_df(
                s3_path=catalog_metadata.s3_path,
                catalog_config=catalog,
            )

            self._logger.info(f"Dataframe columns: {df_base.columns.to_list()}")
            self._logger.info(f"Mongo columns: {catalog.header_types.keys()}")

            headers_config: dict[str, ObjectId] = catalog.header_types

            df_base = await self.select_columns(df_base, config_columns=headers_config)

            redis_key: str = self.redis_keys.get_erp_data_source_redis_key(
                datasource=catalog.name
            )

            self._logger.info(f"DF Catalog: {df_base}")

            self.save_redis(df_erp=df_base, redis_key=redis_key)

    def save_redis(self, df_erp: pd.DataFrame, redis_key: str) -> None:
        """
        Guarda un DataFrame en Redis.

        Args:
            df_erp (pd.DataFrame): DataFrame a guardar.
            :param df_erp:
            :param redis_key:
        """
        self._logger.info("Dataframe info: ")
        self._logger.info(df_erp.info())
        buffer_df: BytesIO = self.redis.set_parquet(df=df_erp)
        self.redis.set(key=redis_key, value=buffer_df)
        self._logger.info(f"Redis Key: {redis_key}")

    async def select_columns(
        self, df_base: pd.DataFrame, config_columns: dict[str, ObjectId]
    ) -> pd.DataFrame:
        # Se obtienen las columnas configuradas en mongo
        try:
            # Se filtran las columnas del Data Frame con base en los registros de mongo
            df_base = df_base.loc[:, list(config_columns)]
        except (ValueError, KeyError) as error_type:
            # Si esto falla se obtienen las columans del Data Frame
            columns_name = df_base.columns

            # Se convierten ambas listas en conjuntos
            col_erp = set(columns_name)
            col_config = set(config_columns)

            # Se obtiene la diferencia entre ambas listas
            diff = col_config.symmetric_difference(col_erp)

            # Se detiene el DAG indicando la diferencia de columnas
            self._airflow_fail_exception.handle_and_store_exception(
                f"Columnas faltantes: {diff}, {error_type}"
            )
        return df_base

    async def get_data_source_erp(
        self, uploads: list[Uploads], today: Date, conciliation_type: ConciliationType
    ) -> Uploads:
        """
        Obtiene datos ERP desde una fuente base.

        Args:
            Uploads: Configuración de la fuente de datos.
            today (pd.Timestamp): Fecha normalizada.

        Returns:
            pd.DataFrame: Datos ERP como DataFrame.
        """

        datasource_upload: Uploads | None = None
        if conciliation_type == ConciliationType.MONTHLY:
            monthly_params: MonthlyParameters = MonthlyParameters(
                month=today.month,
                year=today.year,
            )

            datasource_upload = next(
                (
                    upload
                    for upload in uploads
                    if upload.conciliation_type == conciliation_type
                    and upload.conciliation_parameters == monthly_params
                ),
                None,
            )
        elif conciliation_type == ConciliationType.ACCUMULATED:
            accumulated_params: AccumulatedParameters = AccumulatedParameters(
                year=today.year,
            )

            datasource_upload = next(
                (
                    upload
                    for upload in uploads
                    if upload.conciliation_type == conciliation_type
                    and upload.conciliation_parameters == accumulated_params
                ),
                None,
            )
        elif conciliation_type == ConciliationType.UNITARY:
            unit_params: UnitParameters = UnitParameters()

            datasource_upload = next(
                (
                    upload
                    for upload in uploads
                    if upload.conciliation_type == conciliation_type
                    and upload.conciliation_parameters == unit_params
                ),
                None,
            )

        if datasource_upload is None:
            self._airflow_fail_exception.handle_and_store_exception(
                f"No se encontró un Uploads para la fecha {today.year} - {today.month} y tipo de conciliación {conciliation_type.value}"
            )

        return datasource_upload

    async def get_data_frame_erp(
        self, datasource_upload: Uploads, dataframe_config: Config
    ) -> pd.DataFrame:
        try:
            ds: DataSource = datasource_upload.datasource(dataframe_config)
            df_erp: pd.DataFrame = ds.dataframe
            df_erp = normalize_df(df_erp)
        except httpx.HTTPError as exc:
            self._airflow_fail_exception.handle_and_store_exception(
                f"Network error: {exc}"
            )
        return df_erp

    async def catalog_bucket_to_df(
        self,
        s3_path: str,
        catalog_config: DataSourceCatalog,
    ) -> pd.DataFrame:
        """
        Descarga un archivo de S3 y lo convierte en un DataFrame usando la configuración dada.

        Args:
            s3_path (str): Ruta S3 del archivo.
            catalog_config (DataSourceCatalog): Configuración del catálogo.

        Returns:
            pd.DataFrame: DataFrame con los datos del archivo.
        """

        if not s3_path:
            raise ValueError("s3_path is required")

        try:
            bucket_manager = BucketManager()
            file_url: str = bucket_manager.create_presigned_url(s3_path)

            async with httpx.AsyncClient() as client:
                response = await client.get(file_url)
                response.raise_for_status()

            binary_io = io.BytesIO(response.content)

            data_source_catalog = catalog_config.datasource_type.ds_class(
                excel_sheet_data=catalog_config.excel_sheet_data,
                file_path=binary_io,
                initial_column=catalog_config.initial_column,
                final_column=catalog_config.final_column,
                skip_rows=catalog_config.skip_rows,
                skip_footer=catalog_config.skip_footer,
                final_row=catalog_config.final_row,
                header_row=catalog_config.header_row,
            )

            df: pd.DataFrame = normalize_df(data_source_catalog.dataframe)

            return df

        except httpx.HTTPStatusError as e:
            self._airflow_fail_exception.handle_and_store_exception(
                f"Failed to fetch file from S3: {e}"
            )
        except Exception as e:
            self._airflow_fail_exception.handle_and_store_exception(
                f"Error processing S3 file: {e}"
            )
