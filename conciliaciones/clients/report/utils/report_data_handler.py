from io import BytesIO

import pandas as pd
from k_link.db.core import ObjectId
from k_link.db.daos import (
    ConciliationReportDAO,
    HeaderNameKreportsDAO,
    LinkServicesDAO,
    PivotCustomDAO,
    ProjectDAO,
    ReportCatalogDAO,
)
from k_link.db.models import HeaderNameKreports, LinkServices, Project, ReportCatalog
from k_link.db.models.conciliation_report import ConciliationReport
from k_link.db.models.pivot_customs import PivotCustom
from k_link.extensions.conciliation_type import ConciliationType
from k_link.extensions.pipeline import GroupOptions
from k_link.extensions.pipeline.pivot_table_options import PivotOptions
from k_link.extensions.report_config import (
    HeaderConfig,
    KRConfig,
    KReportsRequest,
    OrigenColumna,
    OrigenDF,
    ReportConfig,
    TipoDato,
)
from k_link.extensions.report_result import (
    ReportMetadata,
    ReportOutputType,
    StatusConciliationReport,
)
from k_link.utils.bucket import BucketManager
from k_link.utils.files.abc_datasource import DataFrame
from k_link.utils.pydantic_types import Date
from loggerk import LoggerK

from conciliaciones.utils.completion_handler.airflow_contex_exception import (
    AirflowContexException,
)
from conciliaciones.utils.filters.conciliation_filters import ConciliationReportUtils
from conciliaciones.utils.redis.redis_keys import RedisKeys
from conciliaciones.utils.redis.redis_storage import RedisStorage

# DAOs y manejadores globales
DAO_PROYECTO = ProjectDAO()
BUCKET_MANAGER = BucketManager()
LINK_SERVICE_DAO = LinkServicesDAO()
CONCILIATION_REPORT_DAO = ConciliationReportDAO()
PIVOT_TEMPLATES_DAO = PivotCustomDAO()
REPORT_TYPE_DAO = ReportCatalogDAO()
HEADERS_REPORT_KREPORTS = HeaderNameKreportsDAO()


class ReportDataHandler:
    def __init__(
        self,
        run_id: str,
        project_id_str: str,
        month: int,
        year: int,
        conciliation_type: ConciliationType,
    ):
        self._logger = LoggerK(self.__class__.__name__)
        self._run_id = run_id
        self.project_id_str = project_id_str
        self.project_id = ObjectId(project_id_str)
        self.month = month
        self.year = year
        self._conciliation_type: ConciliationType = conciliation_type

        self.redis = RedisStorage()
        self.redis_keys = RedisKeys(
            run_id=run_id,
            project_id_str=self.project_id_str,
            month=self.month,
            year=self.year,
            conciliation_type=self._conciliation_type,
        )
        self._airflow_fail_exception = AirflowContexException(
            year=year,
            month=month,
            project_id=project_id_str,
            run_id=run_id,
            conciliation_type=conciliation_type,
        )

        self.project: Project | None = DAO_PROYECTO.get_by_id_sync(
            item_id=self.project_id
        )

        self._pivot_templates: PivotCustom | None = PIVOT_TEMPLATES_DAO.get_sync(
            project_id=self.project_id
        )

        if self._pivot_templates is None:
            self._airflow_fail_exception.handle_and_store_exception(
                f"No se encontró templates de tablas dinámicas para el proyecto: {self.project_id_str}"
            )

        self.link_service: LinkServices | None = LINK_SERVICE_DAO.get_sync(
            project_id=self.project_id
        )

        if self.link_service is None:
            self._airflow_fail_exception.handle_and_store_exception(
                f"No se encontró configuración de LinkServices para el proyecto: {self.project_id_str}"
            )

        report_id: ObjectId | None = None
        if self.link_service.report_config:
            report_type: KReportsRequest | None = (
                self.link_service.report_config.report_type
            )

            if report_type is None:
                self._airflow_fail_exception.handle_and_store_exception(
                    f"No se encontró ReportType en la configuración de LinkServices para el proyecto: {self.project_id_str}"
                )

            report_id = report_type.report_id

        if report_id is None:
            self._airflow_fail_exception.handle_and_store_exception(
                f"El ID del ReportType asociado al proyecto: {self.project_id_str} es None"
            )

        self.mongo_report_catalog: ReportCatalog | None = (
            REPORT_TYPE_DAO.get_by_id_sync(item_id=report_id)
        )

        if self.mongo_report_catalog is None:
            self._airflow_fail_exception.handle_and_store_exception(
                f"No se encontró Report Catalog para el ID: {report_id} asociado al proyecto: {self.project_id_str}"
            )

        if not isinstance(self.link_service.report_config, ReportConfig):
            self._airflow_fail_exception.handle_and_store_exception(
                f"Report Config no es del tipo esperado para el proyecto: {self.project_id_str}"
            )
        self.report_config: ReportConfig = self.link_service.report_config  # type: ignore

        if self.report_config is None:
            self._airflow_fail_exception.handle_and_store_exception(
                f"No se encontró Report Config para el proyecto: {self.project_id_str}"
            )

        self.report_type: KReportsRequest | None = self.report_config.report_type
        self.report_config_headers = self.report_config.headers_erp
        self.report_type_headers = self.mongo_report_catalog.headers
        self.report_config_pt = self._pivot_templates.pivot_tables
        self.headers_sat: list[HeaderConfig] = []

    def get_report_type(self) -> ReportCatalog | None:
        """Devuelve el report_type"""
        return self.mongo_report_catalog

    def get_report_sheets(self, report_name: str) -> ReportCatalog:
        report_sheet = REPORT_TYPE_DAO.get_sync(name=report_name)

        if report_sheet is None:
            self._airflow_fail_exception.handle_and_store_exception(
                f"No se encontró ReportType para el nombre: {report_name}"
            )

        return report_sheet

    def get_file_name(  # noqa: RET503
        self, file_type: ReportOutputType, conciliation_type: ConciliationType
    ) -> str:
        """Genera el nombre del archivo basado en el proyecto y fecha."""
        if self.project is None:
            self._airflow_fail_exception.handle_and_store_exception(
                f"No hay proyecto asociado al ID: {self.project_id_str}"
            )
        file_name: str = ""

        if conciliation_type == ConciliationType.MONTHLY:
            return f"{self.project.owner_rfc} {self.project.name} {self.year} {self.month}.{file_type.value}"
        if conciliation_type == ConciliationType.ACCUMULATED:
            return f"{self.project.owner_rfc} {self.project.name} acumulada {self.year}.{file_type.value}"
        if conciliation_type == ConciliationType.UNITARY:
            return f"{self.project.owner_rfc} {self.project.name} unitaria.{file_type.value}"
        self._airflow_fail_exception.handle_and_store_exception(
            f"Tipo de conciliación no soportado: {conciliation_type}"
        )

        if file_name == "":
            self._logger.error("file name vacío")

        return file_name

    def get_s3_path(
        self, file_type: ReportOutputType, create_execution_date: Date
    ) -> str:
        """Devuelve la ruta donde se guardará el archivo en S3 para reporte mensual."""
        if self.project is None:
            self._airflow_fail_exception.handle_and_store_exception(
                f"No hay proyecto asociado al ID: {self.project_id_str}"
            )

        return "/".join(
            [
                self.project.owner_rfc,
                self.project.project_type,
                f"{self.project_id_str}",
                "reports",
                "mensual",
                str(self.year),
                str(self.month),
                f"{create_execution_date}",
                self.get_file_name(
                    file_type=file_type, conciliation_type=self._conciliation_type
                ),
            ]
        )

    def get_s3_path_unitario(
        self, file_type: ReportOutputType, create_execution_date: Date
    ) -> str:
        """Devuelve la ruta donde se guardará el archivo en S3 para reporte unitario."""

        if self.project is None:
            self._airflow_fail_exception.handle_and_store_exception(
                f"No hay proyecto asociado al ID: {self.project_id_str}"
            )

        return "/".join(
            [
                self.project.owner_rfc,
                self.project.project_type,
                f"{self.project_id_str}",
                "reports",
                "unitaria",
                f"{create_execution_date}",
                self.get_file_name(
                    file_type=file_type, conciliation_type=self._conciliation_type
                ),
            ]
        )

    def get_s3_path_acumulados(
        self, file_type: ReportOutputType, create_execution_date: Date
    ) -> str:
        """Devuelve la ruta donde se guardará el archivo en S3 para reporte acumulado."""

        if self.project is None:
            self._airflow_fail_exception.handle_and_store_exception(
                f"No hay proyecto asociado al ID: {self.project_id_str}"
            )

        return "/".join(
            [
                self.project.owner_rfc,
                self.project.project_type,
                f"{self.project_id_str}",
                "reports",
                "acumuladas",
                str(self.year),
                f"{create_execution_date}",
                self.get_file_name(
                    file_type=file_type, conciliation_type=self._conciliation_type
                ),
            ]
        )

    def get_tabla_config(self) -> list[HeaderConfig]:
        """Obtiene la configuración de la tabla del reporte."""
        return self.report_config_headers

    def get_tipo_header(self) -> dict:
        """Obtiene el tipo de dato de cada encabezado."""
        return {
            header.nombre: header.configuracion_tipo_dato.value
            for header in self.report_config_headers
        }

    async def get_info_metadata_report(self) -> ReportMetadata:
        filters: dict = ConciliationReportUtils.build_filters_for_conciliation_type(
            project_id=self.project_id,
            conciliation_type=self._conciliation_type,
            year=self.year,
            month=self.month,
        )

        conciliation_report: (
            ConciliationReport | None
        ) = await CONCILIATION_REPORT_DAO.get(**filters)

        if conciliation_report is None:
            raise ValueError(
                f"Conciliation report not found for project {self.project_id_str}"
            )

        reports: list[ReportMetadata] = conciliation_report.report_metadata

        if ConciliationReportUtils.validate_history_report(self.project_id):
            existing_report: ReportMetadata | None = (
                ConciliationReportUtils.find_today_execution_report(
                    reports, self._run_id
                )
            )

            self._logger.error(f"Objeto: {existing_report}, {self._run_id}")

            if existing_report is None:
                self._airflow_fail_exception.handle_and_store_exception(
                    f"No se encontró un reporte existente para el tipo de conciliación {self._conciliation_type.value} para el proyecto: {self.project_id_str}"
                )
        else:
            existing_report = reports[-1]

        self._logger.error(f"Objeto: {existing_report}")

        return existing_report

    async def save_mongo_report(
        self,
        final_path: str,
        file_type: ReportOutputType,
    ) -> None:
        """
        Guarda o actualiza el reporte en MongoDB.

        Args:
            final_path (str): ruta del s3.
            file_type (ReportOutputType): tipo de archivo.

        Raises:
            ValueError: Si link_service está vacío.
        """

        filters: dict = ConciliationReportUtils.build_filters_for_conciliation_type(
            project_id=self.project_id,
            conciliation_type=self._conciliation_type,
            year=self.year,
            month=self.month,
        )

        conciliation_report: (
            ConciliationReport | None
        ) = await CONCILIATION_REPORT_DAO.get(**filters)

        if conciliation_report is None:
            raise ValueError(
                f"Conciliation report not found for project {self.project_id_str}"
            )

        reports: list[ReportMetadata] = conciliation_report.report_metadata

        if ConciliationReportUtils.validate_history_report(self.project_id):
            existing_report: ReportMetadata | None = (
                ConciliationReportUtils.find_today_execution_report(
                    reports, self._run_id
                )
            )

            self._logger.error(f"Objeto: {existing_report}, {self._run_id}")

            if existing_report is None:
                self._airflow_fail_exception.handle_and_store_exception(
                    f"No se encontró un reporte existente para el tipo de conciliación {self._conciliation_type.value} para el proyecto: {self.project_id_str}"
                )
        else:
            existing_report = reports[-1]

        self._logger.error(f"Objeto: {existing_report}")

        existing_report.name[file_type] = self.get_file_name(
            file_type=file_type, conciliation_type=self._conciliation_type
        )
        existing_report.s3_path[file_type] = final_path
        existing_report.status = StatusConciliationReport.CONCILIADO
        existing_report.detail = "Reporte conciliado"

        self._logger.error(f"Objeto actualizado: {existing_report}")

        await CONCILIATION_REPORT_DAO.update_by_id(
            conciliation_report.id,  # type: ignore
            conciliation_report,  # type: ignore
        )
        self._logger.info(f"Reporte {file_type} actualizado.")

    async def save_s3_report(
        self,
        excel_buffer: BytesIO,
        file_type: ReportOutputType,
        conciliacion_type: ConciliationType,
        create_execution_date: Date,
    ) -> str:
        """
        Guarda el reporte en S3.

        Args:
            excel_buffer (BytesIO): Archivo Excel en memoria.
        """

        try:
            self._logger.info(
                f"Subiendo archivo a S3 con tipo {conciliacion_type.value}..."
            )

            if not isinstance(excel_buffer, BytesIO):
                self._airflow_fail_exception.handle_and_store_exception(
                    "El buffer de Excel no es del tipo BytesIO."
                )

            if conciliacion_type == ConciliationType.MONTHLY:
                destination_path = self.get_s3_path(file_type, create_execution_date)
            elif conciliacion_type == ConciliationType.UNITARY:
                destination_path = self.get_s3_path_unitario(
                    file_type, create_execution_date
                )
            elif conciliacion_type == ConciliationType.ACCUMULATED:
                destination_path = self.get_s3_path_acumulados(
                    file_type, create_execution_date
                )
            else:
                self._airflow_fail_exception.handle_and_store_exception(
                    f"Tipo de conciliación no soportado: {conciliacion_type}"
                )

            self._logger.info(f"Archivo subido a S3. {destination_path}")

            return BUCKET_MANAGER.upload_file_from_bytes(excel_buffer, destination_path)

        except Exception as exc:
            self._logger.error("Error al subir archivo a S3: %s", exc)
            raise exc

    async def get_dataframe_sat_no_erp(self) -> DataFrame:
        """
        Obtiene el DataFrame de conciliación SAT no ERP desde Redis.

        Returns:
            DataFrame: df sat_no_erp con las columnas filtradas.
        """

        redis_key: str = self.redis_keys.get_sat_no_erp_periodo_key()

        if redis_key is None:
            raise ValueError(f"Redis key: {redis_key} no encontrada.")

        if self.report_type_headers is None:
            raise ValueError("report_type_headers no está inicializado.")

        df_sat_no_erp: pd.DataFrame | None = self.redis.get_df(redis_key=redis_key)

        if df_sat_no_erp is None:
            raise ValueError(f"df vacio. ID project: {self.project_id_str}")

        return df_sat_no_erp

    async def get_sat_no_erp_data(self) -> tuple[DataFrame, list[HeaderConfig]]:
        """
        Obtiene los datos de conciliación SAT no ERP desde Redis.

        Returns:
            DataFrame: df sat_no_erp con las columnas filtradas.

        Raises:
            ValueError: Si no encuentra llave de redis.
            ValueError: Si report_type_headers y el df esta vacio.
        """

        df_sat_no_erp: DataFrame = await self.get_dataframe_sat_no_erp()

        headers_sat, headers_sat_config = await self.ordenar_columnas_sat(
            df=df_sat_no_erp
        )
        self._logger.info(f"df Sat: {df_sat_no_erp}")

        return df_sat_no_erp.loc[:, headers_sat], headers_sat_config

    async def ordenar_columnas_erp_sat(self, df: DataFrame) -> list[str]:
        """
        Ordena las columnas según la configuración de link services y include de proyectos.

        Args:
            df (DataFrame): dataframe a ordenar.

        Returns:
            list[str]: lista de los headers filtrados.

        Raises:
            ValueError: Si report_type_headers está vacío.
        """
        if self.report_type_headers is None:
            self._airflow_fail_exception.handle_and_store_exception(
                "Los headers de ReportType no están inicializados."
            )

        if self.report_config is None:
            return df.columns.tolist()

        headers_erp_sat = [
            header_custom.nombre
            for header_custom in self.report_config.headers_custom
            if header_custom.nombre in df.columns
        ]

        return headers_erp_sat

    async def ordenar_columnas_sat(
        self, df: DataFrame
    ) -> tuple[list[str], list[HeaderConfig]]:
        """
        Ordena las columnas según la configuración de la lista include de proyectos.

        Args:
            df (DataFrame): dataframe a ordenar.

        Returns:
            list[str]: lista de los headers filtrados.

        Raises:
            ValueError: Si report_type_headers está vacío.
        """

        if self.report_type is None:
            self._airflow_fail_exception.handle_and_store_exception(
                f"El Report Type no está inicializado para el proyecto: {self.project_id_str}"
            )

        request_config: KRConfig | None = self.report_type.request_config

        if request_config is None:
            self._airflow_fail_exception.handle_and_store_exception(
                f"No se encontro configuracion KRConfig para el Report Type del proyecto: {self.project_id_str}"
            )

        self._logger.info(f"inlcude list: {request_config.include}")

        # Verifica si report_config está inicializado
        if self.report_config is None:
            raise ValueError("Report config not found")

        if self.report_config.headers_sat is None:
            raise ValueError("Headers sat not found.")

        headers_report_type: list[HeaderConfig] = self.report_config.headers_sat
        headers_report_type_dict: dict[str, HeaderConfig] = {
            header.nombre: header for header in headers_report_type
        }
        headers_report_type_names: list[str] = [
            header.nombre for header in headers_report_type
        ]

        if self.report_type_headers is None:
            raise ValueError("report_type_headers no está inicializado.")

        if request_config.include is None:
            request_config.include = []

        include_list: list[str] = [
            header_sat.nombre
            for header_df in df.columns
            if header_df in headers_report_type_names
            and (header_sat := headers_report_type_dict[header_df]).mostrar_reporte
        ]

        include_list_config: list[HeaderConfig] = [
            header_sat
            for header_df in df.columns
            if header_df in headers_report_type_names
            and (header_sat := headers_report_type_dict[header_df]).mostrar_reporte
        ]

        include_list = include_list + await self.get_dinamic_headers()
        include_list_config: list[HeaderConfig] = (
            include_list_config + await self._get_dynamic_headers_config(df)
        )

        self._logger.info(f"include list: {include_list}")

        headers_sat_config: list[HeaderConfig] = [
            header_config
            for header_config in include_list_config
            if header_config.nombre in df.columns
        ]

        headers_sat: list[str] = [
            header for header in include_list if header in df.columns
        ]

        self._logger.info(f"Headers Sat en ordenar_columnas_sat: {headers_sat}")

        return headers_sat, headers_sat_config

    async def get_dinamic_headers(self) -> list[str]:
        """
        Obtiene los headers dinámicos del reporte.
        """

        if self.report_type is None:
            self._airflow_fail_exception.handle_and_store_exception(
                f"El Report Type no está inicializado para el proyecto: {self.project_id_str}"
            )

        request_config: KRConfig | None = self.report_type.request_config

        if request_config is None:
            self._airflow_fail_exception.handle_and_store_exception(
                f"No se encontro configuracion KRConfig para el Report Type del proyecto: {self.project_id_str}"
            )

        dynamic_headers_key: str = self.redis_keys.get_dynamic_headers_redis_key()

        dinamic_headers: list[str] | None = self.redis.get(
            key=dynamic_headers_key, object_type=list[str]
        )

        if dinamic_headers is None:
            return []

        return dinamic_headers

    async def get_pivot_table_data(
        self,
        origen_df: OrigenDF,
        pivot_name: str,
        funcion_sheet: str | None = None,
    ) -> DataFrame:
        """
        Obtiene los datos de conciliación ERP y SAT desde Redis.

        Returns:
            DataFrame: dataframe filtrado
        """

        pivot_t_map = {
            OrigenDF.ERP_SAT: self.redis_keys.get_sat_erp_redis_key(),
            OrigenDF.SAT_NO_ERP: self.redis_keys.get_sat_no_erp_periodo_key(),
            OrigenDF.SHEETS: self.redis_keys.get_sat_sheets_key(funcion=funcion_sheet),
            OrigenDF.DESCARGA_P: self.redis_keys.get_sat_erp_meta_key(),
            OrigenDF.METADATA_C: self.redis_keys.get_sat_erp_meta_cancel_key(),
            OrigenDF.GROUP_BY: self.redis_keys.get_dataframe_group_redis_key(
                pivot_name
            ),
            OrigenDF.PIVOT_TABLE: self.redis_keys.get_dataframe_pivot_redis_key(
                pivot_name
            ),
        }

        redis_key = pivot_t_map.get(origen_df)

        if redis_key is None:
            self._airflow_fail_exception.handle_and_store_exception(
                f"No se encontró la llave de Redis para el origen de datos: {origen_df}"
            )

        df: pd.DataFrame | None = self.redis.get_df(redis_key=redis_key)

        if df is None:
            self._airflow_fail_exception.handle_and_store_exception(
                f"No se encontró el DataFrame para la llave de Redis: {redis_key}"
            )

        self._logger.info(f"Table config: {self.report_config_headers}")

        if origen_df == OrigenDF.ERP_SAT:
            headers_pivot_table: list[str] = await self.ordenar_columnas_erp_sat(df)
            return df.loc[:, headers_pivot_table]

        return df

    def group_by_apply(self, df: DataFrame, group_by: GroupOptions) -> DataFrame:
        """
        Agrupa y agrega los datos de un DataFrame.

        Args:
            df (DataFrame): DataFrame original a agrupar.
            group_by (GroupOptions): Opciones de agrupamiento y funciones de agregación.

        Returns:
            DataFrame: DataFrame agrupado y con índice reseteado.
        """
        if self.error_headers(df, group_by):
            self._logger.error("No se aplicará agrupado por falta de headers.")
            return pd.DataFrame()

        self._logger.info(f"Grouping by: {group_by.by}")
        self._logger.info(f"Aggregation functions: {group_by.aggfuncs}")

        df_grouped: DataFrame = df.groupby(by=group_by.by).agg(group_by.aggfuncs)  # type: ignore
        df_grouped = df_grouped.reset_index()

        self._logger.info(f"Grouped DataFrame:\n{df_grouped}")

        return df_grouped

    def error_headers(self, df: DataFrame, group_by: GroupOptions) -> bool:
        """
        Valida que los headers utilizados en el agrupado estén presentes en el dataframe.

        Args:
            df (DataFrame): DataFrame a validar.
            group_by (GroupOptions): Opciones de agrupamiento que contienen los headers.

        Raises:
            ValueError: Si algún encabezado requerido no está presente en el DataFrame.
        """
        headers = group_by.by + list(group_by.aggfuncs.keys())
        missing_headers = [header for header in headers if header not in df.columns]

        if missing_headers:
            self._logger.error(
                f"Faltan los siguientes encabezados para el agrupado: {missing_headers}"
            )

            return True
        return False

    async def get_dataframe_erp_sat(self) -> DataFrame:
        """
        Obtiene el DataFrame de conciliación ERP y SAT desde Redis.
        Returns:
            DataFrame: dataframe filtrado
        """
        redis_key_erp: str = self.redis_keys.get_sat_erp_redis_key()

        df_erp_sat: pd.DataFrame | None = self.redis.get_df(redis_key=redis_key_erp)

        if df_erp_sat is None:
            raise ValueError(f"df vacio. ID project: {self.project_id_str}")

        self.redis.set("df_erp_limpio.csv", df_erp_sat.to_csv(index=False))

        return df_erp_sat

    async def get_headers_erp_sat(self, df: DataFrame) -> list[HeaderConfig]:
        """
        Obtiene los headers ERP + SAT asociados al report_type.
        Args:
            df (DataFrame): dataframe a filtrar.
        Returns:
            list[HeaderConfig]: lista de los headers filtrados.
        """
        headers_config_final: list[HeaderConfig] = []

        # Verifica si report_config está inicializado
        if self.report_config is None:
            raise ValueError("Report config not found")

        if self.report_config.headers_custom is None:
            raise ValueError("Headers erp_sat not found.")

        headers_config_final = (
            self.report_config.headers_custom
            + await self._get_dynamic_headers_config(df)
        )

        return [
            header
            for header in headers_config_final
            if header.nombre in df.columns and header.mostrar_reporte
        ]

    def map_dtype_to_tipo(self, dtype) -> TipoDato:
        """
        Mapea un tipo de dato de pandas/numpy a un tipo usado en el reporte.

        Args:
            dtype (Any): Tipo de dato de la columna.

        Returns:
            str: Tipo convertido, puede ser:
                - "MONEDA" para numéricos (float, int).
                - "FECHA" para tipos datetime.
                - "TEXTO" para cualquier otro tipo.
        """
        if str(dtype).startswith("float") or str(dtype).startswith("int"):
            return TipoDato.MONEDA
        if "datetime" in str(dtype):
            return TipoDato.FECHA
        return TipoDato.TEXTO

    async def get_erp_sat_data(self) -> DataFrame:
        """
        Obtiene los datos de conciliación ERP y SAT desde Redis.

        Returns:
            DataFrame: dataframe filtrado
        """
        df_erp_sat: DataFrame = await self.get_dataframe_erp_sat()

        headers_custom: list[HeaderConfig] = await self.get_headers_erp_sat(
            df=df_erp_sat
        )

        headers_erp_sat: list[str] = [
            header.nombre for header in headers_custom if header.nombre
        ]

        return df_erp_sat.loc[:, headers_erp_sat]

    async def get_erp_sat_no_erp_data(self) -> DataFrame:
        """
        Obtiene los datos de conciliación ERP y SAT no ERP desde Redis.

        Returns:
            DataFrame: dataframe combinado de ERP + SAT y SAT no ERP.
        """
        erp_sat_data: DataFrame = await self.get_erp_sat_data()
        sat_no_erp_data, _ = await self.get_sat_no_erp_data()

        return pd.concat([erp_sat_data, sat_no_erp_data], ignore_index=True)

    async def get_pending_data(self) -> DataFrame:
        redis_key: str = self.redis_keys.get_sat_erp_meta_key()

        df_pending: pd.DataFrame | None = self.redis.get_df(redis_key=redis_key)

        if df_pending is None:
            return pd.DataFrame()

        return df_pending

    async def get_cancelled_data(self) -> DataFrame:
        redis_key = self.redis_keys.get_sat_erp_meta_cancel_key()

        df_cancelled: DataFrame | None = self.redis.get_df(redis_key=redis_key)

        if df_cancelled is None:
            return pd.DataFrame()

        return df_cancelled

    def get_pivot_tables_config(self) -> list[PivotOptions]:
        """Obtiene la configuracion para a pivot table"""
        return self.report_config_pt

    def filter_columns_erp(self, df_erp_sat: DataFrame) -> list[HeaderConfig]:
        """
        Aplica filtro a los headers de link services

        Args:
            df_erp_sat (DataFrame): informacion de erp + sat.

        """
        table_config: list[HeaderConfig] = self.report_config_headers
        headers_erp: list[HeaderConfig] = []

        headers_erp = [
            header
            for header in table_config
            if header.nombre in df_erp_sat.columns and header.mostrar_reporte
        ]

        return headers_erp

    async def get_headers_report_kreports(
        self, report_type: ReportCatalog
    ) -> dict[str, str]:
        """
        Obtiene los headers del report_type asociado al reporte.
        Args:
            report_type (ReportCatalog): Reporte asociado al report_type.
        Returns:
            dict[str, str]: Diccionario con los headers del report_type.
        """
        if report_type is None:
            return {}

        dict_report: HeaderNameKreports | None = HEADERS_REPORT_KREPORTS.get_sync(
            id_reporte_asociado=report_type.id
        )

        if dict_report is None:
            return {}

        dynamic_headers: list[str] = await self.get_dinamic_headers()

        dict_report.header_names.update(
            {dynamic_header: dynamic_header for dynamic_header in dynamic_headers}
        )

        return dict_report.header_names

    async def get_headers_sat(self, df: DataFrame) -> list[HeaderConfig]:
        """
        Obtiene los headers de SAT asociados al report_type.
        Args:
            df (DataFrame): DataFrame a filtrar.
        Returns:
            dict[str, str]: Diccionario con los headers de SAT.
        """
        headers_sat: list[HeaderConfig] = []
        headers_sat_final: list[HeaderConfig] = []

        if self.report_type is None:
            self._airflow_fail_exception.handle_and_store_exception(
                f"El Report Type no está inicializado para el proyecto: {self.project_id_str}"
            )

        request_config: KRConfig | None = self.report_type.request_config

        if request_config is None:
            self._airflow_fail_exception.handle_and_store_exception(
                f"No se encontro configuracion KRConfig para el Report Type del proyecto: {self.project_id_str}"
            )

        # Verifica si report_config está inicializado
        if self.report_config is None:
            raise ValueError("Report config not found")

        if self.report_config.headers_sat is None:
            raise ValueError("Headers sat not found.")

        headers_report_type: list[HeaderConfig] = self.report_config.headers_sat
        headers_report_type_dict: dict[str, HeaderConfig] = {
            header.nombre: header for header in headers_report_type
        }

        headers_report_type_names: list[str] = [
            header.nombre for header in headers_report_type
        ]

        if request_config.include is None:
            request_config.include = []

        include_list: list[str] = [
            header_sat.nombre
            for header_df in df.columns
            if header_df in headers_report_type_names
            and (header_sat := headers_report_type_dict[header_df]).mostrar_reporte
            and header_sat.nombre in request_config.include
        ]

        include_list = include_list + await self.get_dinamic_headers()

        headers_sat: list[HeaderConfig] = self.report_config.headers_sat
        headers_sat = headers_sat + await self._get_dynamic_headers_config(df)

        headers_sat_dict: dict[str, HeaderConfig] = {
            header.nombre: header for header in headers_sat
        }

        for header_name in include_list:
            header_sat_config: HeaderConfig = headers_sat_dict[header_name]
            headers_sat_final.append(header_sat_config)

        return headers_sat_final

    async def _get_dynamic_headers_config(self, df) -> list[HeaderConfig]:
        dynamic_headers_config: list[HeaderConfig] = []
        dynamic_headers: list[str] = await self.get_dinamic_headers()

        if dynamic_headers and dynamic_headers != []:
            for name_header in dynamic_headers:
                if name_header in df.columns:
                    dtype = df[name_header].dtype
                    dynamic_header_config = HeaderConfig(
                        nombre=name_header,
                        configuracion_tipo_dato=self.map_dtype_to_tipo(dtype),
                        origen=OrigenColumna.SAT,
                        mostrar_reporte=True,
                    )
                    dynamic_headers_config.append(dynamic_header_config)

        return dynamic_headers_config
