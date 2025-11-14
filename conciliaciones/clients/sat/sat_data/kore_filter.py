from enum import Enum

import pandas as pd
from k_link.db.core import ObjectId
from k_link.db.daos import ProjectDAO
from k_link.db.models import Project
from loggerk import LoggerK

cols_kore_meta = {
    "receptor_sat": "Receptor_Rfc",
    "emisor_sat": "Emisor_Rfc",
    "pendientes": "Pendientes SAT",
    "tipo_comprobante": "TipoComprobante",
    "ultima_actualizacion": "Ultima Actualización",
    "fecha_timbrado": "FechaTimbrado",
    "fecha_cancelacion": "FechaCancelación",
    "fecha_emision": "FechaEmision",
    "hora_timbrado": "HoraTimbrado",
    "hora_cancelacion": "HoraCancelación",
    "hora_emision": "HoraEmision",
    "vigente": "Vigente",
}

tipos = {"I": "Ingreso", "E": "Egreso", "P": "Complemento", "T": "Traslado"}
tipo_comprobante_map = {
    "Clientes": "I",
    "Proveedores": "E",
    "Fiscal": "T",
    "Empleados": "P",
}


class Formatos:
    def formato_utc(self, valor, formato):
        """formatear datetime en formato UTC"""
        return (
            pd.to_datetime(valor, utc=True).strftime(formato.value)
            if not pd.isna(valor)
            else None
        )


class FormatosDate(Enum):
    HORA = "%H:%M:%S"
    FECHA = "%Y-%m-%d"
    FULL = "%Y-%m-%d %H:%M:%S"


class KoreFilter:
    def __init__(
        self,
        project_id_str: str,
    ) -> None:
        self._project_id_str: str = project_id_str
        self._logger = LoggerK(self.__class__.__name__)
        self._formatos = Formatos()
        self._project_dao = ProjectDAO()

    def metadata_filter(
        self,
        project_type: str,
        enterprises: list[str],
        year: int,
        is_pendiente: bool = True,
    ):
        """
        Genera filtro para metadata pendiente o cancelada

        Args:
            year: Año para filtrar
            is_pendiente: True para pendientes (vigentes), False para canceladas
        """
        # Campos base del proyecto
        base_project = {
            "Total": 1,
            "Emisor": 1,
            "Receptor": 1,
            "Vigente": 1,
            "Uuid": 1,
            "FechaEmision": 1,
            "FechaTimbrado": 1,
            "HoraEmision": "$FechaEmision",
            "HoraTimbrado": "$FechaTimbrado",
            "TipoComprobante": 1,
            "Ultima Actualización": "$ProcessorMetadata.LastUpdate",
            "_id": 0,
        }
        if is_pendiente:
            project_fields = {**base_project, "Pendientes SAT": "Descarga Pendiente"}
            vigente_value = True
        else:
            project_fields = {
                **base_project,
                "FechaCancelación": "$Cancelacion.FechaCancelacion",
                "HoraCancelación": "$Cancelacion.FechaCancelacion",
            }
            vigente_value = False

        return [
            {
                "$match": {
                    "Comprobante": False,
                    "Metadata": True,
                    "Vigente": vigente_value,
                    "Emisor.Rfc": {"$in": enterprises},
                    "TipoComprobante": tipo_comprobante_map.get(project_type),
                    "$expr": {
                        "$eq": [
                            {
                                "$year": {
                                    "$toDate": {"$substr": ["$FechaEmision", 0, 10]}
                                }
                            },
                            year,
                        ]
                    },
                }
            },
            {"$project": project_fields},
        ]

    def transform_metadata_columns(
        self, df_meta: pd.DataFrame, is_pendiente: bool = True
    ) -> pd.DataFrame:
        """
        Transforma columnas de metadata para pendiente o cancelada

        Args:
            df_meta: DataFrame con metadata
            is_pendiente: True para pendientes, False para canceladas
        """

        columns_in_df = df_meta.columns.tolist()

        # Transformaciones base (comunes para ambos tipos)
        if cols_kore_meta["vigente"] in columns_in_df:
            df_meta[cols_kore_meta["vigente"]] = (
                df_meta[cols_kore_meta["vigente"]]
                .astype(bool)
                .map({True: "Vigente", False: "Cancelado"})
            )

        if cols_kore_meta["tipo_comprobante"] in columns_in_df:
            df_meta[cols_kore_meta["tipo_comprobante"]] = df_meta[
                cols_kore_meta["tipo_comprobante"]
            ].apply(lambda x: tipos[x] if not pd.isna(x) else None)

        if cols_kore_meta["ultima_actualizacion"] in columns_in_df:
            df_meta[cols_kore_meta["ultima_actualizacion"]] = df_meta[
                cols_kore_meta["ultima_actualizacion"]
            ].apply(self._formatos.formato_utc, args=(FormatosDate.FULL,))

        if cols_kore_meta["fecha_timbrado"] in columns_in_df:
            df_meta[cols_kore_meta["fecha_timbrado"]] = df_meta[
                cols_kore_meta["fecha_timbrado"]
            ].apply(self._formatos.formato_utc, args=(FormatosDate.FECHA,))

        if cols_kore_meta["fecha_emision"] in columns_in_df:
            df_meta[cols_kore_meta["fecha_emision"]] = df_meta[
                cols_kore_meta["fecha_emision"]
            ].apply(self._formatos.formato_utc, args=(FormatosDate.FECHA,))

        if cols_kore_meta["hora_timbrado"] in columns_in_df:
            df_meta[cols_kore_meta["hora_timbrado"]] = df_meta[
                cols_kore_meta["hora_timbrado"]
            ].apply(self._formatos.formato_utc, args=(FormatosDate.HORA,))

        if cols_kore_meta["hora_emision"] in columns_in_df:
            df_meta[cols_kore_meta["hora_emision"]] = df_meta[
                cols_kore_meta["hora_emision"]
            ].apply(self._formatos.formato_utc, args=(FormatosDate.HORA,))

        if is_pendiente:
            self._logger.info(f"Vigente: {df_meta[cols_kore_meta['vigente']]}")
        else:
            # Para metadata cancelada - agregar campos de cancelación
            if cols_kore_meta["fecha_cancelacion"] in columns_in_df:
                df_meta[cols_kore_meta["fecha_cancelacion"]] = df_meta[
                    cols_kore_meta["fecha_cancelacion"]
                ].apply(self._formatos.formato_utc, args=(FormatosDate.FECHA,))

            if cols_kore_meta["hora_cancelacion"] in columns_in_df:
                df_meta[cols_kore_meta["hora_cancelacion"]] = df_meta[
                    cols_kore_meta["hora_cancelacion"]
                ].apply(self._formatos.formato_utc, args=(FormatosDate.HORA,))

            self._logger.info(f"Cancelada: {df_meta[cols_kore_meta['vigente']]}")

        return df_meta

    def filter_df_metadata(self, df_metadata: pd.DataFrame) -> pd.DataFrame:
        project: Project | None = self._project_dao.get_by_id_sync(
            item_id=ObjectId(self._project_id_str)
        )

        if not project:
            return df_metadata

        filter_config: dict[str, str] = {
            "Proveedores": "Receptor_Rfc",
            "Clientes": "Emisor_Rfc",
        }

        rfc_column: str | None = filter_config.get(project.project_type)

        if rfc_column is None:
            self._logger.warning(
                f"Tipo de proyecto no reconocido: {project.project_type}"
            )
            return df_metadata

        if rfc_column and rfc_column in df_metadata.columns:
            df_metadata = df_metadata[df_metadata[rfc_column].isin(project.enterprises)]
            self._logger.info(f"Filtrado aplicado para {project.project_type}")
        else:
            self._logger.warning(f"{rfc_column} no encontrado en DataFrame")

        return df_metadata
