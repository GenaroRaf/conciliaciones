from io import BytesIO
from typing import Any

import pandas as pd
from k_link.db.core import ObjectId
from k_link.db.daos import ProjectDAO
from k_link.db.models import Project
from k_link.extensions.conciliation_type import ConciliationType
from k_link.extensions.report_config import HeaderConfig, OrigenColumna, TipoDato
from k_link.tools import env
from loggerk import LoggerK

from conciliaciones.clients.sat.sat_data.kore_filter import KoreFilter, cols_kore_meta
from conciliaciones.clients.sat.sat_data.utils.flatten_dict import flatten_dict
from conciliaciones.clients.services.kore import KoreService
from conciliaciones.utils.completion_handler.airflow_contex_exception import (
    AirflowContexException,
)
from conciliaciones.utils.headers.headers_types import HeadersTypes
from conciliaciones.utils.redis.redis_keys import RedisKeys
from conciliaciones.utils.redis.redis_storage import RedisStorage


class KoreMetaService:
    def __init__(
        self,
        run_id: str,
        project_id_str: str,
        year: int,
        month: int,
        conciliation_type: ConciliationType,
    ) -> None:
        self._project_id_str: str = project_id_str
        self._year: int = year

        self._project_dao = ProjectDAO()
        self._kore_service = KoreService()

        self._logger = LoggerK(self.__class__.__name__)
        self._redis = RedisStorage()
        self._redis_keys = RedisKeys(
            run_id=run_id,
            project_id_str=project_id_str,
            year=year,
            month=month,
            conciliation_type=conciliation_type,
        )
        self._airflow_fail_exception = AirflowContexException(
            year=year,
            month=month,
            project_id=project_id_str,
            run_id=run_id,
            conciliation_type=conciliation_type,
        )
        self._header_types = HeadersTypes(
            run_id=run_id,
            project_id_str=str(project_id_str),
            month=month,
            year=year,
            conciliation_type=conciliation_type,
        )
        self._kore_filter = KoreFilter(
            project_id_str=project_id_str,
        )

    async def get_metadata_pendiente(self, i_e: str) -> None:
        project: Project | None = await self._project_dao.get_by_id(
            item_id=ObjectId(self._project_id_str)
        )

        if project is None:
            self._airflow_fail_exception.handle_and_store_exception(
                f"El proyecto con el id: {self._project_id_str} no existe en la base de datos"
            )
            return

        enterprises: list[str] = project.enterprises

        if not enterprises:
            self._airflow_fail_exception.handle_and_store_exception(
                f"El proyecto con el id: {self._project_id_str} no tiene empresas asociadas"
            )

        meta_pendiente_filter = self._kore_filter.metadata_filter(
            project_type=project.project_type,
            enterprises=enterprises,
            year=self._year,
            is_pendiente=True,
        )

        data_merge = []
        for enterprise in enterprises:
            response = await self._kore_service.aggregate(
                token=env.DEV_TOKEN, rfc=enterprise, filters=meta_pendiente_filter
            )

            data_merge.extend(response["data"])
            self._logger.info(f"Data for {enterprise}: {response['data']}")

        try:
            flat_merged = [flatten_dict(comprobante) for comprobante in data_merge]

            self._logger.info(f"Flat merged: {flat_merged}")
        except ValueError as _:
            self._airflow_fail_exception.handle_and_store_exception(
                "Uno de los comprobantes está dañado, por favor proporcione un diccionario válido."
            )

        df_erp_sat: pd.DataFrame | None = self._redis.get_df(
            redis_key=self._redis_keys.get_sat_erp_redis_key()
        )

        if df_erp_sat is None:
            self._airflow_fail_exception.handle_and_store_exception(
                f"El DataFrame con la key {self._redis_keys.get_sat_erp_redis_key()} no existe en Redis"
            )
            return

        self._logger.error(f"Cantidad de registros en DF ERP SAT: {len(df_erp_sat)}")

        candidato: list[str] = df_erp_sat.filter(
            regex="(?i)RFCReceptor" if i_e == "I" else "(?i)RFCEmisor"
        ).columns.tolist()

        df_meta = pd.DataFrame(flat_merged)
        self._logger.info(f"Cantidad de registros en DF Meta: {len(df_meta)}")
        self._logger.info(f"DF Meta: {df_meta.columns}")

        resultado = pd.DataFrame()
        if not df_meta.empty:
            df_meta: pd.DataFrame = self._kore_filter.transform_metadata_columns(
                df_meta
            )

            # agregar agrupacion por tipo de docto
            resultado = (
                df_meta.groupby("Receptor_Rfc" if i_e == "I" else "Emisor_Rfc")[
                    "TipoComprobante"
                ]
                .agg(lambda x: "RFC con descarga pendiente de " + ", ".join(set(x)))
                .reset_index()
            )
            resultado.rename(
                columns={"TipoComprobante": "Pendientes SAT"}, inplace=True
            )

        if len(candidato) > 0 and not df_meta.empty:
            # Remover duplicados del df_meta por RFC
            rfc_column = (
                cols_kore_meta["receptor_sat"]
                if i_e == "I"
                else cols_kore_meta["emisor_sat"]
            )
            self._logger.info(
                f"Candidato 0: {candidato[0]}, type: {type(candidato[0])}"
            )
            self._logger.info(f"rfc_column: {rfc_column}, type: {type(rfc_column)}")

            # Normalizar columnas
            try:
                df_erp_sat[candidato[0]] = df_erp_sat[candidato[0]].astype(str)
                df_erp_sat[rfc_column] = df_erp_sat[rfc_column].astype(str)
            except Exception:
                self._logger.info("Falló normalización de columnas")

            df_erp_sat = pd.merge(
                left=df_erp_sat,
                right=resultado,
                left_on=candidato[0],
                right_on=rfc_column,
                suffixes=("", ""),
                how="left",
            )

            for col in df_erp_sat.columns:
                if df_erp_sat[col].apply(lambda x: isinstance(x, (list, dict))).any():
                    df_erp_sat[col] = df_erp_sat[col].apply(
                        lambda x: str(x) if isinstance(x, (list, dict)) else x
                    )

            df_erp_sat = df_erp_sat.drop_duplicates()

            self._logger.info(f"df_kore: {df_erp_sat.head()}")

            self._logger.info(f"Vigente: {df_meta[cols_kore_meta['vigente']]}")
        else:
            df_erp_sat[cols_kore_meta["pendientes"]] = "Descarga Completa"

        if not df_erp_sat.empty:
            df_meta: pd.DataFrame = self._kore_filter.filter_df_metadata(
                df_metadata=df_meta
            )

            df_erp_sat[cols_kore_meta["pendientes"]] = df_erp_sat[
                cols_kore_meta["pendientes"]
            ].apply(lambda x: "Descarga Completa" if pd.isna(x) or x is None else x)

            if not df_meta.empty:
                self._logger.info(f"Pendientes: {df_meta.shape[0]}")

                buffer_df: BytesIO = self._redis.set_parquet(df=df_meta)
                self._redis.set(
                    key=self._redis_keys.get_sat_erp_meta_key(), value=buffer_df
                )
        else:
            self._logger.info("Sin pendientes")

        header_meta_data: HeaderConfig = HeaderConfig(
            nombre="Pendientes SAT",
            configuracion_tipo_dato=TipoDato.TEXTO,
            origen=OrigenColumna.LABEL,
            mostrar_reporte=True,
        )

        headers_meta_data: list[HeaderConfig] = [header_meta_data]

        await self._get_metadata_cancelada(
            project_type=project.project_type, enterprises=enterprises
        )

        await self._header_types.save_redis_headers_list(
            redis_key=self._redis_keys.get_headers_validation_meta_data_list_key(),
            headers_list=headers_meta_data,
        )

        self._logger.error(
            f"Cantidad de registros Final en DF ERP SAT: {len(df_erp_sat)}"
        )

        buffer_df: BytesIO = self._redis.set_parquet(df=df_erp_sat)
        self._redis.set(key=self._redis_keys.get_sat_erp_redis_key(), value=buffer_df)

    async def _get_metadata_cancelada(
        self, project_type: str, enterprises: list[str]
    ) -> None:
        meta_cancelada_filter = self._kore_filter.metadata_filter(
            project_type=project_type,
            enterprises=enterprises,
            year=self._year,
            is_pendiente=False,
        )

        data_merge = []
        for enterprise in enterprises:
            response = await self._kore_service.aggregate(
                token=env.DEV_TOKEN, rfc=enterprise, filters=meta_cancelada_filter
            )

            data_merge.extend(response["data"])
            self._logger.info(f"Data for {enterprise}: {response['data']}")

        try:
            flat_merged = [flatten_dict(comprobante) for comprobante in data_merge]

            self._logger.info(f"Flat merged: {flat_merged}")
        except ValueError as _:
            self._airflow_fail_exception.handle_and_store_exception(
                "Uno de los comprobantes está dañado, por favor proporcione un diccionario válido."
            )

        df_meta = pd.DataFrame(flat_merged)

        if not df_meta.empty:
            columnas_iniciales: list[str] = [
                cols_kore_meta["fecha_timbrado"],
                cols_kore_meta["hora_timbrado"],
                cols_kore_meta["fecha_emision"],
                cols_kore_meta["hora_emision"],
                cols_kore_meta["fecha_cancelacion"],
                cols_kore_meta["hora_cancelacion"],
            ]

            resto: dict[str, Any | None] = dict.fromkeys(
                columnas_iniciales + df_meta.columns.tolist()
            )
            df_meta: pd.DataFrame = df_meta[list(resto)]

            df_meta = self._kore_filter.transform_metadata_columns(
                df_meta, is_pendiente=False
            )

            buffer_df: BytesIO = self._redis.set_parquet(df=df_meta)
            self._redis.set(
                key=self._redis_keys.get_sat_erp_meta_cancel_key(), value=buffer_df
            )
