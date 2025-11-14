import typing
from io import BytesIO

import pandas as pd
from k_link.db.core import ObjectId
from k_link.db.daos import ERPFilesDAO, LinkServicesDAO, ProjectDAO, ReportCatalogDAO
from k_link.db.models import ERPFiles, LinkServices, ReportCatalog
from k_link.db.models.project import Project
from k_link.extensions.conciliation_type import ConciliationType
from k_link.extensions.pivot_k import PivoteKHeader, PivotK
from k_link.extensions.report_config import KReportsRequest, ReportConfig
from k_link.extensions.report_config.header_config import (
    HeaderConfig,
)
from loggerk import LoggerK

from conciliaciones.clients.erp.erp_data.get_pivot_k import PivoteKManager
from conciliaciones.models.shared import HowType
from conciliaciones.utils.completion_handler.airflow_contex_exception import (
    AirflowContexException,
)
from conciliaciones.utils.redis.redis_keys import RedisKeys
from conciliaciones.utils.redis.redis_storage import RedisStorage

ERP_FILES_DAO = ERPFilesDAO()
PROJECT_DAO = ProjectDAO()
LINK_SERVICES_DAO = LinkServicesDAO()

pivot_map: dict[PivoteKHeader, str] = {
    PivoteKHeader.UUID: "uuids",
    PivoteKHeader.SERIE_FOLIO: "serieFolio",
    PivoteKHeader.FOLIO: "folios",
}


class Conciliaciones:
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
        self.month: int = month
        self.year: int = year
        self.redis = RedisStorage()
        self.shared = RedisKeys(
            run_id=run_id,
            project_id_str=self.project_id_str,
            month=self.month,
            year=self.year,
            conciliation_type=conciliation_type,
        )
        self._airflow_fail_exception = AirflowContexException(
            run_id=run_id,
            project_id=project_id_str,
            year=year,
            month=month,
            conciliation_type=conciliation_type,
        )

    async def get_estrategia_pivotes_k(self) -> list[str]:
        """
        Obtiene las estrategias de los pivotes K y las devuelve como una lista de strings.
        Lanza una excepción si no se encuentran pivotes K.
        """
        pivots_k_list: list[PivotK] = await self.get_pivotes_k()

        # Extraer y devolver las estrategias de los pivotes
        strategy_pivot_list = [pivote.pivote_k_header.value for pivote in pivots_k_list]

        self._logger.info(f"Pivot list: {strategy_pivot_list}")

        return strategy_pivot_list

    # Debería regresar un solo elemento o una lista de PivoteK
    async def get_pivotes_k(self) -> list[PivotK]:
        erp_files_data: ERPFiles | None = await ERP_FILES_DAO.get(
            project_id=self.project_id
        )

        if erp_files_data is None:
            self._airflow_fail_exception.handle_and_store_exception(
                f"No hay configuración de ERPFiles para el proyecto: {self.project_id}"
            )

        pivot_k = erp_files_data.pivot_k

        return pivot_k

    async def conciliacion(self, pivotes: list[PivoteKHeader]) -> None:
        dataframe_erp: pd.DataFrame | None = self.redis.get_df(
            redis_key=self.shared.get_erp_redis_key()
        )

        if dataframe_erp is None:
            self._airflow_fail_exception.handle_and_store_exception(
                f"No hay informacion para el DataFrame con la key {self.shared.get_erp_redis_key()}"
            )

        self._logger.info(f"Registros dataFrame ERP: {len(dataframe_erp)}")

        link_services: LinkServices | None = await LINK_SERVICES_DAO.get(
            project_id=self.project_id
        )

        if link_services is None:
            self._airflow_fail_exception.handle_and_store_exception(
                f"No hay configuración de LinkServices para el proyecto: {self.project_id_str}"
            )

        report_config: ReportConfig | None = link_services.report_config

        if not report_config:
            self._airflow_fail_exception.handle_and_store_exception(
                f"No hay configuración de ReportConfig para el proyecto: {self.project_id_str}"
            )

        report_request: KReportsRequest | None = report_config.report_type

        if report_request is None:
            self._airflow_fail_exception.handle_and_store_exception(
                f"No hay configuración de KReportsRequest para el proyecto: {self.project_id_str}"
            )

        report_type: ReportCatalog | None = await ReportCatalogDAO().get_by_id(
            item_id=report_request.report_id
        )

        if report_type is None:
            self._airflow_fail_exception.handle_and_store_exception(
                f"No hay configuracion de ReportCatalog para el ID: {report_request.report_id}"
            )

        strategies = report_type.strategies

        self._logger.info(f"Report type strategies: {strategies}")

        if strategies is None:
            self._airflow_fail_exception.handle_and_store_exception(
                f"No hay estrategias configuradas para el reporte con ID: {report_request.report_id}"
            )

        erp_copy = dataframe_erp.copy()
        list_only_erp = []
        list_erp_sat = []
        erp_sat_merge = pd.DataFrame()  # Initialize with an empty DataFrame
        df_erp_sat_concat: pd.DataFrame = pd.DataFrame()

        for idx, pivote in enumerate(pivotes):
            pivote_k_column_name = PivoteKManager.get_pivote_k_header_name(
                strategy=pivote
            )
            pivote_key = pivote.value.lower()
            self._logger.info(f"Type: {pivote_key}")
            self._logger.info(f"Pivote strategy: {pivote_key}")

            if pivote_key not in strategies:
                self._airflow_fail_exception.handle_and_store_exception(
                    f"Estrategia {pivote_key} no encontrada en las estrategias del reporte con ID: {report_request.report_id}."
                )

            dataframe_sat: pd.DataFrame | None = self.redis.get_df(
                redis_key=self.shared.get_sat_erp_strategy_redis_key(pivote)
            )

            self._logger.info(f"Headers DataFrame ERP: {erp_copy.columns.tolist()}")
            self._logger.info(f"DataFrame SAT: {dataframe_sat}")

            if dataframe_sat is None or dataframe_sat.empty:
                self._logger.error("Dataframe del SAT vacio, no se hará conciliación")
                df_erp_sat_concat: pd.DataFrame = erp_copy
            else:
                self._logger.info(
                    f"Headers DataFrame SAT: {dataframe_sat.columns.tolist()}"
                )

                # Usa el df del erp para la 1ra iteacion
                if idx == 0:
                    self._logger.info(f"DF erp: {erp_copy}")
                    erp_only, erp_sat, erp_sat_merge = self.merge_frames_split(
                        dataframe_erp=erp_copy,
                        dataframe_sat=dataframe_sat,
                        left_on=pivote_k_column_name,
                        rigth_on=strategies[pivote_key],
                        how="outer",
                        pivote_key=pivote_key,
                    )
                # Para 1+ en adelante se hace el merge con only_erp con el dataframe_sat de la iteracion(pivote)
                else:
                    self._logger.info(f"Df erp: {list_only_erp[idx - 1]}")
                    erp_only, erp_sat, _ = self.merge_frames_split(
                        dataframe_erp=list_only_erp[idx - 1],
                        dataframe_sat=dataframe_sat,
                        left_on=pivote_k_column_name,
                        rigth_on=strategies[pivote_key],
                        pivote_key=pivote_key,
                        how="outer",
                    )

                self._logger.info(f"Df sat: {dataframe_sat}")

                self._logger.info(f"ERP Only Iteracion {idx}: {len(erp_only)}")
                self._logger.info(f"ERP SAT Iteracion {idx}: {len(erp_sat)}")

                list_only_erp.append(erp_only)
                list_erp_sat.append(erp_sat)

                if len(pivotes) == 1:
                    df_erp_sat_concat = erp_sat_merge
                else:
                    df_erp_sat_concat = pd.concat(list_erp_sat, ignore_index=True)

            self._logger.info(f"ERP SAT Final: {df_erp_sat_concat.columns.tolist()}")
            self._logger.info(
                f"ERP SAT final - numero registros: {len(df_erp_sat_concat)}"
            )

        df_erp_sat_concat = self._add_headers_relacionados(
            df_erp_sat_concat=df_erp_sat_concat
        )

        self._logger.info(f"erp + sat columns: {df_erp_sat_concat.columns}")

        self._logger.info(f"DataFrame ERP SAT - numero registros: {df_erp_sat_concat}")
        buffer_df: BytesIO = self.redis.set_parquet(df=df_erp_sat_concat)
        self.redis.set(
            key=self.shared.get_sat_erp_redis_key(),
            value=buffer_df,
        )

    async def validate_project_type_for_reporting(
        self, tipo_reporte: str | None = None
    ) -> None:
        self._logger.warning(f"Tipo de reporte: {tipo_reporte}")
        project: Project | None = await PROJECT_DAO.get_by_id(
            ObjectId(self.project_id_str)
        )

        if project is None:
            self._airflow_fail_exception.handle_and_store_exception(
                f"Proyecto no encontrado con ID: {self.project_id_str}"
            )

        project_type = project.project_type

        if (
            project_type not in ["Clientes", "Fiscal", "Empleados"]
        ) or tipo_reporte == "unitario":
            self._logger.info(
                f"El tipo de proyecto es : {project_type}, se salta la validación"
            )
            return

        self._logger.info(
            f"El tipo de proyecto es : {project_type}, se hace concat de los DF para el reporte"
        )
        redis_key_erp = self.shared.get_sat_erp_redis_key()

        df_erp_sat: pd.DataFrame | None = self.redis.get_df(redis_key=redis_key_erp)

        if df_erp_sat is None:
            self._airflow_fail_exception.handle_and_store_exception(
                f"DataFrame no encontrado con la clave: {redis_key_erp}"
            )

        self._logger.info(f"DataFrame ERP SAT: {df_erp_sat}")
        self._logger.info(f"DataFrame ERP SAT - numero registros: {len(df_erp_sat)}")

        redis_key_sat_no_erp_periodo = self.shared.get_sat_no_erp_periodo_key()

        df_sat_no_erp_periodo: pd.DataFrame | None = self.redis.get_df(
            redis_key=redis_key_sat_no_erp_periodo
        )

        if df_sat_no_erp_periodo is None:
            self._airflow_fail_exception.handle_and_store_exception(
                f"DataFrame no encontrado con la clave: {redis_key_sat_no_erp_periodo}"
            )

        self._logger.info(f"DataFrame SAT no ERP periodo: {df_sat_no_erp_periodo}")
        self._logger.info(
            f"DataFrame SAT no ERP periodo - numero registros: {len(df_sat_no_erp_periodo)}"
        )

        df_erp_sat = pd.concat([df_erp_sat, df_sat_no_erp_periodo], axis=0)

        for col in df_erp_sat.columns:
            if df_erp_sat[col].apply(lambda x: isinstance(x, (list, dict))).any():
                df_erp_sat[col] = df_erp_sat[col].apply(
                    lambda x: str(x) if isinstance(x, (list, dict)) else x
                )

        df_erp_sat = df_erp_sat.drop_duplicates()

        self._logger.info(f"DataFrame ERP SAT concatenado: {df_erp_sat}")
        self._logger.info(
            f"DataFrame ERP SAT concatenado - numero registros: {len(df_erp_sat)}"
        )

        buffer_df: BytesIO = self.redis.set_parquet(df=df_erp_sat)
        self.redis.set(
            key=redis_key_erp,
            value=buffer_df,
        )

    @staticmethod
    def merge_frames_split(
        dataframe_erp: pd.DataFrame,
        dataframe_sat: pd.DataFrame,
        left_on: str,
        rigth_on: str,
        pivote_key: str,
        how: HowType = "outer",
    ) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        args: tuple[HowType] = typing.get_args(tp=HowType)
        if how not in args:
            raise ValueError(f"Invalid how parameter. Must be one of {args}")

        if pivote_key == "folio":
            dataframe_sat[left_on] = dataframe_sat[rigth_on].astype("Int64")
            dataframe_sat[rigth_on] = dataframe_sat[rigth_on].astype("string")

            dataframe_sat[rigth_on] = dataframe_sat[rigth_on].astype("Int64")
            dataframe_sat[rigth_on] = dataframe_sat[rigth_on].astype("string")

        merged_df = pd.merge(
            left=dataframe_erp,
            right=dataframe_sat,
            left_on=left_on,
            right_on=rigth_on,
            how=how,
            indicator=True,
        )

        erp_only = merged_df[merged_df["_merge"] == "left_only"].drop(
            columns=["_merge"]
        )
        erp_sat = merged_df[merged_df["_merge"] == "both"].drop(columns=["_merge"])

        return erp_only, erp_sat, merged_df

    def _add_headers_relacionados(
        self, df_erp_sat_concat: pd.DataFrame
    ) -> pd.DataFrame:
        list_headers_relacionados = [
            "relacionado_tipoRelacion",
            "relacionado_comprobante_uuid",
            "relacionado_comprobante_serie",
            "relacionado_comprobante_folio",
            "relacionado_comprobante_serieFolio",
            "relacionado_comprobante_version",
            "relacionado_comprobante_vigencia",
            "relacionado_comprobante_tipo",
            "relacionado_comprobante_metodoPago",
            "relacionado_comprobante_fechaEmision",
            "relacionado_comprobante_fechaCancelacion",
            "relacionado_comprobante_fechaTimbrado",
            "relacionado_comprobante_rfcEmisor",
            "relacionado_comprobante_nombreEmisor",
            "relacionado_comprobante_regimenEmisor",
            "relacionado_comprobante_factAtrAdquirentEmisor",
            "relacionado_comprobante_rfcReceptor",
            "relacionado_comprobante_nombreReceptor",
            "relacionado_comprobante_domicilioFiscal",
            "relacionado_comprobante_ResidenciaFiscal",
            "relacionado_comprobante_NumRegIdTrib",
            "relacionado_comprobante_regimenReceptor",
            "relacionado_comprobante_usoCfdi",
            "relacionado_comprobante_moneda",
            "relacionado_comprobante_formaPago",
            "relacionado_comprobante_Periodicidad",
            "relacionado_comprobante_Meses",
            "relacionado_comprobante_Anio",
            "relacionado_comprobante_condicionesPago",
            "relacionado_comprobante_tipoRelacion",
            "relacionado_comprobante_tipoComplemento",
            "relacionado_comprobante_descuento",
            "relacionado_comprobante_descuentoMXN",
            "relacionado_comprobante_tipoCambio",
            "relacionado_comprobante_subtotal",
            "relacionado_comprobante_total",
            "relacionado_comprobante_subtotalMXN",
            "relacionado_comprobante_totalMXN",
            "relacionado_comprobante_subtotalDescuento",
            "relacionado_comprobante_subtotalDescuentoMxn",
        ]

        df_concat_relacionados = df_erp_sat_concat.reindex(
            columns=list(df_erp_sat_concat.columns)
            + [
                col
                for col in list_headers_relacionados
                if col not in df_erp_sat_concat.columns
            ]
        )

        return df_concat_relacionados

    async def _filtrar_columnas_custom(
        self, df_erp_sat_concat: pd.DataFrame, headers_custom: list[HeaderConfig]
    ) -> pd.DataFrame:
        headers_custom_names: list[str] = [
            header.nombre
            for header in headers_custom
            if header.mostrar_reporte and header.nombre in df_erp_sat_concat
        ]

        headers_df_unicos: set = set(df_erp_sat_concat.columns)
        headers_custom_unicos: set = set(headers_custom_names)

        headers_filtrados: set = headers_df_unicos - headers_custom_unicos

        self._logger.info(f"Headers omitidos: {headers_filtrados}")

        return df_erp_sat_concat[headers_custom_names]
