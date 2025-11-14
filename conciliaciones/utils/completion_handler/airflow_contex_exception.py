from typing import NoReturn

from airflow.exceptions import AirflowException
from k_link.extensions.conciliation_type import ConciliationType
from loggerk import LoggerK

from conciliaciones.utils.redis.redis_keys import RedisKeys
from conciliaciones.utils.redis.redis_storage import RedisStorage


class AirflowContexException:
    def __init__(
        self,
        year: int,
        month: int,
        project_id: str,
        run_id: str,
        conciliation_type: ConciliationType,
    ) -> None:
        self._logger = LoggerK(self.__class__.__name__)
        self._redis = RedisStorage()
        self._redis_key = RedisKeys(
            run_id=run_id,
            project_id_str=project_id,
            month=month,
            year=year,
            conciliation_type=conciliation_type,
        )

    def handle_and_store_exception(self, message: str) -> NoReturn:
        self._logger.error(message)

        self._redis.set(
            key=self._redis_key.get_exceptions_redis_key(),
            value=message,
        )

        raise AirflowException(message)
