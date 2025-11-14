import io
import pickle
from io import BytesIO
from typing import Any, Type, TypeVar, overload

import numpy as np
import pandas as pd
import redis
from k_link.tools import env
from loggerk import LoggerK
from pandas import DataFrame
from typeguard import check_type
from typing_extensions import Buffer, Literal

T = TypeVar("T")


class RedisStorage:
    @overload
    def __init__(
        self,
        url: str = "redis://redis:6379/0",
        /,
    ): ...

    @overload
    def __init__(
        self,
        host: str = "redis",
        port: int = 6379,
        db: int = 0,
    ): ...

    def __init__(
        self,
        *args,
        **kwargs,
    ):
        """inicialización de la conexion se usa el valor de docker-compose file para el servicio redis"""
        self._logger = LoggerK(self.__class__.__name__)
        if not args and not kwargs:
            url = env.get("REDIS_URL") or "redis://redis:6379/0"
            self._client = redis.StrictRedis.from_url(url)
            return

        if args and not kwargs:
            self._client = redis.from_url(*args)
            return

        host = kwargs.get("host", "redis")
        port = kwargs.get("port", 6379)
        db = kwargs.get("db", 0)

        self._client = redis.StrictRedis(host=host, port=port, db=db)
        return

    @classmethod
    def from_url(cls, url: str):
        """Inicializa la conexión a partir de una URL"""
        client = redis.StrictRedis.from_url(url)
        new_instance = cls.__new__(cls)
        new_instance._client = client
        return new_instance

    def set(self, key: str, value: object) -> None:
        """Establece el valor asociado a una clave"""
        serialized_object = self._serialize(value)
        self._client.set(
            name=key,
            value=serialized_object,
        )

    @overload
    def get(
        self,
        key: str,
    ) -> Any | None: ...
    @overload
    def get(
        self,
        key: str,
        object_type: Type[T] = Type[Any],
    ) -> T | None: ...
    def get(
        self,
        key: str,
        object_type: Type[T] = Type[Any],
    ) -> T | None:
        """Obtiene el valor asociado a una clave

        Si la clave no existe, retorna None

        object_type: Tipo esperado del objeto almacenado en Redis (por defecto, Any)
        """
        serialized_object = self._client.get(key)
        if serialized_object is not None:
            return self._deserialize(
                serialized=serialized_object,  # type: ignore
                object_type=object_type,
            )
        return None

    @property
    def keys(self):
        """Retorna todas las claves almacenadas en Redis"""
        return list(self._get_all_keys())

    def _get_all_keys(self):
        """Obtiene todas las claves almacenadas en Redis"""
        encoded_keys = self._client.keys()
        keys = map(lambda key: key.decode("utf-8"), encoded_keys)  # type: ignore
        return keys

    def scan(self, cursor, match=None):
        return self._client.scan(cursor, match=match)

    def get_members(
        self,
        key: str,
        object_type: Type[T] = Type[Any],
    ) -> list[T]:
        """Obtiene los miembros de un SET

        object_type: Tipo esperado de los objetos almacenados en el SET (por defecto, Any)
        """
        serialized_members = self._client.smembers(key)
        return [
            self._deserialize(serialized=item, object_type=object_type)
            for item in serialized_members  # type: ignore
        ]

    def set_member(self, key: str, value: object) -> None:
        """Establece un miembro de un SET"""
        self._client.sadd(key, self._serialize(value))

    def drop_member(self, key: str, value: Any) -> None:
        """Elimina un miembro del set"""
        # Eliminar el elemento del set
        self._client.srem(key, value)

    def delete(self, key: str) -> None:
        """Eliminar Clave en Redis"""
        self._client.delete(key)

    def delete_keys(self, *keys) -> None:
        """Eliminar Clave en Redis"""
        self._client.delete(*keys)

    def delete_pattern(self, pattern: str) -> None:
        """Eliminar Clave en Redis que cumpla con el patron de regex"""
        for key in self._client.scan_iter(match=pattern):
            self._client.delete(key)

    def __del__(self):
        """destructor de la clase cierra la conexion"""
        self._client.close()

    def _serialize(self, value: object) -> bytes:
        """Serializa un objeto"""
        serialized = pickle.dumps(value)
        return serialized

    def _deserialize(self, serialized: Buffer, object_type: Type[T]) -> T:
        """Deserializa un objeto y verifica que sea del tipo esperado"""
        deserialized = pickle.loads(serialized)
        deserialized = check_type(deserialized, object_type)
        return deserialized

    def set_parquet(
        self,
        df: DataFrame,
        engine: Literal["auto", "pyarrow", "fastparquet"] = "pyarrow",
        compression: Literal["snappy", "gzip", "brotli", "lz4", "zstd"]
        | None = "snappy",
    ) -> BytesIO:
        """Convierte un DataFrame a un buffer Parquet, manejando columnas mixtas."""
        df_buffer = io.BytesIO()

        for col in df.columns:
            if df[col].dtype == "object":
                df[col] = df[col].astype(str)

        df.to_parquet(
            path=df_buffer, engine=engine, compression=compression, index=False
        )
        df_buffer.seek(0)

        return df_buffer

    def get_df(
        self,
        redis_key: str,
        engine: Literal["auto", "pyarrow", "fastparquet"] = "pyarrow",
        columns: list[str] | None = None,
    ) -> DataFrame | None:
        """Recupera un DataFrame desde Redis y lo carga desde Parquet."""
        buffer_df: BytesIO | None = self.get(key=redis_key, object_type=BytesIO)
        if buffer_df is None:
            return None

        buffer_df.seek(0)
        df: DataFrame = pd.read_parquet(buffer_df, engine=engine, columns=columns)

        for col in df.columns:
            match df[col].dtype:
                case "object":
                    df[col] = df[col].astype(str)
                    df[col] = df[col].apply(self.safe_convert_value)
                case "int64":
                    df[col] = df[col].astype("Int64")

        return df

    def medir_tamano_valor(self, df: DataFrame, buffer_df: BytesIO) -> None:
        """Mide el tamaño en bytes del valor almacenado en Redis."""
        size_mb = df.memory_usage(deep=True).sum() / (1024**2)
        self._logger.info(
            f"El DataFrame pesa aproximadamente {size_mb:.2f} MB en memoria"
        )

        compressed_size = buffer_df.getbuffer().nbytes
        self._logger.info(f"Archivo Parquet comprimido: {compressed_size:,} bytes")

    def safe_convert_value(self, value: str) -> str | None:
        """Convierte un valor individual a string"""
        try:
            if pd.isna(value) or str(value).strip().lower() in {
                "nan",
                "nat",
                "none",
                "",
            }:
                return None
            return str(value)
        except Exception:
            return str(value)
