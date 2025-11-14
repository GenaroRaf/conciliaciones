from enum import Enum

from k_link.db.core import ObjectId
from k_link.db.daos import ProjectDAO
from k_link.db.models import Project, ReportCatalog
from k_link.extensions.conciliation_type import ConciliationType
from k_link.extensions.pivot_k import PivoteKHeader
from k_link.extensions.report_config import KRConfig
from k_link.utils.pydantic_types import Date
from loggerk import LoggerK
from pandas import DataFrame

from conciliaciones.utils.completion_handler.airflow_contex_exception import (
    AirflowContexException,
)
from conciliaciones.utils.data.normalize import normalize_date
from conciliaciones.utils.redis.redis_keys import RedisKeys
from conciliaciones.utils.redis.redis_storage import RedisStorage

pivot_map = {
    PivoteKHeader.UUID: "uuids",
    PivoteKHeader.SERIE_FOLIO: "serieFolio",
    PivoteKHeader.FOLIO: "folios",
}

rfc_field_map = {
    "Clientes": "rfcEmisor",
    "Proveedores": "rfcReceptor",
}


class RequestsFilters(Enum):
    FILTER_SAT_ERP = "filter_sat_erp"
    FILTER_SAT_NO_ERP_PERIODO = "filter_sat_no_erp_periodo"
    FILTER_SHEETS = "filter_sheets"
    FILTER_FISCAL = "filter_fiscal"


class KReportsFilter:
    def __init__(  # noqa: PLR0913
        self,
        run_id: str,
        project_id_str: str,
        year: int,
        month: int,
        filter: RequestsFilters,
        conciliation_type: ConciliationType,
    ) -> None:
        self._project_id_str: str = project_id_str
        self._year: int = year
        self._month: int = month
        self._filter: RequestsFilters = filter
        self._conciliation_type = conciliation_type

        self._logger = LoggerK(self.__class__.__name__)
        self._redis = RedisStorage()
        self._redis_key = RedisKeys(
            run_id=run_id,
            project_id_str=project_id_str,
            year=year,
            month=month,
            conciliation_type=conciliation_type,
        )
        self._airflow_fail_exception: AirflowContexException = AirflowContexException(
            run_id=run_id,
            project_id=project_id_str,
            year=year,
            month=month,
            conciliation_type=conciliation_type,
        )

        self._project_dao = ProjectDAO()

    async def get_filter(
        self,
        report_type: ReportCatalog | None,
        request_config: KRConfig,
        pivot_header_strategy: PivoteKHeader,
        rfc: str,
        is_fiscal: bool = False,
    ) -> dict:
        self._logger.info(f"Filtro utilizado: {self._filter.value}")

        if isinstance(pivot_header_strategy, str):
            pivot_header_strategy = PivoteKHeader[pivot_header_strategy]

        if self._filter == RequestsFilters.FILTER_SAT_ERP:
            redis_key = self._redis_key.get_erp_validos_redis_key(
                strategy=pivot_header_strategy,
            )

            return await self._get_sat_erp(
                request_config=request_config,
                redis_key=redis_key,
                pivot_header_strategy=pivot_header_strategy,
                rfc=rfc,
            )
        if self._filter == RequestsFilters.FILTER_SAT_NO_ERP_PERIODO and report_type:
            redis_key = self._redis_key.get_sat_erp_redis_key()

            return await self._get_sat_no_erp_periodo(
                request_config=request_config,
                redis_key=redis_key,
                report_type=report_type,
                rfc=rfc,
            )
        if self._filter == RequestsFilters.FILTER_SHEETS:
            redis_key = self._redis_key.get_erp_validos_redis_key(
                strategy=pivot_header_strategy,
            )

            return await self._get_sat_erp(
                request_config=request_config,
                pivot_header_strategy=pivot_header_strategy,
                redis_key=redis_key,
                rfc=rfc,
            )
        if self._filter == RequestsFilters.FILTER_FISCAL:
            return await self._get_sat_fiscal(
                rfc=rfc,
            )
        self._airflow_fail_exception.handle_and_store_exception(
            f"Filtro no soportado: {self._filter.value} para el proyecto: {self._project_id_str}"
        )

    async def _get_sat_erp(
        self,
        request_config: KRConfig,
        pivot_header_strategy: PivoteKHeader,
        redis_key: str,
        rfc: str,
    ):
        redis_validos: DataFrame | None = self._redis.get_df(redis_key=redis_key)

        if redis_validos is None:
            self._airflow_fail_exception.handle_and_store_exception(
                f"No hay información para el DataFrame con clave {redis_key}"
            )

        self._logger.info(f"Validos: {redis_validos}")

        validos_list = redis_validos.iloc[:, 0].tolist()  # type: ignore

        seen = set()
        validos_list = [
            elemento.upper()
            for elemento in validos_list
            if isinstance(elemento, str)
            and not (elemento.upper() in seen or seen.add(elemento.upper()))
        ]
        validos_num = len(validos_list)

        self._logger.info(f"Total validos {pivot_header_strategy.value}: {validos_num}")
        self._logger.info(
            f"Total registros unicos con {pivot_header_strategy.value}: {len(set(validos_list))}",
        )

        pivot_value = pivot_map.get(pivot_header_strategy)

        if pivot_value is None:
            self._airflow_fail_exception.handle_and_store_exception(
                f"Clave {pivot_header_strategy.value} no encontrada en pivot_map para el proyecto: {self._project_id_str}"
            )

        filters: dict = await self._filter_emitidas(rfc=rfc)

        filters = {
            **filters,
            pivot_value: validos_list,
        }

        return await self._apply_request_config_filters(filters, request_config)

    async def _get_sat_no_erp_periodo(
        self,
        report_type: ReportCatalog,
        request_config: KRConfig,
        redis_key: str,
        rfc: str,
    ):
        df_exclude_uuids: DataFrame | None = self._redis.get_df(redis_key=redis_key)

        if df_exclude_uuids is None:
            self._airflow_fail_exception.handle_and_store_exception(
                f"No hay información para el DataFrame con clave {redis_key}"
            )

        filter_date: Date = normalize_date(year=self._year, month=self._month)

        if self._conciliation_type != ConciliationType.ACCUMULATED:
            start_date = filter_date.start_of_month.date_string
            end_date = filter_date.end_of_month.date_string
        else:
            start_date = filter_date.start_of_year.date_string
            end_date = filter_date.today().date_string

        strategies = report_type.strategies

        if strategies is None:
            self._airflow_fail_exception.handle_and_store_exception(
                f"El ReportType con el id: {report_type.id} no tiene estrategias definidas"
            )

        filters: dict = await self._filter_emitidas(rfc=rfc)

        raw_uuids = df_exclude_uuids[strategies["uuid"]].dropna().tolist()  # type: ignore

        seen = set()
        unique_uuids = [
            uuid.upper()
            for uuid in raw_uuids
            if isinstance(uuid, str)
            and not (uuid.upper() in seen or seen.add(uuid.upper()))
            and uuid != "nan"
        ]

        filters = {
            **filters,
            "startDate": start_date,
            "endDate": end_date,
            "notUuids": unique_uuids,
        }

        return await self._apply_request_config_filters(filters, request_config)

    async def _get_sat_fiscal(
        self,
        rfc: str,
    ) -> dict:
        filter_date: Date = normalize_date(year=self._year, month=self._month)
        start_date = filter_date.start_of_month.date_string
        end_date = filter_date.end_of_month.date_string

        filters: dict = await self._filter_emitidas(rfc=rfc)

        return {
            **filters,
            "startDate": start_date,
            "endDate": end_date,
        }

    async def _apply_request_config_filters(
        self,
        filters: dict,
        request_config: KRConfig,
    ):
        if request_config and request_config.required is not None:
            for req in request_config.required:
                if req is None:
                    continue
                for k, v in req.items():  # Iterar sobre clave y valor correctamente
                    if (
                        k in filters
                        and isinstance(filters[k], list)
                        and isinstance(v, list)
                    ):
                        filters[k].extend(v)  # Si ya existe, agregar elementos
                    else:
                        filters[k] = v  # Si no existe, asignarlo directamente

        return filters

    async def _filter_emitidas(self, rfc: str):
        project: Project | None = await self._project_dao.get_by_id(
            item_id=ObjectId(self._project_id_str),
        )

        if project is None:
            self._airflow_fail_exception.handle_and_store_exception(
                f"El proyecto con el id: {self._project_id_str} no existe en la base de datos"
            )

        project_type: str = project.project_type  # type: ignore

        filters: dict = {
            **(
                {rfc_field_map[project_type]: rfc}
                if project_type in rfc_field_map
                else {}
            ),
        }

        return filters
