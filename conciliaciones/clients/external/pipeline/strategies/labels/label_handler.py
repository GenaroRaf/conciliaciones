from k_link.db.core import ObjectId
from k_link.db.daos import LabelTemplatesDAO
from k_link.db.models import LabelTemplates
from k_link.extensions.pipeline import LabelOptions
from loggerk import LoggerK
from pandas import DataFrame, Series

from conciliaciones.clients.external.pipeline.utils.expresion_params_handler import (
    BaseExpressionParamHandler,
)


class LabelHandler:
    def __init__(
        self,
        df: DataFrame,
        label_config: LabelOptions,
        extra_params: dict | None = None,
    ) -> None:
        self._logger = LoggerK(self.__class__.__name__)
        self._df: DataFrame = df
        self._label_config: LabelOptions = label_config
        self._regla_etiquetado = LabelTemplatesDAO()
        self._extra_params = extra_params or {}

    def apply_label(self) -> DataFrame:
        label_id = ObjectId(self._label_config.label_id)
        label: LabelTemplates | None = self._regla_etiquetado.get_by_id_sync(
            item_id=label_id
        )

        if label is None:
            raise ValueError(f"Label not found. ID {label_id}")

        self._logger.info(f"Applying label: {label.header_name} with ID: {label_id}")

        self._df[label.header_name] = None
        params_dict: dict[str, str] = {}

        for case in label.clauses:
            base_expression_handler = BaseExpressionParamHandler(
                df=self._df,
                exp=case.clause,
                params=self._label_config.params,
                constant_params=self._label_config.constant_params,
                id_report_asociado=self._label_config.report_id,
                reports_asociados=label.reportes_asociados,
                extra_params=self._extra_params,
            )
            query, format_dict, missing_headers = (
                base_expression_handler.format_expression()
            )
            self._logger.info(f"Query: {query}")

            if query == "":
                self._logger.error(
                    f"Headers not found in DataFrame for filter expression: {missing_headers}. Label not aplied"
                )
                continue

            mask = self._df.eval(query)

            missing_mask: Series = self._df[label.header_name].isna()
            self._df.loc[mask & missing_mask, label.header_name] = case.value  # type: ignore

            self._logger.info(f"Valor aplicado: {case.value}")

            params_dict = {**params_dict, **format_dict}

            for clave in self._extra_params:
                params_dict.pop(clave, None)

        missing_mask: Series = self._df[label.header_name].isna()
        self._df.loc[missing_mask, label.header_name] = label.default_value

        self.extra_params(label=label, params=params_dict)

        return self._df

    def extra_params(self, label: LabelTemplates, params: dict[str, str]) -> None:
        # Params establecidos en el label
        label_params: set[str] = set(param for param in label.params)
        label_constant_params: set[str] = set(param for param in label.constant_params)
        label_params: set[str] = label_params.union(label_constant_params)

        # Params que se usan en el label
        used_params: set[str] = set(params.keys())

        extra_params: set[str] = used_params - label_params

        dict_extra_params: dict[str, str] = {
            param: params[param] for param in extra_params
        }

        if not extra_params:
            return

        if extra_params:
            self._logger.error(
                f"Extra parameters found: {dict_extra_params}. These parameters are not defined in the label configuration."
            )
