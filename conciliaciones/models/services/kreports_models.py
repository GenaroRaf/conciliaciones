from enum import Enum
from typing import Generic, TypeVar

from k_link.utils.pydantic_types import Date
from pydantic import BaseModel

T = TypeVar("T")
M = TypeVar("M")


class KReportsResponse(BaseModel, Generic[T, M]):
    success: bool
    detail: str
    data: T = None  # type: ignore
    metadata: M = None  # type: ignore


class FilterDateBy(Enum):
    EMISION = "emision"
    PAGO = "pago"


class PagosReportType(Enum):
    ONLY_UUID = "OnlyUUID"
    PAGO_AND_ORIGIN_UUID = "PagoAndOriginUUID"


class ReportFilters(BaseModel):
    startDate: Date | str | None = None
    endDate: Date | str | None = None
    folio: list[str] | None = None
    serie: str | None = None
    uuids: list[str] | None = None
    skip: int = 0
    limit: int = 0
    sortKey: str = ""
    sortDirection: str = "1"
    rfcEmisor: str | None = None
    rfcReceptor: str | None = None
    folios: list[str] | None = None
    series: list[str] | None = None
    notFolios: list[str] | None = None
    notSeries: list[str] | None = None
    notUuids: list[str] | None = None


class ReportFiltersExcel(ReportFilters):
    emails: list[str] = []
    includedHeaders: list[str] = []
    excludedHeaders: list[str] = []


class ReportPagosFilters(ReportFilters):
    reportType: PagosReportType = PagosReportType.ONLY_UUID
    emails: list[str] = []


class ReportNominaFilters(ReportFilters):
    filterDateBy: FilterDateBy


class VersionNomina(Enum):
    N11 = "1.1"
    N12 = "1.2"


class Vigencia(Enum):
    VIGENTE = "Vigente"
    CANCELADO = "Cancelado"


class TipoComprobante(Enum):
    INGRESO = "I"
    EGRESO = "E"
    TRASLADO = "T"
    NOMINA = "N"
    PAGO = "P"


class NominaItem(BaseModel):
    # El mapeado de este modelo no está completo, terminar de mapear los campos restantes
    # El modelo completo se puede encontrar en kreports como ComprobanteNomina
    uuid: str
    version: dict
    rfc_emisor: str
    nombre_emisor: str
    regimen_emisor: str
    rfc_receptor: str
    nombre_receptor: str
    regimen_receptor: str
    fecha_emision: Date
    folio: str
    vigencia: Vigencia
    tipo: TipoComprobante
    total: float
    subtotal: float
    total_mxn: float
    subtotal_mxn: float
    version_nomina: VersionNomina
    tipo_nomina: str
    fecha_pago: Date
    fecha_inicial_pago: Date
    fecha_final_pago: Date
    num_dias_pagados: float
    total_percepciones: float
    total_deducciones: float
    total_otros_pagos: float
