import datetime
import re
from enum import Enum

import numpy as np
import pandas as pd
from k_link.extensions.pipeline import GeneralConfig, Operation
from k_link.extensions.report_config import HeaderConfig, OrigenColumna, TipoDato
from loggerk import LoggerK

from conciliaciones.clients.external.pipeline.utils.expresion_components_handler import (
    BaseExpressionComponentHandler,
)
from conciliaciones.clients.external.pipeline.utils.operations import OperationUtils

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


class GeneralHandler(BaseExpressionComponentHandler):
    """Handler class for General operations.

    Attributes:
        operation (Operation): The base operation configuration.
        general_config (GeneralConfig): The general specific configuration.
        df (DataFrame): The input DataFrame to apply operations on.
    """

    def __init__(
        self,
        df: pd.DataFrame,
        operation: Operation,
        general_config: GeneralConfig,
    ) -> None:
        self._operation: Operation = operation
        self._general_config: GeneralConfig = general_config
        super().__init__(
            df=df,
            exp=self._general_config.expression,
            components=self._general_config.components,
        )
        self._logger = LoggerK(self.__class__.__name__)
        self._temp_col_name: str = operation.name
        self._operation_utils = OperationUtils(
            df_aux=df, operation_config=self._operation
        )

    def apply_general_operation(self) -> tuple[pd.DataFrame, HeaderConfig]:
        """
        Applies a general custom operation to the DataFrame using Python's 'eval()' with a defined context,
        creating a new calculated column.

        This function builds an expression string using the DataFrame’s headers as parameters,
        normalizes the required columns, builds the execution context with libraries (NumPy, Pandas)
        and optional custom variables, evaluates the expression with 'eval()', and fills missing
        values in the resulting column if configured.

        Args:
            None (uses internal attributes: self._df, self._general_config, self._operation)

        Returns:
            tuple[pd.DataFrame, HeaderConfig]:
                A tuple containing:
                - The modified DataFrame with the new calculated column.
                - A HeaderConfig object describing the resulting column metadata.

        Raises:
            BuildError: If the generated expression is empty.
            Exception: If an error occurs during expression evaluation.
        """
        self._logger.info("Applying general operation")

        header_operation = HeaderConfig(
            nombre=self._operation.name,
            configuracion_tipo_dato=TipoDato.TEXTO,
            origen=OrigenColumna.DIFF,
            mostrar_reporte=True,
        )

        if self._general_config.components:
            query, missing_headers = self._format_expression()
        else:
            query = self._general_config.expression
            missing_headers = []

        if query == "":
            self._logger.error(
                f"Headers not found in DataFrame for filter expression. {missing_headers}. Operation not applied"
            )
            return self._df, header_operation

        query_aux: str = query
        aux_df: pd.DataFrame = self._df.copy()

        aux_df = self._operation_utils.prepare_cols_for_operation(
            aux_df, self.query_headers, query=query
        )

        self._logger.info(f"Evaluating expression: {query_aux}")
        context: dict = {
            "np": np,
            "pd": pd,
            "df": aux_df,
            "re": re,
            **(self._general_config.context or {}),
        }

        try:
            aux_df[self._operation.name] = eval(query, context)  # noqa: S307
        except Exception as e:
            self._logger.error(f"Error the applied general operation: {e}")
            return self._df, header_operation

        aux_df = self._operation_utils.convert_timedelta_to_days(aux_df)

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
                            self._df[self._operation.name]
                            .fillna(fill_cfg)
                            .astype(float)
                        )
                elif pd.api.types.is_integer_dtype(col_dtype):
                    if fill_cfg is not None:
                        self._df[self._operation.name] = (
                            self._df[self._operation.name].fillna(fill_cfg).astype(int)
                        )
                else:
                    self._df[self._operation.name] = self._df[
                        self._operation.name
                    ].fillna(fill_cfg)

        header_operation: HeaderConfig = (
            self._operation_utils.get_header_config_operation(
                series=self._df[self._operation.name]
            )
        )

        return self._df, header_operation
