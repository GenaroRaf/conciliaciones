import datetime
import re
import uuid
from enum import Enum

import numpy as np
import pandas as pd
from k_link.extensions.pipeline import Operation, SimpleOperation
from k_link.extensions.report_config import HeaderConfig, OrigenColumna, TipoDato
from loggerk import LoggerK

from conciliaciones.clients.external.pipeline.utils.expresion_components_handler import (
    BaseExpressionComponentHandler,
)

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


class OperationHandler(BaseExpressionComponentHandler):
    def __init__(
        self,
        df: pd.DataFrame,
        operation: Operation,
    ) -> None:
        self._operation: Operation = operation
        self._operation_config: SimpleOperation = operation.operation_config  # type: ignore
        super().__init__(
            df=df,
            exp=self._operation_config.expression,
            components=self._operation_config.components,
        )
        self._logger = LoggerK(self.__class__.__name__)
        self._temp_col_name = operation.name

    def apply_operation(self) -> tuple[pd.DataFrame, HeaderConfig]:
        query, missing_headers = self._format_expression()

        if query == "":
            self._logger.error(
                f"Headers not found in DataFrame for filter expression. {missing_headers}. Operation not applied"
            )

            header_operation = HeaderConfig(
                nombre=self._operation.name,
                configuracion_tipo_dato=TipoDato.TEXTO,
                origen=OrigenColumna.DIFF,
                mostrar_reporte=True,
            )
            return self._df, header_operation

        query_aux = f"{self._temp_col_name} = {query}"
        aux_df = self._df.copy()[self.query_headers]
        context: dict = {
            "np": np,
            "pd": pd,
            "df": aux_df,
            "re": re,
            **(self._operation_config.context or {}),
        }

        self._prepare_cols_for_operation(aux_df, self.query_headers)

        # Execute the query
        # Detect string concatenation pattern: {A} + '-' + {B}
        if "+" in query and "'" in query:
            # Assumes exactly two components: A and B
            if len(self._operation_config.components) == 2:
                a = self._operation_config.components[0].header
                b = self._operation_config.components[1].header
                # Replace NaN with empty string before converting to str
                aux_df[a] = aux_df[a].fillna("")
                aux_df[b] = aux_df[b].fillna("")
                aux_df[self._temp_col_name] = (
                    aux_df[a].astype(str) + "-" + aux_df[b].astype(str)
                )
            else:
                raise ValueError(
                    "String concatenation with '+' requires exactly two components."
                )
        else:
            # Execute the query normally
            aux_df.eval(expr=query_aux, inplace=True, local_dict=context)

        self._convert_timedelta_to_days(aux_df)

        # add the result to the original DataFrame
        self._df[self._operation.name] = aux_df[self._temp_col_name]

        # Apply fillna if specified in the operation config
        if getattr(self._operation, "fillna", None):
            self._logger.warning(
                f"Applying fillna with config: {self._operation.fillna}"
            )
            if self._operation.fillna:
                fill_cfg = self._operation.fillna.value
                col_dtype = self._df[self._operation.name].dtype

                if pd.api.types.is_float_dtype(col_dtype):
                    if fill_cfg is not None:
                        self._df[self._operation.name] = (
                            self._df[self._operation.name].fillna(fill_cfg).astype(int)
                        )
                else:
                    self._df[self._operation.name] = self._df[
                        self._operation.name
                    ].fillna(fill_cfg)

        # Apply fillna if specified in the operation config
        if getattr(self._operation, "fillna", None):
            self._logger.warning(
                f"Applying fillna with config: {self._operation.fillna}"
            )
            if self._operation.fillna:
                fill_cfg = self._operation.fillna.value
                col_dtype = self._df[self._operation.name].dtype

                if pd.api.types.is_float_dtype(col_dtype):
                    if fill_cfg is not None:
                        self._df[self._operation.name] = (
                            self._df[self._operation.name].fillna(fill_cfg).astype(int)
                        )
                else:
                    self._df[self._operation.name] = self._df[
                        self._operation.name
                    ].fillna(fill_cfg)

        tipo_dato = TipoDato.TEXTO

        if self._df[self._operation.name].dtype in ["int64", "float64"]:
            tipo_dato = TipoDato.NUMERO
        elif self._df[self._operation.name].dtype == "bool":
            tipo_dato = TipoDato.BOOLEANO

        header_operation: HeaderConfig = HeaderConfig(
            nombre=self._operation.name,
            configuracion_tipo_dato=tipo_dato,
            origen=OrigenColumna.DIFF,
            mostrar_reporte=True,
        )

        return self._df, header_operation

    @property
    def _temp_col_name(self) -> str:
        return self._tmp_col

    @_temp_col_name.setter
    def _temp_col_name(self, col_name: str):
        base = re.sub(r"\W|^(?=\d)", "_", col_name)
        prefix = "__temp__"
        suffix = uuid.uuid4().hex[:8]
        self._tmp_col = f"{prefix}_{base}_{suffix}"

    def _convert_timedelta_to_days(self, aux_df: pd.DataFrame):
        dtype = self._get_dtype(self._get_types_in_col(aux_df[self._temp_col_name]))

        if dtype == KnowTypes.TIMEDELTA:
            # extract days from timedelta
            aux_df[self._operation.name] = aux_df[self._operation.name].dt.days

    def _prepare_cols_for_operation(
        self, aux_df: pd.DataFrame, headers_in_query: list[str]
    ):
        for col in headers_in_query:
            types_in_col = self._get_types_in_col(aux_df[col][pd.notna(aux_df[col])])
            dtype = self._get_dtype(types_in_col)

            if ".dt" in self._operation_config.expression:
                self._logger.info(
                    f"Forzando conversión a datetime para columna '{col}' por uso de .dt en expresión."
                )
                dtype = KnowTypes.DATETIME
                self._df[col] = pd.to_datetime(aux_df[col], errors="coerce")
                self._df[col] = self._df[col].dt.strftime("%Y-%m-%dT%H:%M:%SZ")

            self._logger.info(f"Type: {dtype}")

            if dtype == KnowTypes.DATETIME:
                aux_df[col] = pd.to_datetime(aux_df[col], errors="coerce")
            elif dtype == KnowTypes.NUMERIC:
                aux_df[col] = pd.to_numeric(aux_df[col], errors="coerce")
            elif dtype == KnowTypes.TEXT:
                aux_df[col] = aux_df[col].fillna("").astype(str)

    def _get_types_in_col(self, col: pd.Series) -> list[str]:
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

    def _get_dtype(self, types_in_col: list[str]) -> KnowTypes:
        if any(dt in types_in_col for dt in KnowTypes.DATETIME.value):
            return KnowTypes.DATETIME
        if any(dt in types_in_col for dt in KnowTypes.TIMEDELTA.value):
            return KnowTypes.TIMEDELTA
        if any(dt in types_in_col for dt in KnowTypes.NUMERIC.value):
            return KnowTypes.NUMERIC
        if any(dt in types_in_col for dt in KnowTypes.TEXT.value):
            return KnowTypes.TEXT
        return KnowTypes.NUMERIC
