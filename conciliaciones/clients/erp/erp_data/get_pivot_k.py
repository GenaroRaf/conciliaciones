import re
from io import BytesIO

import numpy as np
import pandas as pd
from k_link.db.core import ObjectId
from k_link.db.daos import ERPFilesDAO, ExcelDataTypeDAO
from k_link.db.models import ERPFiles
from k_link.extensions.conciliation_type import ConciliationType
from k_link.extensions.pivot_k import (
    ChooseStrategy,
    ConcatStrategy,
    PivoteKHeader,
    PivotK,
    RegexpStrategy,
    SplitStrategy,
    StrategyComponent,
    is_choose_strategy,
    is_concat_strategy,
    is_none_strategy,
    is_regexp_strategy,
    is_split_strategy,
)
from k_link.extensions.report_config import HeaderConfig
from loggerk import LoggerK

from conciliaciones.utils.completion_handler.airflow_contex_exception import (
    AirflowContexException,
)
from conciliaciones.utils.headers.headers_types import HeadersTypes
from conciliaciones.utils.redis.redis_keys import RedisKeys
from conciliaciones.utils.redis.redis_storage import RedisStorage

ERP_FILES = ERPFilesDAO()
PIVOTE_K_HEADER_BASE: str = "Pivote K"
EXCEL_DATA_TYPES = ExcelDataTypeDAO()
TYPE_HEADER = "pivot"


class PivoteKManager:
    _logger: LoggerK

    def __init__(
        self,
        run_id: str,
        project_id_str: str,
        month: int,
        year: int,
        conciliation_type: ConciliationType,
    ) -> None:
        super().__init__()
        self._logger = LoggerK(self.__class__.__name__)
        self.project_id_str: str = project_id_str
        self.project_id = ObjectId(project_id_str)
        self.redis = RedisStorage()
        self.redis_keys = RedisKeys(
            run_id=run_id,
            project_id_str=self.project_id_str,
            month=month,
            year=year,
            conciliation_type=conciliation_type,
        )
        self._header_types = HeadersTypes(
            run_id=run_id,
            project_id_str=self.project_id_str,
            month=month,
            year=year,
            conciliation_type=conciliation_type,
        )
        self._airflow_fail_exception = AirflowContexException(
            run_id=run_id,
            project_id=project_id_str,
            year=year,
            month=month,
            conciliation_type=conciliation_type,
        )

    async def get_pivote_k_serie(self) -> None:
        # Obtener los datos de redis
        df: pd.DataFrame | None = self.redis.get_df(
            redis_key=self.redis_keys.get_erp_redis_key()
        )

        if df is None:
            self._airflow_fail_exception.handle_and_store_exception(
                f"No se encontro el DataFrame de la key {self.redis_keys.get_erp_redis_key()}"
            )

        # Obtener la lista de configuraciones de pivote K
        erp_files: ERPFiles | None = await ERP_FILES.get(project_id=self.project_id)
        if erp_files is None:
            self._airflow_fail_exception.handle_and_store_exception(
                f"No se encontró configuración del ERPFiles para el proyecto: {self.project_id}"
            )

        pivot_k_list: list[PivotK] | None = erp_files.pivot_k

        # Validar contenido en pivote K list
        if pivot_k_list is None or len(pivot_k_list) == 0:
            self._airflow_fail_exception.handle_and_store_exception(
                f"No hay configuración para la Pivot K del proyecto: {self.project_id_str}"
            )

        # Se recupera lista final de erp headers
        headers_erp_final: list[HeaderConfig] = self._header_types.get_headers_list(
            redis_key=self.redis_keys.get_headers_erp_final_list_key()
        )

        headers_pivot: list[HeaderConfig] = []
        headers_name_strategy: list[str] = []

        self._logger.info(f"Pivot k list: {pivot_k_list}")

        for pivot_k_config in pivot_k_list:
            self._logger.info(f"Type: {pivot_k_config.type.value}")
            self._logger.info(f"Strategy: {pivot_k_config.pivote_k_header.value}")

            # Encabezado de pivoteK
            pivote_k_header: str = self.get_pivote_k_header_name(
                strategy=pivot_k_config.pivote_k_header
            )

            # Sin estrategia
            if is_none_strategy(
                pivot_k_config.strategy, strategy_type=pivot_k_config.type
            ):
                headers_name_strategy.append(pivot_k_config.strategy.header)
                self._logger.info(f"Column: {pivot_k_config.strategy.header}")
                df[pivote_k_header] = df[pivot_k_config.strategy.header]

            # Estrategia de regex
            elif is_regexp_strategy(
                pivot_k_config.strategy, strategy_type=pivot_k_config.type
            ):
                headers_name_strategy.append(pivot_k_config.strategy.header)
                self._logger.info(f"Column: {pivot_k_config.strategy.header}")
                self.apply_regex_strategy(
                    df=df,
                    regex_strategy=pivot_k_config.strategy,
                    pivote_k_header=pivote_k_header,
                )

            # Estrategia de split
            elif is_split_strategy(
                pivot_k_config.strategy, strategy_type=pivot_k_config.type
            ):
                headers_name_strategy.append(pivot_k_config.strategy.header)
                self._logger.info(f"Column: {pivot_k_config.strategy.header}")
                self.apply_split_strategy(
                    df=df,
                    split_strategy=pivot_k_config.strategy,
                    pivote_k_header=pivote_k_header,
                )

            # Estrategia de concat
            elif is_concat_strategy(
                pivot_k_config.strategy, strategy_type=pivot_k_config.type
            ):
                headers_name_strategy = pivot_k_config.strategy.headers
                self._logger.info(f"Column: {pivot_k_config.strategy.headers}")
                self.apply_concat_strategy(
                    df=df,
                    concat_strategy=pivot_k_config.strategy,
                    pivote_k_header=pivote_k_header,
                )

            # Estrategia de choose
            elif is_choose_strategy(
                pivot_k_config.strategy, strategy_type=pivot_k_config.type
            ):
                headers_name_strategy = [
                    component.name for component in pivot_k_config.strategy.components
                ]

                self._logger.info(f"Strategies: {pivot_k_config.strategy.components}")
                df[pivote_k_header] = self.apply_choose_strategy(
                    df=df, choose_strategy=pivot_k_config.strategy
                )

            self._header_types._add_headers_pivot(
                header_list=headers_name_strategy,
                pivote_k_header_k=pivote_k_header,
                headers_erp_final=headers_erp_final,
                headers_pivot=headers_pivot,
            )

            self._logger.info(f"Column pivot k: {df[pivote_k_header]}")
            self._logger.info(
                f"Numero de {pivot_k_config.pivote_k_header.value}: {len(df[pivote_k_header])}"
            )

        # Guardar lista de dynamic headers en redis
        await self._header_types.save_redis_headers_list(
            redis_key=self.redis_keys.get_headers_pivot_list_key(),
            headers_list=headers_pivot,
        )

        # Actualiar dataframe en redis
        buffer_df: BytesIO = self.redis.set_parquet(df=df)
        self.redis.set(key=self.redis_keys.get_erp_redis_key(), value=buffer_df)

    @staticmethod
    def get_pivote_k_header_name(strategy: PivoteKHeader) -> str:
        return f"{PIVOTE_K_HEADER_BASE} {strategy.value}"

    @staticmethod
    def apply_regex(field, regex: str) -> tuple:
        if isinstance(field, str):
            match = re.search(rf"{regex}", field.upper())
            if match:
                return match.groups()
            return tuple()  # Si no hay match, tupla vacía
        return (field,)  # Devuelve el valor original si no es cadena

    @staticmethod
    def apply_regex_strategy(
        df: pd.DataFrame, regex_strategy: RegexpStrategy, pivote_k_header: str
    ) -> None:
        header: str = regex_strategy.header
        regex: str = regex_strategy.pattern
        group_names: list[str] | None = regex_strategy.group_names
        pivot_index: int | None = regex_strategy.pivot_index

        # Aplicar regex a cada valor
        df_regex: pd.DataFrame = df[header].apply(
            lambda x: pd.Series(PivoteKManager.apply_regex(x, regex))
        )

        # Crear nombres de columnas
        column_num: int = df_regex.shape[1]
        column_names: list[str] = []

        if column_num == 1:
            column_names.append(pivote_k_header)

        if group_names is not None:
            for i in range(column_num):
                if i == pivot_index:
                    column_names.append(pivote_k_header)
                else:
                    column_names.append(group_names[i])

        df_regex.columns = column_names

        for name in df_regex.columns:
            df[name] = df_regex[name]

    @staticmethod
    def apply_split(field: str, split_constraint_character: str, position: int):
        if isinstance(field, str):
            split_list: list[str] = field.split(split_constraint_character)
            split_result = str(split_list[position])

            joined_field: str = "".join(split_result)
            return joined_field

        return field  # Devuelve el valor original si no es cadena

    @staticmethod
    def apply_split_strategy(
        df: pd.DataFrame, split_strategy: SplitStrategy, pivote_k_header: str
    ) -> None:
        header: str = split_strategy.header
        split_constraint: str = split_strategy.separator
        position: int = split_strategy.position

        # Asignación de pivoteK
        df[pivote_k_header] = df[header].apply(
            lambda x: PivoteKManager.apply_split(
                field=str(x),
                split_constraint_character=split_constraint,
                position=position,
            )
        )

    @staticmethod
    def apply_concat_strategy(
        df: pd.DataFrame, concat_strategy: ConcatStrategy, pivote_k_header: str
    ):
        separator_constraint: str = concat_strategy.separator
        headers: list[str] = concat_strategy.headers

        if separator_constraint is None:
            df[pivote_k_header] = df[headers].apply(lambda row: "".join(row), axis=1)
        else:
            df[pivote_k_header] = df[headers].apply(
                lambda row: separator_constraint.join(str(x) for x in row), axis=1
            )

    @staticmethod
    def apply_choose_strategy(
        df: pd.DataFrame, choose_strategy: ChooseStrategy
    ) -> pd.Series:
        components: list[StrategyComponent] = choose_strategy.components

        first_header_series: str = components[0].header
        second_header_series: str = components[1].header

        # Asignación de pivoteK. Si los encabezados coinciden, se devuelve el primero, si no, el segundo
        result = np.where(
            df[first_header_series] == df[second_header_series],
            df[first_header_series].astype(dtype=str),
            df[second_header_series].astype(dtype=str),
        )

        return pd.Series(result, index=df.index)
