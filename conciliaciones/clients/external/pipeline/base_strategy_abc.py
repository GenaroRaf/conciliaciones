import re
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from io import BytesIO

import pandas as pd
from k_link.extensions.pipeline import (
    ConcatOptions,
    Filter,
    FstringOptions,
    GroupOptions,
    JoinOptions,
    LabelOptions,
    Operation,
    OperationType,
    Options,
)
from k_link.extensions.pipeline.drop_duplicate_options import DropDuplicateOptions
from k_link.extensions.pipeline.pivot_table_options import PivotOptions
from k_link.extensions.pivot_k import RegexpStrategy
from k_link.extensions.report_config import HeaderConfig
from loggerk import LoggerK
from pandas import DataFrame

from conciliaciones.clients.external.pipeline.strategies.filters.filter_handler import (
    FilterHandler,
)
from conciliaciones.clients.external.pipeline.strategies.labels.label_handler import (
    LabelHandler,
)
from conciliaciones.clients.external.pipeline.strategies.operations.complex.operation_manager import (
    OperationManager,
)
from conciliaciones.clients.external.pipeline.strategies.operations.simple.operations_handler import (
    OperationHandler,
)
from conciliaciones.clients.external.pipeline.strategies.pivots.pivot_handler import (
    PivotHandler,
)
from conciliaciones.utils.redis.redis_keys import RedisKeys
from conciliaciones.utils.redis.redis_storage import RedisStorage


class BaseStrategy(ABC):
    def __init__(
        self,
        df: DataFrame,
        args: Options,
        df_temp: DataFrame,
        year: int,
        month: int,
        redis_key: RedisKeys,
    ) -> None:
        super().__init__()
        self._logger = LoggerK(self.__class__.__name__)
        self._df_base: DataFrame = df
        self._args = args
        self._df_temp: DataFrame = df_temp
        self._year: int = year
        self._month: int = month
        self._redis_key = redis_key
        self._redis = RedisStorage()

    @property
    @abstractmethod
    def execute_strategy(self) -> DataFrame | tuple[DataFrame, HeaderConfig | None]: ...


class StrategyConcat(BaseStrategy):
    @property
    def execute_strategy(self) -> DataFrame:
        if not isinstance(self._args, ConcatOptions):
            raise ValueError("Invalid args for Concat strategy")

        if self._df_temp is None:
            raise ValueError("df_temp is required for Concat strategy")

        self._logger.info(f"DF Base: {self._df_base.columns}")
        self._logger.info(f"DF Temp: {self._df_temp.columns}")

        self._df_base = pd.concat([self._df_base, self._df_temp], ignore_index=True)

        self._logger.info(f"DataFrame Base Concat: {self._df_base.columns}")
        return pd.DataFrame(self._df_base)


class StrategyJoin(BaseStrategy):
    @property
    def execute_strategy(self) -> DataFrame:
        if not isinstance(self._args, JoinOptions):
            raise ValueError("Invalid args for Join strategy")

        if self._df_temp is None:
            raise ValueError("df_temp is required for Join strategy")

        self._logger.info(f"Left: {self._args.left_on[0]}")
        self._logger.info(f"Right: {self._args.right_on[0]}")
        self._logger.info(f"How: {self._args.how.value}")

        self._logger.info(f"DF Base: {self._df_base.columns}")
        self._logger.info(f"DF Temp: {self._df_temp.columns}")

        self._df_base = pd.merge(
            self._df_base,
            self._df_temp,
            how=self._args.how.value,
            left_on=self._args.left_on[0],
            right_on=self._args.right_on[0],
        )

        self._logger.info(f"DataFrame Base Join: {self._df_base.columns}")
        self._logger.info(f"DataFrame Base Join shape: {self._df_base.shape}")
        return pd.DataFrame(self._df_base)


class StrategyGroup(BaseStrategy):
    @property
    def execute_strategy(self) -> DataFrame:
        if not isinstance(self._args, GroupOptions):
            raise ValueError("Invalid args for Concat strategy")

        self._logger.info(f"grouping by: {self._args.by}")
        self._logger.info(f"aggfunc: {self._args.aggfuncs}")

        df_grouped: DataFrame = self._df_base.groupby(
            by=self._args.by, dropna=False
        ).agg(self._args.aggfuncs)  # type: ignore

        df_grouped = df_grouped.reset_index()

        if self._args.name is None:
            self._args.name = "grouped_dataframe"

        redis_key: str = self._redis_key.get_dataframe_group_redis_key(
            group_name=self._args.name
        )

        self._logger.info(f"DataFrame Group: {df_grouped}")
        self._logger.info(f"Redis key: {redis_key}")

        buffer_df: BytesIO = self._redis.set_parquet(df=df_grouped)
        self._redis.set(key=redis_key, value=buffer_df)

        return DataFrame()


class StrategyFilter(BaseStrategy):
    @property
    def execute_strategy(self) -> DataFrame:
        if not isinstance(self._args, Filter):
            raise ValueError("Invalid args for Filter strategy")

        self._logger.info(f"Clause: {self._args.clause}")
        self._logger.info(f"Components: {self._args.components}")

        filter_handler = FilterHandler(df=self._df_base, filter_config=self._args)
        df_base = filter_handler.apply_filter()

        self._logger.info(f"DataFrame Base Filtrado: {df_base.columns}")
        self._logger.info(f"DataFrame Base Filtrado shape: {df_base.shape}")

        return df_base


class StrategyOperation(BaseStrategy):
    @property
    def execute_strategy(self) -> tuple[DataFrame, HeaderConfig | None]:
        if not isinstance(self._args, Operation):
            raise ValueError("Invalid args for Operation strategy")

        self._logger.info(f"Header name: {self._args.name}")

        if self._args.operation_type == OperationType.SIMPLE:
            self._logger.info("is simple")
            operation_handler = OperationHandler(
                df=self._df_base,
                operation=self._args,
            )

            df_base, header_config = operation_handler.apply_operation()
        elif self._args.operation_type == OperationType.COMPLEX:
            self._logger.info("is complex")
            operation_handler = OperationManager(
                df=self._df_base,
                operation=self._args,
                complex_operation=self._args.operation_config,  # type: ignore
                redis_key=self._redis_key,
            )
            df_base, header_config = operation_handler.apply_complex_operation()
        else:
            raise ValueError("Invalid type Operation strategy")

        return df_base, header_config


class StrategyFstring(BaseStrategy):
    @property
    def execute_strategy(self) -> DataFrame:
        if not isinstance(self._args, FstringOptions):
            raise ValueError("Invalid args for Fstring strategy")

        columns = [header.header for header in self._args.headers]
        for header in self._args.headers:
            if header.header not in self._df_base.columns:
                raise ValueError(f"Header {header.header} not found in DataFrame")

        self._df_base[self._args.name] = self._df_base[columns].apply(
            lambda x: self._args.cadena.format(  # type: ignore
                **{header.name: x[header.header] for header in self._args.headers}  # type: ignore
            ),
            axis=1,
        )

        return self._df_base


class StrategyRegexp(BaseStrategy):
    @property
    def execute_strategy(self) -> DataFrame:
        if not isinstance(self._args, RegexpStrategy):
            raise ValueError("Invalid args for Regexp strategy")

        header: str = self._args.header
        regex: str = self._args.pattern
        group_names: list[str] | None = self._args.group_names

        df_regex: pd.DataFrame = self._df_base[header].apply(
            lambda x: pd.Series(self.apply_regex(x, regex))
        )

        column_num: int = df_regex.shape[1]
        column_names: list[str] = []

        if column_num == 1:
            column_names.append(header)

        if group_names is not None:
            for i in range(column_num):
                column_names.append(group_names[i])

        df_regex.columns = column_names

        for name in df_regex.columns:
            self._df_base[name] = df_regex[name]

        return self._df_base

    @staticmethod
    def apply_regex(field, regex: str) -> tuple:
        if isinstance(field, str):
            match = re.search(rf"{regex}", field.upper())
            if match:
                return match.groups()
            return tuple()  # Si no hay match, tupla vacía
        return (field,)  # Devuelve el valor original si no es cadena


class StrategyEtiqueta(BaseStrategy):
    def get_month_bounds(self, year: int, month: int) -> tuple[str, str, str]:
        start = datetime(year, month, 1, 0, 0, 0)
        if month == 12:
            next_month = datetime(year + 1, 1, 1)
        else:
            next_month = datetime(year, month + 1, 1)
        end = next_month - timedelta(seconds=1)
        now = datetime.utcnow()

        return (
            start.strftime("%Y-%m-%dT%H:%M:%SZ"),
            end.strftime("%Y-%m-%dT%H:%M:%SZ"),
            now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        )

    @property
    def execute_strategy(self) -> DataFrame:
        if not isinstance(self._args, LabelOptions):
            raise ValueError("Invalid args for Etiqueta strategy")

        start_month, end_month, now_date = self.get_month_bounds(
            year=self._year, month=self._month
        )

        self._logger.info(f"etiqueta_id: {self._args.label_id}")
        self._logger.info(f"params: {self._args.params}")
        self._logger.info(f"report_id: {self._args.report_id}")

        label_handler = LabelHandler(
            df=self._df_base,
            label_config=self._args,
            extra_params={
                "end_month": end_month,
                "year": self._year,
                "start_month": start_month,
                "month": self._month,
                "now_date": now_date,
            },
        )
        df_base = label_handler.apply_label()

        self._logger.info(f"DataFrame Base Filtrado: {df_base.columns}")
        self._logger.info(f"DataFrame Base Filtrado shape: {df_base.shape}")

        return df_base


class StrategyDropDuplicate(BaseStrategy):
    @property
    def execute_strategy(self) -> DataFrame:
        if not isinstance(self._args, DropDuplicateOptions):
            raise ValueError("Invalid args for drop duplicate strategy")

        self._logger.info(f"subset: {self._args.subset}")
        self._logger.info(f"keep: {self._args.keep}")
        self._logger.info(f"inplace: {self._args.inplace}")
        self._logger.info(f"ignore_index: {self._args.ignore_index}")

        self._logger.info(f"Numero de regitros antes {self._df_base.shape[0]}")

        # Ensure keep is only 'first', 'last', or False (not string 'False' or 'True')
        keep_value = self._args.keep.value

        new_df: DataFrame = self._df_base.drop_duplicates(
            subset=self._args.subset,
            keep=keep_value,
            ignore_index=self._args.ignore_index,
        )

        duplicados = self._df_base.duplicated()
        self._logger.info(f"Duplicados detectados por pandas: {duplicados.sum()}")

        self._logger.info(f"Numero de regitros despues con subset{new_df.shape[0]}")

        return new_df


class StrategyPivotTable(BaseStrategy):
    @property
    def execute_strategy(self) -> DataFrame:
        if not isinstance(self._args, PivotOptions):
            raise ValueError("Invalid args for drop duplicate strategy")

        self._logger.info(f"Pivot id: {self._args.pivot_id}")
        self._logger.info(f"Index: {self._args.index_params}")
        self._logger.info(f"Columns: {self._args.columns_params}")
        self._logger.info(f"Values: {self._args.values_params}")
        self._logger.info(f"Aggfunc: {self._args.agg_func_params}")
        self._logger.info(f"Filter: {self._args.filter_params}")
        self._logger.info(f"Group by: {self._args.group_by_params}")

        pivot_handler: PivotHandler = PivotHandler(
            df=self._df_base,
            pipeline=True,
            pivot_options=self._args,
            redis_key=self._redis_key,
        )

        pivot_name, df_pivot = pivot_handler.create_pivot_tables()
        df_pivot: DataFrame = df_pivot.reset_index()

        redis_key: str = self._redis_key.get_dataframe_pivot_redis_key(
            pivot_name=pivot_name
        )

        if isinstance(df_pivot.columns, pd.MultiIndex):
            ultimo_nivel: int = df_pivot.columns.nlevels - 1

            df_pivot.columns = [
                col[ultimo_nivel] if col[ultimo_nivel] != "" else col[0]
                for col in df_pivot.columns
            ]

        redis_key: str = self._redis_key.get_dataframe_pivot_redis_key(
            pivot_name=pivot_name
        )

        self._logger.info(f"df pivot creada: {df_pivot}")
        self._logger.info(f"Redis key: {redis_key}")

        buffer_df: BytesIO = self._redis.set_parquet(df=df_pivot)
        self._redis.set(key=redis_key, value=buffer_df)

        return DataFrame()
