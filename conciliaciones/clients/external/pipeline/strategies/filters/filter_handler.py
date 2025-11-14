from k_link.extensions.pipeline import Filter
from loggerk import LoggerK
from pandas import DataFrame

from conciliaciones.clients.external.pipeline.utils.expresion_components_handler import (
    BaseExpressionComponentHandler,
)


class FilterHandler(BaseExpressionComponentHandler):
    def __init__(self, df: DataFrame, filter_config: Filter) -> None:
        super().__init__(
            df,
            filter_config.clause,
            filter_config.components,
        )
        self._logger = LoggerK(self.__class__.__name__)

    def apply_filter(self) -> DataFrame:
        query, missing_headers = self._format_expression()

        if query == "":
            self._logger.error(
                f"Headers not found in DataFrame for filter expression: {missing_headers}. Filter not aplied"
            )
            return self._df

        filtered_df = self._df.query(query)
        return filtered_df
