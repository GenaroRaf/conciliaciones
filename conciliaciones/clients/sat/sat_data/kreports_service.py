from io import BytesIO

import pandas as pd
from k_link.db.core import ObjectId
from k_link.db.daos import LinkServicesDAO, ProjectDAO, ReportCatalogDAO
from k_link.db.models import LinkServices, Project, ReportCatalog
from k_link.extensions import ConciliationType
from k_link.extensions.pivot_k import PivoteKHeader
from k_link.extensions.report_config import KRConfig, KReportsRequest, ReportConfig
from k_link.tools import env
from loggerk import LoggerK

from conciliaciones.clients.sat.sat_data.kreports_filter import (
    KReportsFilter,
    RequestsFilters,
)
from conciliaciones.clients.sat.sat_data.utils.flatten_dict import flatten_dict
from conciliaciones.clients.sat.sat_data.utils.flatten_nomina_sabana import (
    get_nomina_headers_dict,
    order_headers_by_nomina,
)
from conciliaciones.clients.sat.sat_data.utils.flatten_sabana_impuestos import (
    procesar_impuestos,
)
from conciliaciones.clients.services.kreports_resource import KreportsResource
from conciliaciones.utils.completion_handler.airflow_contex_exception import (
    AirflowContexException,
)
from conciliaciones.utils.redis.redis_keys import RedisKeys
from conciliaciones.utils.redis.redis_storage import RedisStorage

PROJECT_DAO = ProjectDAO()


class KReportsService:
    list_tax_reports: list[str] = [
        "PUE_PPD_General_Sabana_Pagos",
        "PUE_PPD_General_Momentos",
        "PUE_PPD_General_Sabana",
        "PUE_CDP_Sabana",
    ]

    def __init__(
        self,
        run_id: str,
        project_id_str: str,
        year: int,
        month: int,
        filter: RequestsFilters,
        tipo_reporte: str | None,
        conciliation_type: ConciliationType,
        pivote: PivoteKHeader | None = None,
    ) -> None:
        self._logger = LoggerK(self.__class__.__name__)
        self._project_id_str: str = project_id_str
        self._year: int = year
        self._month: int = month
        self._filter: RequestsFilters = filter
        self._tipo_reporte: str | None = tipo_reporte
        self._conciliation_type: ConciliationType = conciliation_type
        self._pivote: PivoteKHeader | None = pivote

        self._project_dao = ProjectDAO()
        self._link_services_dao = LinkServicesDAO()
        self._report_type_dao = ReportCatalogDAO()

        self._redis = RedisStorage()
        self._redis_keys = RedisKeys(
            run_id=run_id,
            project_id_str=project_id_str,
            year=year,
            month=month,
            conciliation_type=conciliation_type,
        )
        self._kreports_filter = KReportsFilter(
            run_id=run_id,
            filter=filter,
            project_id_str=project_id_str,
            year=year,
            month=month,
            conciliation_type=conciliation_type,
        )
        self._airflow_fail_exception = AirflowContexException(
            run_id=run_id,
            project_id=project_id_str,
            year=year,
            month=month,
            conciliation_type=conciliation_type,
        )

    async def get_sat_report(
        self,
        sheets: bool = False,
        is_fiscal: bool = False,
        tipo_reporte: str | None = None,
    ) -> None:
        self._logger.info(f"Filtro utilizado: {self._filter.value}")
        self._logger.warning(f"Tipo de reporte: {tipo_reporte}")

        link_services: LinkServices | None = await self._link_services_dao.get(
            project_id=ObjectId(self._project_id_str)
        )

        if link_services is None:
            self._airflow_fail_exception.handle_and_store_exception(
                f"No se encontro configuración de LinkServices para el proyecto: {self._project_id_str}"
            )

        report_config: ReportConfig | None = link_services.report_config

        if (
            report_config is None
            or not report_config.report_sheets
            and self._filter == RequestsFilters.FILTER_SHEETS
        ):
            self._logger.error(
                f"Report config o extra sheets vacias, proyecto: {self._project_id_str}"
            )
            return

        project: Project | None = await self._project_dao.get_by_id(
            item_id=ObjectId(self._project_id_str)
        )

        if project is None:
            self._airflow_fail_exception.handle_and_store_exception(
                f"El proyecto con el id: {self._project_id_str} no existe en la base de datos"
            )

        enterprises: list[str] = project.enterprises

        self._logger.info(f"ID project: {self._project_id_str}")
        self._logger.info(f"Enterprises rfc: {enterprises}")

        if report_config is None:
            self._airflow_fail_exception.handle_and_store_exception(
                f"El report_config del proyecto con el id: {self._project_id_str} no existe en la base de datos"
            )

        if sheets:
            await self._get_report_sheets(
                enterprises=enterprises,
                report_config=report_config,
                is_fiscal=is_fiscal,
            )
        else:
            report_request: KReportsRequest | None = report_config.report_type

            if report_request is None:
                self._airflow_fail_exception.handle_and_store_exception(
                    f"El report type del proyecto con el id: {self._project_id_str} no existe en la base de datos"
                )

            dinamic_headers: list[str] = await self._get_report_type(
                enterprises=enterprises,
                report_request=report_request,
                is_fiscal=is_fiscal,
            )

            dynamic_headers_key: str = self._redis_keys.get_dynamic_headers_redis_key()

            link_services_updated: (
                LinkServices | None
            ) = await self._link_services_dao.update_by_id(
                item_id=link_services.id,  # type: ignore
                data=link_services,
            )

            if link_services_updated is None:
                self._airflow_fail_exception.handle_and_store_exception(
                    f"No se pudo actualizar el objeto LinkServices para el proyecto: {self._project_id_str}"
                )

            self._logger.info(f"Dinamic headers: {dinamic_headers}")

            self._redis.set(
                key=dynamic_headers_key,
                value=dinamic_headers,
            )

    async def _get_report_sheets(
        self, enterprises: list[str], report_config: ReportConfig, is_fiscal: bool
    ) -> None:
        report_sheets: list[KReportsRequest] | None = report_config.report_sheets

        if report_sheets is None:
            return self._logger.error(
                f"El report_sheets del proyecto con el id: {self._project_id_str} no existe en la base de datos"
            )

        for report_sheet in report_sheets:
            await self._get_report_type(
                enterprises=enterprises,
                report_request=report_sheet,
                is_fiscal=is_fiscal,
            )

    async def _get_report_type(  # noqa: PLR0912, PLR0915
        self, enterprises: list[str], report_request: KReportsRequest, is_fiscal: bool
    ) -> list[str]:
        total_erp_cfdis = 0
        erp_merged = []
        flat_merged = []

        self._logger.info(f"Report type: {report_request.report_id}")

        report_type: ReportCatalog | None = await self._report_type_dao.get_by_id(
            item_id=report_request.report_id
        )

        if report_type is None:
            self._airflow_fail_exception.handle_and_store_exception(
                f"El ReportType con el ID: {report_request.report_id} del proyecto: {self._project_id_str} no existe en la base de datos"
            )

        name_report: str = report_type.name
        servicio: str = report_type.function_service.service
        funcion: str = report_type.function_service.function_name

        self._logger.info(f"Servicio: {servicio}, Funcion: {funcion}")

        request_config: KRConfig | None = report_request.request_config

        if request_config is None:
            self._airflow_fail_exception.handle_and_store_exception(
                f"No se encontró la configuración 'request_config' para el tipo de reporte con ID: {report_request.report_id} en la base de datos. Verifique que el campo esté correctamente configurado."
            )

        for enterprise in enterprises:
            if (
                self._filter == RequestsFilters.FILTER_SAT_NO_ERP_PERIODO
                and report_type
            ):
                get_sat = await self._validate_sat_report(report_type=report_type)

                if get_sat is False:
                    self._logger.info(
                        f"El reporte {report_type.name} tiene la lista de UUDIs vacía para la empresa {enterprise}. No se realizará la peteción"
                    )
                    continue
            if is_fiscal or (
                self._filter == RequestsFilters.FILTER_SHEETS and is_fiscal
            ):
                request_filter: dict = await self._kreports_filter._get_sat_fiscal(
                    rfc=enterprise,
                )
            else:
                request_filter = await self._kreports_filter.get_filter(
                    report_type=report_type,
                    pivot_header_strategy=self._pivote,  # type: ignore
                    request_config=request_config,
                    rfc=enterprise,
                )

            self._logger.info(f"Request filter: {request_filter}")

            erp_cfdis_response = await getattr(KreportsResource(), funcion)(
                rfc=enterprise,
                token=env.DEV_TOKEN,
                filters=request_filter,
            )

            cfdis_enterprise: int = len(erp_cfdis_response.data)
            total_erp_cfdis += cfdis_enterprise

            self._logger.info(f"CFDIS de empresa {enterprise}: {cfdis_enterprise}")

            response_dict = erp_cfdis_response.model_dump()

            erp_merged.extend(response_dict["data"])

            self._logger.info(f"UUID encontrado: {erp_merged}")
            self._logger.info(f"Flat: {flat_merged}")

            try:
                if name_report == "Nomina_Sabana":
                    self._logger.info("Flat nomina sabana")
                    flat_merged = [
                        get_nomina_headers_dict(comprobante)
                        for comprobante in erp_merged
                    ]
                else:
                    self._logger.info("Flat no nomina sabana")
                    flat_merged = [
                        flatten_dict(comprobante) for comprobante in erp_merged
                    ]
            except Exception as _:
                self._airflow_fail_exception.handle_and_store_exception(
                    "Uno de los comprobantes está dañado, por favor proporcione un diccionario válido."
                )

            self._logger.info(f"Flat: {flat_merged}")

            # Reportes con impuestos
            if name_report in self.list_tax_reports:
                self._logger.info("Flat pagos sabana")
                flat_merged = self._get_list_headers(flat_merged)

            self._logger.info(f"Flat: {flat_merged}")

        df_conciliacion = pd.DataFrame(flat_merged)
        self._logger.info(f"df_sat: {df_conciliacion.columns}")

        if "impuestos" in df_conciliacion.columns:
            df_conciliacion = df_conciliacion.drop(
                columns=["impuestos"], errors="ignore"
            )

        dinamic_headers: list[str] = []
        if name_report == "Nomina_Sabana" or name_report in self.list_tax_reports:
            dinamic_headers = await self._validate_dinamic_headers_by_nomina(
                df=df_conciliacion, report_type=report_type
            )

        self._logger.info(f"Registros de df_conciliacion: {df_conciliacion.shape[0]}")
        self._logger.info(f"Cantidad total de CFDI obtenidos de ERP: {total_erp_cfdis}")

        for col in df_conciliacion.columns:
            if df_conciliacion[col].dtype == "object":
                df_conciliacion[col] = df_conciliacion[col].fillna("-")

        await self._save_redis(
            df=df_conciliacion,
            report_function=funcion,
            pivot_header_strategy=self._pivote,  # type: ignore
            is_fiscal=is_fiscal,
        )

        if self._filter == RequestsFilters.FILTER_SAT_NO_ERP_PERIODO:
            await self.validate_project_type_for_reporting()

        self._logger.info(f"Headers Dataframe SAT: {df_conciliacion.columns.tolist()}")

        return dinamic_headers

    async def _save_redis(
        self,
        df: pd.DataFrame,
        report_function: str,
        pivot_header_strategy: PivoteKHeader,
        is_fiscal: bool,
    ) -> None:
        if isinstance(pivot_header_strategy, str):
            pivot_header_strategy = PivoteKHeader[pivot_header_strategy]

        if is_fiscal and self._filter == RequestsFilters.FILTER_SAT_ERP:
            redis_key = self._redis_keys.get_sat_erp_redis_key()
        elif self._filter == RequestsFilters.FILTER_SAT_ERP:
            redis_key = self._redis_keys.get_sat_erp_strategy_redis_key(
                strategy=pivot_header_strategy
            )
        elif self._filter == RequestsFilters.FILTER_SAT_NO_ERP_PERIODO:
            redis_key = self._redis_keys.get_sat_no_erp_periodo_key()
        elif (
            is_fiscal and self._filter == RequestsFilters.FILTER_SHEETS
        ) or self._filter == RequestsFilters.FILTER_SHEETS:
            redis_key = self._redis_keys.get_sat_sheets_key(funcion=report_function)
        elif self._filter == RequestsFilters.FILTER_FISCAL:
            redis_key = self._redis_keys.get_sat_erp_strategy_redis_key(
                strategy=pivot_header_strategy
            )
        else:
            self._airflow_fail_exception.handle_and_store_exception(
                f"Filtro no soportado: {self._filter.value} para el proyecto: {self._project_id_str}"
            )

        buffer_df: BytesIO = self._redis.set_parquet(df=df)
        self._redis.set(
            key=redis_key,
            value=buffer_df,
        )

        self._logger.info(f"Guardando en Redis: {redis_key}")

    async def _validate_sat_report(self, report_type: ReportCatalog) -> bool:
        redis_key = self._redis_keys.get_sat_erp_redis_key()

        df_exclude_uuids: pd.DataFrame | None = self._redis.get_df(redis_key=redis_key)

        if df_exclude_uuids is None:
            return False

        strategies = report_type.strategies

        uuids = df_exclude_uuids.get(strategies["uuid"], pd.Series([]))

        if uuids is None or uuids.empty:
            return False

        return True

    async def _validate_dinamic_headers_by_nomina(
        self, df: pd.DataFrame, report_type: ReportCatalog
    ) -> list[str]:
        header_config = report_type.headers
        headers_sat = df.columns.tolist()

        dinamic_headers: list[str] = [
            header for header in headers_sat if header not in header_config.keys()
        ]

        dinamic_headers = order_headers_by_nomina(headers=dinamic_headers)

        self._logger.error(f"Dinamic headers: {dinamic_headers}")

        return dinamic_headers

    def _get_list_headers(self, flat_merged: list[dict[str, dict]]) -> list[dict]:
        return [fila for row in flat_merged for fila in procesar_impuestos(row)]

    async def validate_project_type_for_reporting(self) -> None:
        """
        Concatenates ERP_SAT and SAT_NO_ERP DataFrames for "Clientes", "Fiscal", or "Empleados" projects,
        creating a unified data source for the final report.

        This function retrieves the project configuration from the database.
        If the project type is "unitario" or "proveedores", the process is skipped.
        Otherwise, it loads the ERP_SAT and SAT_NO_ERP DataFrames from Redis, concatenates them,
        applies `drop_duplicates()`, and saves the resulting DataFrame back to Redis.

        Args:
            None (uses internal attributes: self._tipo_reporte, self._project_id_str)

        Returns:
            None

        Raises:
            KeyError: If the project is not found in the database.
            ValueError: If either DataFrame (df_sat_no_erp_periodo or df_erp_sat) is None.
        """

        project: Project | None = await PROJECT_DAO.get_by_id(
            ObjectId(self._project_id_str)
        )

        if project is None:
            self._airflow_fail_exception.handle_and_store_exception(
                f"Proyecto no encontrado con ID: {self._project_id_str}"
            )

        project_type: str = project.project_type

        if (
            project_type not in ["Clientes", "Fiscal", "Empleados"]
        ) or self._tipo_reporte == "unitario":
            self._logger.info(
                f"El tipo de proyecto es : {project_type}, se salta la validación"
            )
            return

        self._logger.info(
            f"El tipo de proyecto es : {project_type}, se hace concat de los DF para el reporte"
        )
        redis_key_erp = self._redis_keys.get_sat_erp_redis_key()

        df_erp_sat: pd.DataFrame | None = self._redis.get_df(redis_key=redis_key_erp)

        if df_erp_sat is None:
            self._airflow_fail_exception.handle_and_store_exception(
                f"DataFrame no encontrado con la clave: {redis_key_erp}"
            )

        self._logger.info(f"DataFrame ERP SAT: {df_erp_sat}")
        self._logger.info(f"DataFrame ERP SAT - numero registros: {len(df_erp_sat)}")

        redis_key_sat_no_erp_periodo = self._redis_keys.get_sat_no_erp_periodo_key()

        df_sat_no_erp_periodo: pd.DataFrame | None = self._redis.get_df(
            redis_key=redis_key_sat_no_erp_periodo
        )

        if df_sat_no_erp_periodo is None:
            self._airflow_fail_exception.handle_and_store_exception(
                f"DataFrame no encontrado con la clave: {redis_key_sat_no_erp_periodo}"
            )

        self._logger.info(f"DataFrame SAT no ERP periodo: {df_sat_no_erp_periodo}")
        self._logger.info(
            f"DataFrame SAT no ERP periodo - numero registros: {len(df_sat_no_erp_periodo)}"
        )

        df_erp_sat = pd.concat([df_erp_sat, df_sat_no_erp_periodo], axis=0)

        for col in df_erp_sat.columns:
            if df_erp_sat[col].apply(lambda x: isinstance(x, (list, dict))).any():
                df_erp_sat[col] = df_erp_sat[col].apply(
                    lambda x: str(x) if isinstance(x, (list, dict)) else x
                )

        df_erp_sat = df_erp_sat.drop_duplicates()

        self._logger.info(f"DataFrame ERP SAT concatenado: {df_erp_sat}")
        self._logger.info(
            f"DataFrame ERP SAT concatenado - numero registros: {len(df_erp_sat)}"
        )

        buffer_df: BytesIO = self._redis.set_parquet(df=df_erp_sat)
        self._redis.set(
            key=redis_key_erp,
            value=buffer_df,
        )
