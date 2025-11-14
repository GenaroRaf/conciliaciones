from k_link.extensions.pipeline import (
    Operation,
    SplitExplodeConfig,
)
from k_link.extensions.report_config import HeaderConfig, OrigenColumna, TipoDato
from loggerk import LoggerK
from pandas import DataFrame

from conciliaciones.clients.external.pipeline.utils.operations import OperationUtils


class SplitExplodeHandler:
    """Handler class for Split and Explode operations.

    Attributes:
        df (DataFrame): The input DataFrame to apply operations on.
        operation (Operation): The base operation configuration.
        split_explode_config (SplitExplodeConfig): The split and explode specific configuration.
    """

    def __init__(
        self,
        df: DataFrame,
        operation: Operation,
        split_explode_config: SplitExplodeConfig,
    ) -> None:
        self._logger = LoggerK(self.__class__.__name__)
        self._df: DataFrame = df
        self._operation: Operation = operation
        self._split_explode_config: SplitExplodeConfig = split_explode_config
        self._operation_utils = OperationUtils(
            df_aux=df, operation_config=self._operation
        )

    def apply_split_explode_operation(self) -> tuple[DataFrame, HeaderConfig]:
        """
        Applies a split and explode operation to a specified column in the DataFrame.

        This function takes the origin column defined in '_split_explode_config', splits each
        string value into a list using the configured delimiter, and then expands each list element
        into separate rows (using Pandas' 'explode' method). The result is a flattened DataFrame
        where each split value occupies its own row under a new column name.

        Args:
            None (uses internal attributes: self._df, self._split_explode_config, self._operation)

        Returns:
            tuple[pd.DataFrame, HeaderConfig]:
                A tuple containing:
                - The transformed DataFrame after the split and explode operation.
                - A HeaderConfig object describing the metadata for the new column.

        Raises:
            TypeError: If the origin column contains non-string and non-null values.
            KeyError: If the origin column specified in the configuration does not exist in the DataFrame.
        """

        self._logger.info("Applying split and explode operation")

        if self._split_explode_config.origin_column not in self._df.columns:
            self._logger.error(
                f"Origin column '{self._split_explode_config.origin_column}' not found in DataFrame"
            )
            return DataFrame(), HeaderConfig(
                nombre=self._operation.name,
                configuracion_tipo_dato=TipoDato.TEXTO,
                origen=OrigenColumna.DIFF,
                mostrar_reporte=True,
            )

        series = self._df[self._split_explode_config.origin_column]
        if not series.apply(lambda x: isinstance(x, str) or x is None).all():
            raise TypeError(
                f"Column '{self._split_explode_config.origin_column}' must be string or None for split operation"
            )

        self._logger.info(
            f"Registros originales: {len(self._df[self._split_explode_config.origin_column])}"
        )

        df_expanded: DataFrame = self._df.assign(
            **{
                self._operation.name: self._df[
                    self._split_explode_config.origin_column
                ].str.split(pat=self._split_explode_config.split)
            }
        ).explode(column=self._operation.name)

        # Opcional: eliminar la columna original si ya no se necesita
        df_expanded = (
            df_expanded.drop(columns=[self._split_explode_config.origin_column])
            .reset_index(drop=True)
            .drop_duplicates()
        )

        self._logger.info(
            f"Registros finales: {len(df_expanded[self._operation.name])}"
        )

        header_config: HeaderConfig = self._operation_utils.get_header_config_operation(
            series=df_expanded[self._operation.name]
        )

        return df_expanded, header_config
