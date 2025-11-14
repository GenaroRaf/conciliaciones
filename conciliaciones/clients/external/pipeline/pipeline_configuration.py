from typing import Final

import pandas as pd
from k_link.extensions.pipeline import (
    DataFrameConfig,
    Estrategia,
    Options,
    PipelineFileOperation,
    PipelineOperation,
)
from k_link.extensions.report_config import HeaderConfig
from loggerk import LoggerK
from pandas import DataFrame

from conciliaciones.clients.external.pipeline.base_strategy_abc import (
    BaseStrategy,
    StrategyConcat,
    StrategyDropDuplicate,
    StrategyEtiqueta,
    StrategyFilter,
    StrategyFstring,
    StrategyGroup,
    StrategyJoin,
    StrategyOperation,
    StrategyPivotTable,
    StrategyRegexp,
)
from conciliaciones.utils.redis.redis_keys import RedisKeys


class PipelineFactory:
    _map: Final[dict[Estrategia, type[BaseStrategy]]] = {
        Estrategia.CONCATENATE: StrategyConcat,
        Estrategia.JOIN: StrategyJoin,
        Estrategia.GROUP: StrategyGroup,
        Estrategia.FILTER: StrategyFilter,
        Estrategia.OPERATION: StrategyOperation,
        Estrategia.FSTRING: StrategyFstring,
        Estrategia.LABEL: StrategyEtiqueta,
        Estrategia.REGEX: StrategyRegexp,
        Estrategia.DROPDUPLICATES: StrategyDropDuplicate,
        Estrategia.PIVOT_TABLE: StrategyPivotTable,
    }

    @classmethod
    def create(
        cls,
        stratregy: Estrategia,
        df: pd.DataFrame,
        args: Options,
        df_temp: pd.DataFrame,
        year: int,
        month: int,
        redis_key: RedisKeys,
    ) -> BaseStrategy:
        strategy_cls: type[BaseStrategy] | None = cls._map.get(stratregy)
        if not strategy_cls:
            raise ValueError(f"No service mapped for Strategy: {stratregy}")
        return strategy_cls(df, args, df_temp, year, month, redis_key)


class PipelineConfiguration:
    def __init__(
        self,
        data: pd.DataFrame,
        data_frame_config: DataFrameConfig,
        pipeline_data_df: list[tuple[str, pd.DataFrame]],
        datasources_optional: list[str],
        year: int,
        month: int,
        redis_key: RedisKeys,
    ) -> None:
        self._logger = LoggerK(self.__class__.__name__)
        self._year: int = year
        self._month: int = month

        self._data_frame_config: DataFrameConfig = data_frame_config
        self._data: pd.DataFrame = data
        self._pipelines_data_df: list[tuple[str, pd.DataFrame]] = pipeline_data_df
        self._datasources_optional: list[str] = datasources_optional
        self._redis_key = redis_key

        self.pipeline_data_map: dict[str, pd.DataFrame] = {
            name: df for name, df in self._pipelines_data_df
        }

    async def apply_configuration_pipeline(self) -> tuple[DataFrame, HeaderConfig]:
        pipelines: list[PipelineOperation] = self._data_frame_config.pipeline

        header_config: HeaderConfig = None  # type: ignore
        for pipeline in pipelines:
            if isinstance(pipeline, PipelineFileOperation):
                if pipeline.df_base in self._datasources_optional:
                    self._logger.error(
                        f"Pipeline {pipeline.df_base} es opcional, se omite"
                    )
                    continue

            if pipeline.args is None:
                raise ValueError(
                    f"La estrategia {pipeline.tipo} no tiene argumentos definidos"
                )

            self._logger.info(f"Aplicando estrategia: {pipeline.tipo}")

            pipeline_data_df = pd.DataFrame()
            if pipeline.tipo in [
                Estrategia.JOIN,
                Estrategia.CONCATENATE,
                Estrategia.OPERATION,
            ]:
                try:
                    pipeline_data_df: pd.DataFrame = self.pipeline_data_map[
                        (
                            pipeline.df_base
                            if isinstance(pipeline, PipelineFileOperation)
                            else pipeline.json_source.value
                        )
                    ]
                except StopIteration:
                    raise ValueError(
                        f"No se encontró el DataFrame temporal para la estrategia {pipeline.tipo}"
                    )

            self._logger.info(f"DataFrame Base: {self._data.columns}")
            self._logger.info(
                f"DataFrame Temporal (Pipeline): {pipeline_data_df.columns}"
            )

            try:
                strategy: BaseStrategy = PipelineFactory.create(
                    stratregy=pipeline.tipo,
                    df=self._data,
                    args=pipeline.args,
                    df_temp=pipeline_data_df,
                    year=self._year,
                    month=self._month,
                    redis_key=self._redis_key,
                )

                result = strategy.execute_strategy

                if isinstance(result, pd.DataFrame):
                    result = (result, None)

                if not isinstance(result, tuple) or not isinstance(
                    result[0], pd.DataFrame
                ):
                    raise ValueError(
                        f"Expected a tuple with a DataFrame as the first element, got {type(result)}"
                    )

                self._data, header_config = result  # type: ignore

            except Exception as e:
                raise ValueError(
                    f"Error al aplicar la estrategia {pipeline.tipo.value}: {e}"
                ) from e

        return self._data, header_config
