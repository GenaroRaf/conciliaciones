from k_link.extensions.pipeline import (
    ComplexOperation,
    ComplexOperationType,
    Operation,
)
from k_link.extensions.report_config import HeaderConfig
from loggerk import LoggerK
from pandas import DataFrame

from conciliaciones.clients.external.pipeline.strategies.operations.complex.base_operation_abc import (
    BaseOperationABC,
    DateOperationStrategy,
    GeneralStrategy,
    LambdaStrategy,
    SplitExplodeStrategy,
    TextTransformStrategy,
)
from conciliaciones.utils.redis.redis_keys import RedisKeys


class OperationFactory:
    """
    Factory class for creating operation strategy instances.
    """

    _map: dict[ComplexOperationType, type[BaseOperationABC]] = {
        ComplexOperationType.GENERAL: GeneralStrategy,
        ComplexOperationType.DATE: DateOperationStrategy,
        ComplexOperationType.LAMBDA: LambdaStrategy,
        ComplexOperationType.TEXT_TRANSFORM: TextTransformStrategy,
        ComplexOperationType.SPLIT_EXPLODE: SplitExplodeStrategy,
    }

    @classmethod
    def operation_create(
        cls,
        df: DataFrame,
        operation: Operation,
        complex_operation: ComplexOperation,
        redis_key: RedisKeys,
    ) -> BaseOperationABC:
        strategy_cls: type[BaseOperationABC] | None = cls._map.get(
            complex_operation.complex_type
        )
        if not strategy_cls:
            raise ValueError(
                f"No service mapped for Operation Strategy: {complex_operation.complex_type}"
            )
        return strategy_cls(df, operation, complex_operation, redis_key)


class OperationManager:
    """Operation Manager apply complex operations to DataFrame.

    Attributes:
        df (DataFrame): The input DataFrame to apply operations on.
        operation (Operation): The base operation configuration.
        complex_operation (ComplexOperation): The complex operation specific configuration.
        redis_key (RedisKeys): The Redis key for caching or state management.

    Methods:
        apply_complex_operation() -> tuple[DataFrame, HeaderConfig | None]:
            Applies the complex operation strategy to the DataFrame and returns the modified DataFrame
    """

    def __init__(
        self,
        df: DataFrame,
        operation: Operation,
        complex_operation: ComplexOperation,
        redis_key: RedisKeys,
    ) -> None:
        self._logger = LoggerK(self.__class__.__name__)
        self._df: DataFrame = df
        self._operation: Operation = operation
        self._complex_operation: ComplexOperation = complex_operation
        self._redis_key: RedisKeys = redis_key

    def apply_complex_operation(self) -> tuple[DataFrame, HeaderConfig | None]:
        """Applies the complex operation strategy to the DataFrame.

        Returns:
            tuple[DataFrame, HeaderConfig | None]: A tuple containing the modified DataFrame and the new HeaderConfig
        """
        try:
            operation_strategy: BaseOperationABC = OperationFactory.operation_create(
                df=self._df,
                operation=self._operation,
                complex_operation=self._complex_operation,
                redis_key=self._redis_key,
            )
            self._logger.info("entró a operation manager")

            result = operation_strategy.apply_operation_strategy()

            match result:
                case DataFrame() as df:
                    df_base, header_config = df, None
                case (DataFrame() as df, cfg):
                    df_base, header_config = df, cfg
                case _:
                    raise ValueError(f"Invalid result from operation: {type(result)}")

        except Exception as e:
            raise ValueError(
                f"Error al aplicar la estrategia {self._complex_operation.complex_type}: {e}"
            ) from e

        return df_base, header_config
