import pandas as pd
from k_link.extensions.pipeline import (
    DateConfig,
    DateType,
    Operation,
)
from k_link.extensions.report_config import HeaderConfig, OrigenColumna, TipoDato
from loggerk import LoggerK
from pandas import DataFrame, DateOffset

from conciliaciones.clients.external.pipeline.utils.dates import normalize_to_utc
from conciliaciones.clients.external.pipeline.utils.operations import OperationUtils


class DateOperationHandler:
    """
    Handler class for Date operations.

    Attributes:
        operation (Operation): The base operation configuration.
        date_config (DateConfig): The date specific configuration.
        df (DataFrame): The input DataFrame to apply operations on.
    """

    def __init__(
        self,
        operation: Operation,
        date_config: DateConfig,
        df: pd.DataFrame,
    ) -> None:
        self._logger = LoggerK(self.__class__.__name__)
        self._operation: Operation = operation
        self._date_config: DateConfig = date_config
        self._df: DataFrame = df
        self._operation_utils = OperationUtils(
            df_aux=df, operation_config=self._operation
        )

    def apply_date_operation(self) -> tuple[DataFrame, HeaderConfig]:
        """
        Applies a date operation (addition or subtraction by days, months, or years) to a DataFrame column.

        This function normalizes the source date column to UTC, determines whether the operation
        should use a numeric value or another column as reference, applies the specified time delta,
        and removes timezone information for compatibility with reporting tools like Excel.

        Args:
            None (uses internal attributes: self._df, self._date_config, self._operation)

        Returns:
            tuple[pd.DataFrame, HeaderConfig]:
                A tuple containing:
                - The modified DataFrame with the new calculated date column.
                - A HeaderConfig object describing the resulting column metadata.

        Raises:
            KeyError: If the origin column or reference column is not found in the DataFrame.
            ValueError: If an invalid date type is provided.
        """
        self._logger.info("Applying date operation")

        header_config: HeaderConfig = HeaderConfig(
            nombre=self._operation.name,
            configuracion_tipo_dato=TipoDato.TEXTO,
            origen=OrigenColumna.DIFF,
            mostrar_reporte=True,
        )

        if self._date_config.origin_column not in self._df.columns:
            self._logger.error(
                f"Origin column '{self._date_config.origin_column}' not found in DataFrame"
            )
            return self._df, header_config

        column_name: str = self._date_config.origin_column
        series: pd.Series = self._df[column_name]

        delta: pd.Timedelta | pd.DateOffset | pd.Series | None = None
        number_series: int | pd.Series

        # Asegurar que sean datetime
        series = pd.to_datetime(series, errors="coerce")

        series = normalize_to_utc(series=series)

        if isinstance(self._date_config.value_or_column, str):
            if self._date_config.value_or_column not in self._df.columns:
                self._logger.error(
                    f"Origin column '{self._date_config.origin_column}' not found in DataFrame"
                )
                return self._df, header_config
            number_series = self._df[self._date_config.value_or_column]
        else:
            number_series = self._date_config.value_or_column

        match self._date_config.date_type:
            case DateType.DAY:
                delta = pd.to_timedelta(number_series, unit="D")
            case DateType.MONTH:
                if isinstance(number_series, pd.Series):
                    delta = number_series.apply(lambda x: DateOffset(months=x))
                else:
                    delta = DateOffset(months=number_series)
            case DateType.YEAR:
                if isinstance(number_series, pd.Series):
                    delta = number_series.apply(lambda x: DateOffset(years=x))
                else:
                    delta = DateOffset(years=number_series)

        if delta is None:
            self._logger.info("Date type not valid")
            result_series = self._df[column_name]
        else:
            result_series = series + delta  # type: ignore

            # Quitar timezone, no permitida en excel
            if hasattr(result_series.dtype, "tz"):
                result_series = result_series.dt.tz_convert(None)

            result_series = result_series.dt.date

        header_config: HeaderConfig = self._operation_utils.get_header_config_operation(
            series=result_series
        )

        self._df[self._operation.name] = result_series

        return self._df, header_config
