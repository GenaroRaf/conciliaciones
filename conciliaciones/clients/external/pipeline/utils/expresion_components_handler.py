from collections.abc import Sequence
from typing import Protocol

from k_link.extensions.pipeline import Component
from pandas import DataFrame


class ExpressionConfig(Protocol):
    @property
    def exp(self) -> str: ...

    @property
    def components(self) -> list[Component]: ...


class BaseExpressionComponentHandler:
    def __init__(
        self,
        df: DataFrame,
        exp: str,
        components: Sequence[Component],
        extra_params: dict | None = None,
    ) -> None:
        self._df = df
        self._exp = exp
        self._components = components
        self._extra_params = extra_params or {}

    def _format_expression(self) -> tuple[str, list]:
        # Create base format dict with component headers
        format_dict = {
            component.name: f"`{component.header}`" for component in self._components
        }

        # Update with any extra parameters
        format_dict.update(self._extra_params)

        error_header, missing_headers = self.error_headers()

        if error_header:
            return "", missing_headers

        # Format expression with all parameters
        query = self._exp.format(**format_dict)
        return query, missing_headers

    @property
    def query_headers(self) -> list[str]:
        return [component.header for component in self._components]

    def error_headers(self) -> tuple[bool, list]:
        missing_headers = [
            component.header
            for component in self._components
            if component.header not in self._df.columns
        ]
        if missing_headers:
            return True, missing_headers
        return False, missing_headers
