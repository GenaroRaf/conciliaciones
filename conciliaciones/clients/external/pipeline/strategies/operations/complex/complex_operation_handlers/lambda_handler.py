import numpy as np  # noqa: F401
import pandas as pd
from k_link.extensions.pipeline import LambdaConfig, Operation
from k_link.extensions.report_config import HeaderConfig, OrigenColumna, TipoDato
from loggerk import LoggerK

from conciliaciones.clients.external.pipeline.utils.expresion_components_handler import (
    BaseExpressionComponentHandler,
)
from conciliaciones.clients.external.pipeline.utils.operations import OperationUtils


class LambdaHandler(BaseExpressionComponentHandler):
    """Handler class for Lambda operations.

    Attributes:
        operation (Operation): The base operation configuration.
        lambda_config (LambdaConfig): The lambda specific configuration.
        df (DataFrame): The input DataFrame to apply operations on.
    """

    def __init__(
        self, df: pd.DataFrame, operation: Operation, lambda_config: LambdaConfig
    ) -> None:
        super().__init__(df, lambda_config.expression, lambda_config.components)
        self._logger = LoggerK(self.__class__.__name__)
        self._temp_col_name: str = operation.name
        self._operation: Operation = operation
        self._lambda_config: LambdaConfig = lambda_config
        self._operation_utils = OperationUtils(
            df_aux=df, operation_config=self._operation
        )

    def apply_lambda_operation(self) -> tuple[pd.DataFrame, HeaderConfig]:
        """
        Applies a custom lambda expression or dynamic operation to the DataFrame.

        This function evaluates a lambda or general Python expression defined in the operation
        configuration ('_lambda_config'). It prepares the DataFrame columns, builds the execution
        context with libraries (NumPy, Pandas) and optional custom variables, and then applies the
        evaluated expression to generate a new column in the DataFrame.

        If the expression starts with 'lambda', it is executed via 'DataFrame.apply()' along the
        specified axis. Otherwise, it is directly evaluated with 'eval()' using the prepared context.

        Args:
            None (uses internal attributes: self._df, self._lambda_config, self._operation)

        Returns:
            tuple[pd.DataFrame, HeaderConfig]:
                A tuple containing:
                - The modified DataFrame with the newly calculated column.
                - A HeaderConfig object describing the resulting column metadata.

        Raises:
            ValueError: If the evaluated expression is not a valid lambda function.
            Exception: If the expression evaluation or application fails.
        """
        self._logger.info("Applying lambda operation")

        header_operation: HeaderConfig = HeaderConfig(
            nombre=self._operation.name,
            configuracion_tipo_dato=TipoDato.TEXTO,
            origen=OrigenColumna.DIFF,
            mostrar_reporte=True,
        )

        if self._lambda_config.components:
            query, missing_headers = self._format_expression()
        else:
            query = self._lambda_config.expression
            missing_headers = []

        if not query:
            self._logger.error(
                f"No se encontró expresión válida. Headers faltantes: {missing_headers}"
            )
            return self._df, header_operation

        aux_df = self._df.copy()
        aux_df = self._operation_utils.prepare_cols_for_operation(
            aux_df, self.query_headers, query=query
        )

        context: dict = {
            "np": np,
            "pd": pd,
            "df": aux_df,
            **(self._lambda_config.context or {}),
        }

        try:
            if query.strip().startswith("lambda"):
                func = eval(query, context)  # noqa: S307
                if not callable(func):
                    raise ValueError(
                        "La expresión evaluada no es una función lambda válida."
                    )

                axis = (
                    self._lambda_config.axis
                    if self._lambda_config.axis in [0, 1]
                    else 1
                )
                result_series = aux_df.apply(func, axis=axis)  # type: ignore
            else:
                result_series = eval(query, context)  # noqa: S307

            self._df[self._operation.name] = result_series

        except Exception as e:
            self._logger.error(f"Error evaluando/aplicando lambda: {e}")
            return self._df, header_operation

        header_operation = self._operation_utils.get_header_config_operation(
            series=result_series
        )

        return self._df, header_operation
