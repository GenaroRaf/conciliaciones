import pandas as pd
from k_link.extensions.pipeline import Operation, TextTransformConfig
from k_link.extensions.pipeline.operation_strategy.text_case_type import TextCaseType
from k_link.extensions.report_config import HeaderConfig
from loggerk import LoggerK
from pandas import DataFrame

from conciliaciones.clients.external.pipeline.utils.operations import OperationUtils


class TextTransformHandler:
    """Handler class for text transform operations.

    Attributes:
        df (DataFrame): The input DataFrame to apply operations on.
        operation (Operation): The base operation configuration.
        text_transform_config (TextTransformConfig): The text transform specific configuration.
    """

    def __init__(
        self,
        df: DataFrame,
        operation: Operation,
        text_transform_config: TextTransformConfig,
    ) -> None:
        self._logger = LoggerK(name=self.__class__.__name__)
        self._df: DataFrame = df
        self._operation: Operation = operation
        self._text_transform_config: TextTransformConfig = text_transform_config
        self._operation_utils = OperationUtils(
            df_aux=df, operation_config=self._operation
        )

    def apply_text_transform_operation(self) -> tuple[DataFrame, HeaderConfig]:
        """
        Applies a text transformation operation to a specific column in the DataFrame.

        This function transforms the text in the column specified by '_text_transform_config.origin_column'
        according to the selected text case operation (lowercase, uppercase, or capitalize). It creates a new
        column defined by 'self._operation.name' containing the transformed text values.

        Args:
            None (uses internal attributes: self._df, self._text_transform_config, self._operation)

        Returns:
            tuple[pd.DataFrame, HeaderConfig]:
                A tuple containing:
                - The modified DataFrame with the new text-transformed column.
                - A HeaderConfig object describing the resulting column metadata.

        Raises:
            ValueError: If the provided text transformation type is invalid.
            KeyError: If the origin column is not found in the DataFrame.
        """

        self._logger.info("Applying text transform operation")

        if self._text_transform_config.origin_column in self._df.columns:
            if not pd.api.types.is_string_dtype(
                arr_or_dtype=self._df[self._text_transform_config.origin_column]
            ):
                self._df[self._text_transform_config.origin_column] = self._df[
                    self._text_transform_config.origin_column
                ].astype(dtype=str)

            match self._text_transform_config.text_case:
                case TextCaseType.LOWER:
                    self._df[self._operation.name] = self._df[
                        self._text_transform_config.origin_column
                    ].str.lower()
                case TextCaseType.UPPER:
                    self._df[self._operation.name] = self._df[
                        self._text_transform_config.origin_column
                    ].str.upper()
                case TextCaseType.CAPITALIZE:
                    self._df[self._operation.name] = self._df[
                        self._text_transform_config.origin_column
                    ].str.capitalize()
                case _:
                    raise ValueError(
                        f"Invalid operation: {self._text_transform_config.text_case}"
                    )
        else:
            self._logger.error(
                f"Origin column '{self._text_transform_config.origin_column}' not found in DataFrame"
            )

        header_config: HeaderConfig = self._operation_utils.get_header_config_operation(
            series=self._df[self._operation.name]
        )

        return self._df, header_config
