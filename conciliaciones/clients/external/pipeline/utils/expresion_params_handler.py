from typing import Protocol

from k_link.db.core import ObjectId
from k_link.extensions import ReporteAsociado
from loggerk import LoggerK
from pandas import DataFrame


class ExpressionConfig(Protocol):
    @property
    def exp(self) -> str: ...

    @property
    def params(self) -> dict[str, str]: ...

    @property
    def report_asociado(self) -> ObjectId | None: ...

    @property
    def reports_asociados(self) -> list: ...


class BaseExpressionParamHandler:
    def __init__(
        self,
        df: DataFrame,
        exp: str,
        params: dict[str, str],
        constant_params: dict[str, str],
        id_report_asociado: ObjectId | None,
        reports_asociados: list[ReporteAsociado],
        extra_params: dict[str, str] = None,  # type: ignore
    ) -> None:
        self._logger = LoggerK(self.__class__.__name__)
        self._df = df
        self._exp = exp
        self._params = params
        self._constant_params = constant_params
        self._id_report_asociado = id_report_asociado
        self._reports_asociados = reports_asociados
        self._extra_params = extra_params or {}

    def format_expression(self) -> tuple[str, dict[str, str], list]:
        format_dict: dict = {}
        if self._id_report_asociado:
            for reporte in self._reports_asociados:
                if self._id_report_asociado == reporte.report_id:
                    format_dict = reporte.params
                    break

        format_dict = {**format_dict, **self._params}

        error_header, missing_headers = self.error_headers(format_dict=format_dict)

        if error_header:
            return "", format_dict, missing_headers

        for letter, header_name in format_dict.items():
            format_dict[letter] = f"`{header_name}`"

        format_dict.update(self._extra_params)
        format_dict.update(self._constant_params)

        query: str = self._exp.format(**format_dict)
        return query, format_dict, missing_headers

    @property
    def query_headers(self) -> list[str]:
        names_param: list[str] = []
        if self._id_report_asociado:
            for reporte in self._reports_asociados:
                if (
                    hasattr(reporte, "report_id")
                    and self._id_report_asociado == reporte.report_id
                ):
                    params: dict = getattr(reporte, "params", {})
                    for letters, name_parame in params.items():
                        names_param.append(name_parame)

        for letters, name_param in self._params:
            names_param.append(name_param)

        return names_param

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
