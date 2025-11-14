from abc import ABC, abstractmethod

from k_link.extensions.pipeline import (
    ComplexConfig,
    ComplexOperation,
    DateConfig,
    GeneralConfig,
    LambdaConfig,
    Operation,
    SplitExplodeConfig,
    TextTransformConfig,
)
from k_link.extensions.report_config import HeaderConfig
from loggerk import LoggerK
from pandas import DataFrame

from conciliaciones.clients.external.pipeline.strategies.operations.complex.complex_operation_handlers.date_handler import (
    DateOperationHandler,
)
from conciliaciones.clients.external.pipeline.strategies.operations.complex.complex_operation_handlers.general_handler import (
    GeneralHandler,
)
from conciliaciones.clients.external.pipeline.strategies.operations.complex.complex_operation_handlers.lambda_handler import (
    LambdaHandler,
)
from conciliaciones.clients.external.pipeline.strategies.operations.complex.complex_operation_handlers.split_explode_handler import (
    SplitExplodeHandler,
)
from conciliaciones.clients.external.pipeline.strategies.operations.complex.complex_operation_handlers.text_transform_handler import (
    TextTransformHandler,
)
from conciliaciones.utils.redis.redis_keys import RedisKeys
from conciliaciones.utils.redis.redis_storage import RedisStorage


class BaseOperationABC(ABC):
    """
    Abstract base class for complex operation strategies.

    Attributes:
        df (DataFrame): The input DataFrame to apply operations on.
        operation (Operation): The base operation configuration.
        complex_config (ComplexConfig): The complex operation specific configuration.
        redis_key (RedisKeys): The Redis key for caching or state management.

    Returns:
        tuple[DataFrame, HeaderConfig]:
            - DataFrame with the new column generated.
            - Header configuration for the report.
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
        self._complex_config: ComplexConfig = complex_operation.complex_config
        self._redis_key: RedisKeys = redis_key
        self._redis: RedisStorage = RedisStorage()

    @abstractmethod
    def apply_operation_strategy(
        self,
    ) -> tuple[DataFrame, HeaderConfig]: ...


class GeneralStrategy(BaseOperationABC):
    """Applies a general operation strategy."""

    def apply_operation_strategy(self) -> tuple[DataFrame, HeaderConfig]:
        if not isinstance(self._complex_config, GeneralConfig):
            raise ValueError("Invalid args for General Operation strategy")

        self._logger.info(f"Expression: {self._complex_config.expression}")
        self._logger.info(f"Components: {self._complex_config.components}")
        self._logger.info(f"Context: {self._complex_config.context}")

        general_handler = GeneralHandler(
            df=self._df,
            operation=self._operation,
            general_config=self._complex_config,
        )

        aux_df, header_config = general_handler.apply_general_operation()

        return aux_df, header_config


class DateOperationStrategy(BaseOperationABC):
    """Applies the operation with date addition/subtraction on the origin column."""

    def apply_operation_strategy(self) -> tuple[DataFrame, HeaderConfig]:
        if not isinstance(self._complex_config, DateConfig):
            raise ValueError("Invalid args for Date Operation strategy")

        self._logger.info(f"Origin column: {self._complex_config.origin_column}")
        self._logger.info(f"Value o column: {self._complex_config.value_or_column}")
        self._logger.info(f"Date type: {self._complex_config.date_type}")
        self._logger.info(f"Operation: {self._complex_config.operation}")
        self._logger.info(f"Format date: {self._complex_config.format_date}")

        date_operation_handler: DateOperationHandler = DateOperationHandler(
            df=self._df, operation=self._operation, date_config=self._complex_config
        )

        aux_df, header_config = date_operation_handler.apply_date_operation()

        return aux_df, header_config


class LambdaStrategy(BaseOperationABC):
    """Applies a lambda operation strategy."""

    def apply_operation_strategy(self) -> tuple[DataFrame, HeaderConfig]:
        if not isinstance(self._complex_config, LambdaConfig):
            raise ValueError("Invalid args for Lambda Operation strategy")

        self._logger.info(f"Expression: {self._complex_config.expression}")
        self._logger.info(f"Components: {self._complex_config.components}")
        self._logger.info(f"Context: {self._complex_config.context}")
        self._logger.info(f"Axis: {self._complex_config.axis}")

        lambda_handler = LambdaHandler(
            df=self._df,
            operation=self._operation,
            lambda_config=self._complex_config,
        )

        aux_df, header_config = lambda_handler.apply_lambda_operation()

        return aux_df, header_config


class SplitExplodeStrategy(BaseOperationABC):
    """Applies the operation with (split and explode) on the origin column."""

    def apply_operation_strategy(self) -> tuple[DataFrame, HeaderConfig]:
        if not isinstance(self._complex_config, SplitExplodeConfig):
            raise ValueError("Invalid args for Split and Explode Operation strategy")

        self._logger.info(f"Origin column: {self._complex_config.origin_column}")
        self._logger.info(f"split: {self._complex_config.split}")

        split_explode_handler: SplitExplodeHandler = SplitExplodeHandler(
            df=self._df,
            operation=self._operation,
            split_explode_config=self._complex_config,
        )

        aux_df, header_config = split_explode_handler.apply_split_explode_operation()

        self._logger.info(f"split: {aux_df[self._operation.name]}")

        return aux_df, header_config


class TextTransformStrategy(BaseOperationABC):
    """Applies a text transform operation strategy."""

    def apply_operation_strategy(self) -> tuple[DataFrame, HeaderConfig]:
        if not isinstance(self._complex_config, TextTransformConfig):
            raise ValueError("Invalid args for Text Transform Operation strategy")

        self._logger.info(f"Origin column: {self._complex_config.origin_column}")
        self._logger.info(f"Operation: {self._complex_config.text_case}")

        lower_upper_handler: TextTransformHandler = TextTransformHandler(
            df=self._df,
            operation=self._operation,
            text_transform_config=self._complex_config,
        )

        aux_df, header_config = lower_upper_handler.apply_text_transform_operation()

        return aux_df, header_config
