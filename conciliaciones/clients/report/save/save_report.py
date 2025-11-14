import json
from collections.abc import Hashable
from datetime import datetime
from io import BytesIO
from typing import Any

import numpy as np
import pandas as pd
from k_link.db.core import ObjectId
from k_link.extensions import ConciliationType
from k_link.extensions.influx import InfluxLogItem, Strategies
from k_link.extensions.report_result import ReportMetadata, ReportOutputType
from loggerk import LoggerK
from pandas import DataFrame

from conciliaciones.clients.report.utils.report_data_handler import ReportDataHandler
from conciliaciones.utils.completion_handler.airflow_contex_exception import (
    AirflowContexException,
)
from conciliaciones.utils.redis.redis_keys import RedisKeys
from conciliaciones.utils.redis.redis_storage import RedisStorage


class SaveReport:
    PIVOTE_K_UUID = "Pivote K UUID"
    PIVOTE_K_FOLIO = "Pivote K FOLIO"
    PIVOTE_K_SERIE_FOLIO = "Pivote K SERIE_FOLIO"
    CONCILIADO_STATUS = "Estatus conciliado"

    reporte_data: ReportDataHandler

    def __init__(
        self,
        run_id: str,
        project_id_str: str,
        month: int,
        year: int,
        conciliation_type: ConciliationType,
    ) -> None:
        self._logger = LoggerK(self.__class__.__name__)
        self.run_id: str = run_id
        self.project_id_str: str = project_id_str
        self.project_id = ObjectId(project_id_str)
        self.month: int = month
        self.year: int = year
        self._conciliation_type: ConciliationType = conciliation_type

        self.redis = RedisStorage()

        self.redis_keys = RedisKeys(
            run_id=run_id,
            project_id_str=self.project_id_str,
            month=self.month,
            year=self.year,
            conciliation_type=self._conciliation_type,
        )
        self._airflow_fail_exception = AirflowContexException(
            year=year,
            month=month,
            project_id=project_id_str,
            run_id=run_id,
            conciliation_type=conciliation_type,
        )

    async def save_files(self) -> None:
        # Instancia de report_handler
        self.get_report_data_handler()

        # Recupero excel buffer
        excel_buffer_key: str = self.redis_keys.get_excel_buffer_key()
        excel_buffer: BytesIO | None = self.redis.get(
            key=excel_buffer_key, object_type=BytesIO
        )

        if excel_buffer is None:
            self._airflow_fail_exception.handle_and_store_exception(
                f"No se encontró el buffer de Excel para el proyecto: {self.project_id} en la Task de guardar reporte."
            )

        workbook: dict[str, DataFrame] = pd.read_excel(excel_buffer, sheet_name=None)

        def parse_value(v):
            res = v
            if isinstance(v, (pd.Timestamp, datetime)):
                res = v.isoformat()

            if pd.isna(res):
                res = None
            return res

        workbook_dict: dict[str, list[dict[Hashable, Any]]] = {
            sheetname: df.map(parse_value)
            .replace({np.nan: None})
            .to_dict(orient="records")
            for sheetname, df in workbook.items()
        }

        json_str: str = json.dumps(workbook_dict)

        with BytesIO() as json_buffer:
            json_buffer.write(json_str.encode("utf-8"))
            json_buffer.seek(0)

            excel_buffer.seek(0)

            find_report: ReportMetadata = (
                await self.reporte_data.get_info_metadata_report()
            )

            creation_date = find_report.creation_date

            if creation_date is None:
                raise ValueError("La fecha de creación del reporte es None")

            # Guardar en s3 archivo excel
            final_path = await self.reporte_data.save_s3_report(
                excel_buffer=excel_buffer,
                file_type=ReportOutputType.EXCEL,
                conciliacion_type=self._conciliation_type,
                create_execution_date=creation_date,
            )
            await self.reporte_data.save_mongo_report(
                final_path=final_path,
                file_type=ReportOutputType.EXCEL,
            )

            # Guardar archivo json
            final_path: str = await self.reporte_data.save_s3_report(
                excel_buffer=json_buffer,
                file_type=ReportOutputType.JSON,
                conciliacion_type=self._conciliation_type,
                create_execution_date=creation_date,
            )
            await self.reporte_data.save_mongo_report(
                final_path=final_path,
                file_type=ReportOutputType.JSON,
            )
        # self.send_metrics()

    def get_report_data_handler(self) -> None:
        """Obtiene el manejador de datos del reporte."""
        self.reporte_data = ReportDataHandler(
            run_id=self.run_id,
            project_id_str=self.project_id_str,
            month=self.month,
            year=self.year,
            conciliation_type=self._conciliation_type,
        )

    def send_metrics(self) -> None:
        df_erp_key = self.redis_keys.get_erp_redis_key()
        df_erp = self.redis.get(df_erp_key, DataFrame)
        df_sat_erp_key = self.redis_keys.get_sat_erp_redis_key()
        df_sat_erp = self.redis.get(df_sat_erp_key, DataFrame)
        ##
        metrics_key = self.redis_keys.get_metrics_redis_key()
        metrics_log = self.redis.get(metrics_key, InfluxLogItem)

        if metrics_log is None:
            raise ValueError("Metricas vacias")

        if df_erp is None:
            raise ValueError("Dataframe erp vacío")

        if df_sat_erp is None:
            raise ValueError("Dataframe df_sat_erp is None")

        if self.CONCILIADO_STATUS not in df_sat_erp.columns:
            return
        ## Se calculan los conciliados y no conciliados totales
        conciliado_total = (df_sat_erp[self.CONCILIADO_STATUS] == "Conciliado").sum()
        no_conciliado_total = (
            df_sat_erp[self.CONCILIADO_STATUS] == "No Conciliado"
        ).sum()
        metrics_log.registers_metrics[Strategies.TOTAL].conciliated = int(
            conciliado_total
        )
        metrics_log.registers_metrics[Strategies.TOTAL].not_conciliated = int(
            no_conciliado_total
        )
        metrics_log.registers_metrics[Strategies.TOTAL].percentage_conciliated = float(
            conciliado_total / len(df_sat_erp) * 100
        )
        metrics_log.registers_metrics[
            Strategies.TOTAL
        ].percentage_not_conciliated = float(
            no_conciliado_total / len(df_sat_erp) * 100
        )

        ##Se calculan los conciliados y no conciliados por estrategia
        if self.PIVOTE_K_UUID in df_sat_erp.columns:
            conciliado = (
                (df_sat_erp[f"(Valido) {self.PIVOTE_K_UUID}"] == True)
                & (df_sat_erp[self.CONCILIADO_STATUS] == "Conciliado")
            ).sum()
            no_conciliado = (
                (df_sat_erp[f"(Valido) {self.PIVOTE_K_UUID}"] == True)
                & (df_sat_erp[self.CONCILIADO_STATUS] == "No Conciliado")
            ).sum()
            metrics_log.registers_metrics[Strategies.UUID].conciliated = int(conciliado)
            metrics_log.registers_metrics[Strategies.UUID].not_conciliated = int(
                no_conciliado
            )
            metrics_log.registers_metrics[
                Strategies.UUID
            ].percentage_conciliated = float(conciliado / len(df_sat_erp) * 100)
            metrics_log.registers_metrics[
                Strategies.UUID
            ].percentage_not_conciliated = float(no_conciliado / len(df_sat_erp) * 100)
        if self.PIVOTE_K_FOLIO in df_sat_erp.columns:
            conciliado = (
                (df_sat_erp[f"(Valido) {self.PIVOTE_K_FOLIO}"] == True)
                & (df_sat_erp[self.CONCILIADO_STATUS] == "Conciliado")
            ).sum()
            no_conciliado = (
                (df_sat_erp[f"(Valido) {self.PIVOTE_K_FOLIO}"] == True)
                & (df_sat_erp[self.CONCILIADO_STATUS] == "No Conciliado")
            ).sum()
            metrics_log.registers_metrics[Strategies.FOLIO].conciliated = int(
                conciliado
            )
            metrics_log.registers_metrics[Strategies.FOLIO].not_conciliated = int(
                no_conciliado
            )
            metrics_log.registers_metrics[
                Strategies.FOLIO
            ].percentage_conciliated = float(conciliado / len(df_sat_erp) * 100)
            metrics_log.registers_metrics[
                Strategies.FOLIO
            ].percentage_not_conciliated = float(no_conciliado / len(df_sat_erp) * 100)
        if self.PIVOTE_K_SERIE_FOLIO in df_sat_erp.columns:
            conciliado = (
                (df_sat_erp[f"(Valido) {self.PIVOTE_K_SERIE_FOLIO}"] == True)
                & (df_sat_erp[self.CONCILIADO_STATUS] == "Conciliado")
            ).sum()
            no_conciliado = (
                (df_sat_erp[f"(Valido) {self.PIVOTE_K_SERIE_FOLIO}"] == True)
                & (df_sat_erp[self.CONCILIADO_STATUS] == "No Conciliado")
            ).sum()
            metrics_log.registers_metrics[Strategies.SERIE_FOLIO].conciliated = int(
                conciliado
            )
            metrics_log.registers_metrics[Strategies.SERIE_FOLIO].not_conciliated = int(
                no_conciliado
            )
            metrics_log.registers_metrics[
                Strategies.SERIE_FOLIO
            ].percentage_conciliated = float(conciliado / len(df_sat_erp) * 100)
            metrics_log.registers_metrics[
                Strategies.SERIE_FOLIO
            ].percentage_not_conciliated = float(no_conciliado / len(df_sat_erp) * 100)
        self.redis.set(
            key=self.redis_keys.get_metrics_redis_key(),
            value=metrics_log,
        )
