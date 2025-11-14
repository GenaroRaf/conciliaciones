import re

import pandas as pd
from k_link.db.daos.pivot_table_dao import PivotTableDAO
from k_link.db.models import PivotTable
from k_link.extensions.pipeline import Filter
from k_link.extensions.pipeline.pivot_table_options import PivotOptions, SourcePivot
from k_link.extensions.report_config.filter_params import FilterParams
from loggerk import LoggerK
from pandas import DataFrame, MultiIndex

from conciliaciones.utils.redis.redis_keys import RedisKeys


class PivotHandler:
    def __init__(
        self,
        df: DataFrame,
        pipeline: bool,
        pivot_options: PivotOptions,
        redis_key: RedisKeys,
    ) -> None:
        self._logger = LoggerK(self.__class__.__name__)
        self._df = df
        self._pipeline: bool = pipeline
        self._pivot_config_custom = pivot_options
        self._redis_key = redis_key

        self._pivot_table_dao = PivotTableDAO()

    def create_pivot_tables(self) -> tuple[str, DataFrame]:
        """
        * Crea tablas dinámicas basadas en las opciones proporcionadas.
        * Guarda el resultado en Redis.
        """
        data_pivot: dict = {}
        df_pivot: DataFrame = DataFrame()
        pivot_config_catalog: PivotTable | None = self._pivot_table_dao.get_by_id_sync(
            item_id=self._pivot_config_custom.pivot_id
        )

        if pivot_config_catalog is None:
            self._logger.error(
                f"No se encontró la tabla dinámica con ID: {self._pivot_config_custom.pivot_id}."
            )
            return "", DataFrame()

        try:
            self._logger.info(f"Pivot config catalog. {pivot_config_catalog}")
            self._logger.info(f"Pivot config template. {self._pivot_config_custom}")

            df_clean: DataFrame = self._clean_numeric_columns(
                self._df, data_pivot.get("values", [])
            )

            filter_pivot_catalog: Filter | None = pivot_config_catalog.filter
            filter_pivot_template: FilterParams | None = (
                self._pivot_config_custom.filter_params
            )
            expression: str = ""
            clause: str = ""
            missing_headers = []
            apply_filter: bool = False
            params: dict[str, str] = {}

            if self._pivot_config_custom.source_pivot == SourcePivot.TEMPLATE:
                if filter_pivot_catalog:
                    apply_filter = True

                    clause: str = filter_pivot_catalog.clause

                    for component in filter_pivot_catalog.components:
                        params[component.name] = component.header

                else:
                    apply_filter = False

            elif self._pivot_config_custom.source_pivot == SourcePivot.CUSTOM:
                if filter_pivot_template:
                    apply_filter = True

                    clause = filter_pivot_template.expresion
                    params = filter_pivot_template.params
                else:
                    apply_filter = False

            if apply_filter:
                expression, _, missing_headers = self._format_expression(
                    exp=clause,
                    params=params,
                    df=df_clean,
                )

                if expression == "":
                    self._logger.error(
                        f"Headers not found in DataFrame for filter expression: {missing_headers}. Filter not applied"
                    )
                    return "", DataFrame()

                expression = self.sanitize_expression(expression)
                self._logger.info(f"Applying filter expression: {expression}")
                df_clean = df_clean.query(expression)

                if df_clean.empty:
                    self._logger.error(
                        f"Dataframe vacio, filtro utilizado: {expression}",
                        exc_info=True,
                    )

            # Traer info para la tabla dinámica
            data_pivot = self._get_pivot_data(pivot_config_catalog, df_clean)

            # Validar columnas
            validate_columns = self._validate_columns(
                self._df, data_pivot, pivot_config_catalog
            )

            if not validate_columns:
                return "", DataFrame()

            df_pivot: DataFrame = pd.pivot_table(**data_pivot)
            if pivot_config_catalog.order_by:
                df_pivot = df_pivot.sort_values(
                    by=pivot_config_catalog.order_by,
                    ascending=pivot_config_catalog.ascending or False,
                )

            if pivot_config_catalog.reset_index:
                df_pivot = df_pivot.reset_index()

            df_pivot = self._apply_column_order(
                df_pivot=df_pivot, pivot_config_catalog=pivot_config_catalog
            )

            return pivot_config_catalog.nombre, df_pivot

        except Exception as e:
            self._logger.error(
                f"[PivotError] Error al crear tabla dinámica '{pivot_config_catalog.nombre}': {e}",
                exc_info=True,
            )
            return "", DataFrame()

    def _get_pivot_data(self, pivot_config_catalog: PivotTable, df: DataFrame) -> dict:
        """
        * Extrae y prepara los datos necesarios para crear la tabla dinámica.
        TODO @param pivot_config_catalog: Configuración de la tabla dinámica.
        ? Retorna: Diccionario con los datos preparados.
        """
        data_pivot: dict = {"data": df}

        if self._pivot_config_custom.source_pivot == SourcePivot.TEMPLATE:
            data_pivot["index"] = pivot_config_catalog.index
            data_pivot["columns"] = pivot_config_catalog.columns
            data_pivot["values"] = pivot_config_catalog.values
            data_pivot["aggfunc"] = pivot_config_catalog.aggfunc
        elif self._pivot_config_custom.source_pivot == SourcePivot.CUSTOM:
            data_pivot["index"] = self._pivot_config_custom.index_params
            data_pivot["columns"] = self._pivot_config_custom.columns_params
            data_pivot["values"] = self._pivot_config_custom.values_params
            data_pivot["aggfunc"] = self._pivot_config_custom.agg_func_params

        data_pivot["fill_value"] = pivot_config_catalog.fill_value
        data_pivot["dropna"] = pivot_config_catalog.dropna

        if self._pipeline:
            return data_pivot

        data_pivot["margins"] = pivot_config_catalog.margins
        data_pivot["margins_name"] = pivot_config_catalog.margins_name

        return data_pivot

    def _validate_columns(
        self, df: DataFrame, config: dict, pivot_config_catalog: PivotTable
    ) -> bool:
        """
        * Valida que el DataFrame contenga todas las columnas requeridas
        por la configuración de la tabla dinámica.
        ! Lanza ValueError si faltan columnas.
        TODO @param df: DataFrame a validar.
        TODO @param config: Configuración de la tabla dinámica.
        """

        required_cols = {
            k: v or []
            for k, v in {
                "index": config.get("index", []),
                "columns": config.get("columns", []),
                "values": config.get("values", []),
                "order_by": pivot_config_catalog.order_by,
            }.items()
        }
        missing = {
            k: [col for col in v if col not in df.columns]
            for k, v in required_cols.items()
            if any(col not in df.columns for col in v)
        }
        if missing:
            msg = " | ".join(f"{k}: {v}" for k, v in missing.items())
            self._logger.error(
                f"[PivotWarning] Tabla dinámica '{pivot_config_catalog.nombre}' con columnas faltantes: {msg}"
            )
            return False

        return True

    def _clean_numeric_columns(self, df: DataFrame, columns: list[str]) -> DataFrame:
        """
        * Limpia y convierte a numérico las columnas indicadas, reemplazando valores no numéricos por cero.
        TODO @param df: DataFrame de entrada.
        TODO @param columns: Lista de columnas a limpiar.
        ? Retorna: DataFrame con columnas limpias.
        """

        for col in columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)  # type: ignore
        return df

    def _format_expression(
        self,
        exp: str,
        params: dict,
        df: DataFrame,
    ) -> tuple[str, dict[str, str], list]:
        format_dict: dict = {}
        format_dict = {**format_dict, **params}

        error_header, missing_headers = self.error_headers(
            format_dict=format_dict, df=df
        )

        if error_header:
            return "", format_dict, missing_headers

        for letter, header_name in format_dict.items():
            format_dict[letter] = f'"{header_name}"'

        query: str = exp.format(**format_dict)
        return query, format_dict, missing_headers

    def error_headers(self, format_dict: dict, df: DataFrame) -> tuple[bool, list]:
        missing_headers = [
            header_name
            for letter, header_name in format_dict.items()
            if header_name not in df.columns
        ]

        if missing_headers:
            return True, missing_headers
        return False, missing_headers

    def sanitize_expression(self, expr: str) -> str:
        return re.sub(r'"([^"]+)"', r"`\1`", expr)

    def _apply_column_order(
        self, df_pivot: DataFrame, pivot_config_catalog: PivotTable
    ) -> DataFrame:
        """
        Reordena columnas de la pivot table según la configuración.
        Soporta:
        - Columnas simples
        - MultiIndex
        - Reset index (agrega índices como columnas normales)
        - Caso sin columnas (solo index + values)
        """
        if (
            not self._pivot_config_custom.columns_params
            and not self._pivot_config_custom.values_params
        ):
            return df_pivot

        # lista de headers ordenadas
        expected_cols: list[str] = []

        if pivot_config_catalog.reset_index and self._pivot_config_custom.index_params:
            expected_cols.extend(self._pivot_config_custom.index_params)

        if self._pivot_config_custom.columns_params:
            expected_cols.extend(self._pivot_config_custom.columns_params)

        if self._pivot_config_custom.values_params:
            expected_cols.extend(self._pivot_config_custom.values_params)

        # MultiIndex en columnas
        if isinstance(df_pivot.columns, MultiIndex):
            if all(isinstance(c, tuple) for c in expected_cols):
                valid_cols = [c for c in expected_cols if c in df_pivot.columns]
                return df_pivot.reindex(columns=pd.MultiIndex.from_tuples(valid_cols))  # type: ignore
            valid_cols = [
                c
                for c in expected_cols
                if c in df_pivot.columns.get_level_values(level=0)
            ]
            return df_pivot.reindex(columns=valid_cols, level=0)
        valid_cols: list[str] = [c for c in expected_cols if c in df_pivot.columns]
        return df_pivot.reindex(columns=valid_cols)
