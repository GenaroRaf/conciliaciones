import datetime
import re
import uuid
from enum import Enum

import pandas as pd
from k_link.extensions.report_config import HeaderConfig, OrigenColumna, TipoDato
from k_link.extensions.pipeline import Operation
from k_link.extensions.report_config import TipoDato
from loggerk import LoggerK
from pandas import DataFrame, Series

# Patrón para ISO 8601 con Z al final (UTC)
iso8601_pattern = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$"


class KnowTypes(Enum):
    DATETIME = [
        str(dt)
        for dt in [
            datetime.datetime,
            datetime.date,
            datetime.time,
            pd.Timestamp,
            pd.DatetimeTZDtype,
        ]
    ]
    TIMEDELTA = [
        str(dt)
        for dt in [
            datetime.timedelta,
            pd.Timedelta,
            pd.TimedeltaIndex,
        ]
    ]
    NUMERIC = [
        str(dt)
        for dt in [
            int,
            float,
            pd.Int8Dtype,
            pd.Int16Dtype,
            pd.Int32Dtype,
            pd.Int64Dtype,
            pd.UInt8Dtype,
            pd.UInt16Dtype,
            pd.UInt32Dtype,
            pd.UInt64Dtype,
            pd.Float32Dtype,
            pd.Float64Dtype,
        ]
    ]
    TEXT = [str(str)]


class OperationUtils:
    def __init__(
        self, df_aux: DataFrame, operation_config: Operation
    ) -> None:
        self._logger = LoggerK(self.__class__.__name__)

        self._df: DataFrame = df_aux
        self._operation: Operation = operation_config

        self._temp_col_name = operation_config.name

    def prepare_cols_for_operation(
        self, aux_df: pd.DataFrame, headers_in_query: list[str], query: str
    ) -> DataFrame:
        for col in headers_in_query:
            types_in_col = self.get_types_in_col(aux_df[col][pd.notna(aux_df[col])])
            dtype = self.get_dtype(types_in_col)

            self._logger.info(f"Type: {dtype}")

            if ".dt" in query:
                self._logger.info(
                    f"Forzando conversión a datetime para columna '{col}' por uso de .dt en expresión."
                )
                dtype = KnowTypes.DATETIME
                self._df[col] = pd.to_datetime(aux_df[col], errors="coerce")
                self._df[col] = self._df[col].dt.strftime("%Y-%m-%dT%H:%M:%SZ")

            if dtype == KnowTypes.DATETIME:
                aux_df[col] = pd.to_datetime(aux_df[col], errors="coerce")
            elif dtype == KnowTypes.NUMERIC:
                aux_df[col] = pd.to_numeric(aux_df[col], errors="coerce").fillna(value=0.0)
            elif dtype == KnowTypes.TEXT:
                aux_df[col] = aux_df[col].fillna("").astype(str)

        return aux_df

    def convert_timedelta_to_days(self, aux_df: pd.DataFrame) -> DataFrame:
        dtype = self.get_dtype(self.get_types_in_col(aux_df[self._temp_col_name]))

        if dtype == KnowTypes.TIMEDELTA:
            # extract days from timedelta
            aux_df[self._operation.name] = aux_df[
                self._operation.name
            ].dt.days

        return aux_df

    def get_types_in_col(self, col: pd.Series) -> list[str]:
        lista = col.map(
            lambda x: (
                str(type(x))
                if type(x) != str
                else (str(str) if not self.es_fecha_iso(x) else str(datetime.datetime))
            )
        ).unique()
        return list(lista)

    def es_fecha_iso(self, texto):
        return bool(re.match(iso8601_pattern, texto))

    def get_dtype(self, types_in_col: list[str]) -> KnowTypes:
        if any(dt in types_in_col for dt in KnowTypes.DATETIME.value):
            return KnowTypes.DATETIME
        if any(dt in types_in_col for dt in KnowTypes.TIMEDELTA.value):
            return KnowTypes.TIMEDELTA
        if any(dt in types_in_col for dt in KnowTypes.NUMERIC.value):
            return KnowTypes.NUMERIC
        if any(dt in types_in_col for dt in KnowTypes.TEXT.value):
            return KnowTypes.TEXT
        return KnowTypes.NUMERIC

    def detect_column_type(self, series: pd.Series) -> TipoDato:
        if pd.api.types.is_numeric_dtype(series):
            return TipoDato.NUMERO
        if pd.api.types.is_bool_dtype(series):
            return TipoDato.BOOLEANO
        if pd.api.types.is_datetime64_any_dtype(series):
            return TipoDato.FECHA
        return TipoDato.TEXTO

    def get_header_config_operation(self, series: Series) -> HeaderConfig:
        tipo_col: TipoDato = self.detect_column_type(
            series=series
        )
        return HeaderConfig(
            nombre=self._operation.name,
            configuracion_tipo_dato=tipo_col,
            origen=OrigenColumna.DIFF,
            mostrar_reporte=True,
        )
