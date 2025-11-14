import re

from k_link.db.core import ObjectId
from k_link.db.daos import IndicatorTemplateDAO
from k_link.db.models import IndicatorTemplate
from k_link.extensions import ConciliationType, ReporteAsociado
from k_link.extensions.indicators import (
    IndicatorConfig,
    IndicatorType,
    MultOperation,
    OperationColumn,
    OperationIndicator,
)
from loggerk import LoggerK
from pandas import DataFrame

from conciliaciones.utils.completion_handler.airflow_contex_exception import (
    AirflowContexException,
)


class IndicatorHandler:
    def __init__(
        self,
        df: DataFrame,
        indicator_config: IndicatorConfig,
        year: int,
        month: int,
        project_id_str: str,
        run_id: str,
        conciliation_type: ConciliationType,
        extra_params: dict | None = None,
    ) -> None:
        self._logger = LoggerK(self.__class__.__name__)
        self._df: DataFrame = df
        self._indicator_config: IndicatorConfig = indicator_config
        self._extra_params = extra_params or {}
        self._indicator_dao = IndicatorTemplateDAO()
        self._sheet_constant_found = False
        self._airflow_fail_exception = AirflowContexException(
            year=year,
            month=month,
            project_id=project_id_str,
            run_id=run_id,
            conciliation_type=conciliation_type,
        )

    def apply_indicator(self) -> tuple[DataFrame, str]:
        indicator: IndicatorTemplate | None = self._indicator_dao.get_by_id_sync(
            item_id=self._indicator_config.indicator_id
        )

        if not indicator:
            self._airflow_fail_exception.handle_and_store_exception(
                f"No se encontró el indicador con ID: {self._indicator_config.indicator_id}"
            )

        # Contiene los resultados de operation_columns listo para formar el dataframe
        dataframe_result_mostrar = {}
        dataframe_result_montos_vertical = {}
        dataframe_result_montos_horizontal = {}

        # Resultados, mult y params por operation_column
        operation_results: list[float] = []
        params_dict: dict[str, str] = {}
        total_list_vertical: list[float] = []
        total_list_horizontal: list[float] = []

        operation_columns: list[OperationColumn] = indicator.operation_columns

        sheet_name: str = ""
        for operation_column, param_column in zip(
            operation_columns, self._indicator_config.column_params
        ):
            operation_results = []
            mult_operations: list[MultOperation] = []
            params_dict = {}

            operation_indicators: list[OperationIndicator] = (
                operation_column.operation_indicators
            )

            for operation in operation_indicators:
                self._logger.info(
                    f"Applying operation: {operation} with indicator ID: {self._indicator_config.indicator_id}"
                )

                expression, _format_dict, missing_headers = self._format_expression(
                    exp=operation.clause,
                    params=param_column.params,
                    constant_params=param_column.constant_params,
                    id_report_asociado=(
                        self._indicator_config.report_id
                        if self._indicator_config.report_id is not None
                        else ObjectId()
                    ),
                    reports_asociados=indicator.reportes_asociados,
                    extra_params=self._extra_params,
                )

                if expression == "":
                    self._logger.error(
                        f"Headers not found in DataFrame for filter expression: {missing_headers}. Indicator not aplied"
                    )
                    continue

                params_dict = {**params_dict, **_format_dict}

                try:
                    self._logger.info(f"Evaluating expression: {expression}")
                    result = eval(expression, {"df": self._df})

                    operation_results.append(result)
                    mult_operations.append(operation.mult_operation)
                    self._logger.info(f"Evaluated: {expression} → {result}")
                except Exception as e:
                    self._logger.error(f"Error applying operation: {e}")
                    self._airflow_fail_exception.handle_and_store_exception(
                        f"No se pudo validar la expresion: {expression} para el indicador: {self._indicator_config.indicator_id}. Error: {e}"
                    )

            if not self._sheet_constant_found:
                sheet_name = self._get_sheet_name(
                    format_dict_general=params_dict,
                    sheet_name_constant=indicator.sheet_name,
                )

            results_mostrar: list[float] = []
            results_montos_vertical: list[float] = []
            total_vertical = 0
            results_montos_horizontal: list[float] = []
            total_horizontal = 0

            cont_h = 0
            for result, mult_operation in zip(operation_results, mult_operations):
                if isinstance(result, (int, float)):
                    value_mostrar = result

                    if mult_operation.vertical != 0:
                        value_montos_vertical = result * mult_operation.vertical
                        total_vertical += value_montos_vertical
                    else:
                        value_montos_vertical = 0

                    if mult_operation.horizontal != 0:
                        value_montos_horizontal = result * mult_operation.horizontal
                        total_horizontal += value_montos_horizontal

                    else:
                        value_montos_horizontal = 0

                else:
                    value_mostrar = result

                    value_montos_vertical = 0
                    value_montos_horizontal = 0

                results_mostrar.append(value_mostrar)
                results_montos_vertical.append(value_montos_vertical)
                results_montos_horizontal.append(value_montos_horizontal)

            total_list_vertical.append(total_vertical)
            total_list_horizontal.append(total_horizontal)

            dataframe_result_mostrar[operation_column.column_name] = results_mostrar
            dataframe_result_montos_vertical[operation_column.column_name] = (
                results_montos_vertical
            )
            dataframe_result_montos_horizontal[operation_column.column_name] = (
                results_montos_horizontal
            )

            cont_h += 1

            self._logger.info(f"Total vertical: {total_list_vertical}")
            self._logger.info(f"Total horizontal: {results_montos_horizontal}")

        self.extra_params(
            indicator=indicator, params=params_dict, sheet_name=sheet_name
        )

        total_operations = 0
        if indicator.indicator_type is not IndicatorType.RESUMEN:
            # Totales verticales
            total_operations_column_montos: list[float] = self._get_total(
                dataframe_result_montos_horizontal
            )
            total_operations = sum(total_operations_column_montos)

            total_operations_column_mostrar: list[float] = self._get_total(
                dataframe_result_montos_horizontal
            )

            dataframe_result_mostrar["Total"] = total_operations_column_mostrar

        df_operation: DataFrame = self._get_df(
            indicator=indicator,
            dataframe_result=dataframe_result_mostrar,
            total=total_operations,
            total_list_vertical=total_list_vertical,
        )

        return df_operation, sheet_name

    def _get_df(
        self,
        indicator: IndicatorTemplate,
        dataframe_result: dict[str, list[float]],
        total_list_vertical: list[float],
        total: float,
    ) -> DataFrame:
        data = {}
        row_count = None  # type: ignore
        first_column = None  # type: ignore

        for custom_indicator in indicator.custom_indicators:
            if first_column is None:
                first_column: str = custom_indicator.column_name

            column_name: str = custom_indicator.column_name
            values: list[str] = custom_indicator.values

            if row_count is None:
                row_count: int = len(values)
            elif len(values) != row_count:
                self._airflow_fail_exception.handle_and_store_exception(
                    f"Longitud de valores para la columna '{column_name}' "
                    f"({len(values)}) no coincide con el número esperado de filas ({row_count})."
                )

            data[column_name] = values

        data.update(dataframe_result)
        self._logger.info(f"Data: {data}")

        try:
            df_operation: DataFrame = DataFrame(data)
        except ValueError:
            self._logger.error(
                "Las listas de datos no tienen la misma longitud. Se devuelve un DataFrame vacío."
            )
            return DataFrame()

        if indicator.indicator_type is not IndicatorType.RESUMEN:
            total_row = dict.fromkeys(df_operation.columns, "")
            total_row["Total"] = total  # type: ignore

            if first_column:
                total_row[first_column] = "Total"

            df_operation.loc[len(df_operation)] = total_row  # type: ignore

            column: int = len(indicator.custom_indicators)
            row: int = len(df_operation) - 1
            for result_total_column in total_list_vertical:
                df_operation.iat[row, column] = result_total_column
                column += 1

        self._logger.info(f"DataFrame created for indicator: \n{df_operation}")

        self._logger.info(f"Tipo df: {df_operation.dtypes}")

        return df_operation

    def extra_params(
        self, indicator: IndicatorTemplate, params: dict, sheet_name: str
    ) -> None:
        label_params: set = set()
        for operation_column in indicator.operation_columns:
            label_params.update(param for param in operation_column.params)
        used_params: set[str] = set(params.keys())

        if "{" in sheet_name and "}" in sheet_name:
            sheet_name_placeholders = set(re.findall(r"{(.*?)}", indicator.sheet_name))
            label_params.update(sheet_name_placeholders)

        extra_params: set[str] = used_params - label_params

        dict_extra_params: dict[str, str] = {
            param: params[param] for param in extra_params
        }

        if not extra_params:
            return

        if extra_params:
            self._logger.error(
                f"Extra parameters found: {dict_extra_params}. These parameters are not defined in the label configuration."
            )

    def _format_expression(
        self,
        exp: str,
        params: dict[str, str],
        constant_params: dict[str, str],
        id_report_asociado: ObjectId,
        reports_asociados: list[ReporteAsociado],
        extra_params: dict[str, str] = None,  # type: ignore
    ) -> tuple[str, dict[str, str], list]:
        format_dict: dict = {}
        if id_report_asociado:
            for reporte in reports_asociados:
                if id_report_asociado == reporte.report_id:
                    format_dict = reporte.params
                    break

        format_dict = {**format_dict, **params}

        error_header, missing_headers = self.error_headers(format_dict=format_dict)

        if error_header:
            return "", format_dict, missing_headers

        for letter, header_name in format_dict.items():
            format_dict[letter] = f'"{header_name}"'

        format_dict.update(extra_params)
        format_dict.update(constant_params)

        query: str = exp.format(**format_dict)
        return query, format_dict, missing_headers

    def error_headers(self, format_dict: dict) -> tuple[bool, list]:
        missing_headers = [
            header_name
            for letter, header_name in format_dict.items()
            if header_name not in self._df.columns
            and header_name not in self._extra_params
        ]
        if missing_headers:
            return True, missing_headers
        return False, missing_headers

    def _get_sheet_name(self, format_dict_general: dict, sheet_name_constant: str):
        parametro = re.findall(r"\{(.*?)\}", sheet_name_constant)
        if "{" in sheet_name_constant and "}" in sheet_name_constant:
            for param in parametro:
                if param in format_dict_general:
                    self._sheet_constant_found = True
                    sheet_name: str = sheet_name_constant.format(**format_dict_general)
                    return sheet_name
            return sheet_name_constant
        return sheet_name_constant

    def _get_total(self, dataframe_result: dict[str, list[float]]) -> list[float]:
        return [sum(values) for values in zip(*dataframe_result.values())]
