from enum import Enum

from k_link.db.core import ObjectId
from k_link.extensions.conciliation_type import ConciliationType
from k_link.extensions.pivot_k import PivoteKHeader
from loggerk import LoggerK


class Keys(Enum):
    ERP = "erp"
    SAT_ERP = "sat_erp"
    SAT_NO_ERP_PERIODO = "sat_no_erp_periodo"
    SAT_SHEETS = "sat_sheets"
    LIST_HEADERS = "list_headers"
    DYNAMIC = "dynamic"
    PIVOTS = "pivot"
    VALIDATIONS = "validation"
    VALIDATION_META_DATA = "validation_meta_data"
    OPERATIONS = "operation"
    LABELS = "label"
    SAT = "sat"
    METRICS = "metrics"
    FORMAT_CONFIG = "format_config_pivot_table"
    EXCEL_BUFFER = "excel_buffer"
    INDICATORS = "indicators"
    EXCEPTIONS = "exceptions"
    DYNAMIC_HEADERS = "dynamic_headers"
    DATAFRAME_GROUP = "dataframe_group"
    DATAFRAME_PIVOT = "dataframe_pivot"
    WEBHOOKS_CONCILIATION_REQUEST = "WEBHOOKS_CONCILIATION_REQUEST"


class RedisKeys:
    _logger: LoggerK

    def __init__(
        self,
        run_id: str,
        project_id_str: str,
        month: int,
        year: int,
        conciliation_type: ConciliationType,
    ) -> None:
        self._logger = LoggerK(self.__class__.__name__)
        self.run_id: str = run_id
        self.project_id_str: str = project_id_str
        self.project_id = ObjectId(project_id_str)
        self.month: int = month
        self.year: int = year
        self._conciliation_type: ConciliationType = conciliation_type

    @property
    def base_key(self) -> str:
        return "_".join(
            [
                self.run_id,
                self.project_id_str,
                self._conciliation_type.value.lower(),
                str(self.month),
                str(self.year),
            ]
        )

    def get_exceptions_redis_key(self) -> str:
        return self._compose_key(f"{Keys.EXCEPTIONS.value}")

    def get_metrics_redis_key(self) -> str:
        return self._compose_key(Keys.METRICS.value)

    def get_erp_redis_key(self) -> str:
        return self._compose_key(Keys.ERP.value)

    def get_erp_validos_redis_key(self, strategy: PivoteKHeader) -> str:
        return self._compose_key(f"{Keys.ERP.value}_{strategy.value.lower()}_validos")

    def get_erp_data_source_redis_key(self, datasource: str) -> str:
        return self._compose_key(f"{Keys.ERP.value}_{datasource}_{self.base_key}")

    def get_sat_erp_redis_key(self) -> str:
        return self._compose_key(Keys.SAT_ERP.value)

    def get_sat_erp_strategy_redis_key(self, strategy: PivoteKHeader) -> str:
        return self._compose_key(
            f"{Keys.SAT_ERP.value}_{strategy.value.lower()}_{self.base_key}"
        )

    def get_sat_erp_strategy_sheets_redis_key(
        self, strategy: PivoteKHeader, funcion: str
    ) -> str:
        return self._compose_key(
            f"{Keys.SAT_ERP.value}_{strategy.value.lower()}_{funcion}"
        )

    def get_sat_no_erp_periodo_key(self) -> str:
        return self._compose_key(Keys.SAT_NO_ERP_PERIODO.value)

    def get_sat_no_erp_periodo_sheets_key(self, funcion) -> str:
        return self._compose_key(f"{Keys.SAT_NO_ERP_PERIODO.value}_{funcion}")

    def get_sat_sheets_key(self, funcion) -> str:
        return self._compose_key(f"{Keys.SAT_SHEETS.value}_{funcion}")

    def get_sat_erp_meta_key(self) -> str:
        return self._compose_key(f"{Keys.SAT_ERP.value}_meta")

    def get_sat_erp_meta_cancel_key(self) -> str:
        return self._compose_key(f"{Keys.SAT_ERP.value}_meta_cancelada")

    def _compose_key(self, key: str) -> str:
        return f"{key}_{self.base_key}"

    def get_headers_erp_list_key(self) -> str:
        return self._compose_key(f"{Keys.LIST_HEADERS.value}_{Keys.ERP.value}")

    def get_headers_erp_final_list_key(self) -> str:
        return self._compose_key(f"{Keys.LIST_HEADERS.value}_{Keys.ERP.value}_final")

    def get_headers_pivot_list_key(self) -> str:
        return self._compose_key(f"{Keys.LIST_HEADERS.value}_{Keys.PIVOTS.value}")

    def get_headers_validation_list_key(self) -> str:
        return self._compose_key(f"{Keys.LIST_HEADERS.value}_{Keys.VALIDATIONS.value}")

    def get_headers_validation_meta_data_list_key(self) -> str:
        return self._compose_key(
            f"{Keys.LIST_HEADERS.value}_{Keys.VALIDATION_META_DATA.value}"
        )

    def get_headers_operation_list_key(self) -> str:
        return self._compose_key(f"{Keys.LIST_HEADERS.value}_{Keys.OPERATIONS.value}")

    def get_headers_label_list_key(self) -> str:
        return self._compose_key(f"{Keys.LIST_HEADERS.value}_{Keys.LABELS.value}")

    def get_headers_sat_list_key(self) -> str:
        return self._compose_key(f"{Keys.LIST_HEADERS.value}_{Keys.SAT.value}")

    def get_headers_report_type_list_key(self, name_report_type: str) -> str:
        return self._compose_key(
            f"{Keys.LIST_HEADERS.value}_report_type_{name_report_type}"
        )

    def get_pivot_table_format_config_key(self) -> str:
        return self._compose_key(f"{Keys.FORMAT_CONFIG.value}")

    def get_excel_buffer_key(self) -> str:
        return self._compose_key(f"{Keys.EXCEL_BUFFER.value}")

    def get_indicators_redis_key(self, indicator_name: str) -> str:
        return self._compose_key(f"{Keys.INDICATORS.value}_{indicator_name}")

    def get_dynamic_headers_redis_key(self) -> str:
        return self._compose_key(f"{Keys.DYNAMIC_HEADERS.value}")

    def get_dataframe_group_redis_key(self, group_name: str) -> str:
        return self._compose_key(f"{Keys.DATAFRAME_GROUP.value}_{group_name}")

    def get_dataframe_pivot_redis_key(self, pivot_name: str) -> str:
        return self._compose_key(f"{Keys.DATAFRAME_PIVOT.value}_{pivot_name}")

    @property
    def redis_key_conciliation_status(self) -> str:
        return self._compose_key(Keys.WEBHOOKS_CONCILIATION_REQUEST.value)
