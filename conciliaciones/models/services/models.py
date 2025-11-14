# pyright: reportCallIssue=false

from enum import Enum
from typing import Annotated, Any, Literal, Optional

from k_link.utils.pydantic_types import Date
from pydantic import BaseModel, Field

# Enums


# Models
class AccionesOTitulosNomina(BaseModel):
    precioAlOtorgarse: float
    valorMercado: float


class BaseBodyExcelHeaderComprobanteRelacionadosSabana(BaseModel):
    advancedFilter: Annotated[Optional[Any], Field(exclude_none=True)] = None
    emails: list[str]
    endDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    excludedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    folios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    includedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    includedMetodosPago: list[str]
    limit: Annotated[Optional[int], Field(exclude_none=True)] = None
    notFolios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSerieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSeries: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notUuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    rfcEmisor: Annotated[Optional[str], Field(exclude_none=True)] = None
    rfcReceptor: Annotated[Optional[str], Field(exclude_none=True)] = None
    serieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    series: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    skip: Annotated[Optional[int], Field(exclude_none=True)] = None
    sortDirection: Annotated[Optional[str], Field(exclude_none=True)] = None
    sortKey: Annotated[Optional[str], Field(exclude_none=True)] = None
    startDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    uuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None


class BaseBodyHeaderComprobanteRelacionadosSabana(BaseModel):
    advancedFilter: Annotated[Optional[Any], Field(exclude_none=True)] = None
    endDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    excludedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    folios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    includedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    includedMetodosPago: list[str]
    limit: Annotated[Optional[int], Field(exclude_none=True)] = None
    notFolios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSerieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSeries: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notUuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    rfcEmisor: Annotated[Optional[str], Field(exclude_none=True)] = None
    rfcReceptor: Annotated[Optional[str], Field(exclude_none=True)] = None
    serieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    series: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    skip: Annotated[Optional[int], Field(exclude_none=True)] = None
    sortDirection: Annotated[Optional[str], Field(exclude_none=True)] = None
    sortKey: Annotated[Optional[str], Field(exclude_none=True)] = None
    startDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    uuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None


class BaseBodyHeaderComprobanteRelacionadosTidy(BaseModel):
    advancedFilter: Annotated[Optional[Any], Field(exclude_none=True)] = None
    endDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    excludedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    folios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    includedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    includedMetodosPago: list[str]
    limit: Annotated[Optional[int], Field(exclude_none=True)] = None
    notFolios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSerieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSeries: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notUuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    rfcEmisor: Annotated[Optional[str], Field(exclude_none=True)] = None
    rfcReceptor: Annotated[Optional[str], Field(exclude_none=True)] = None
    serieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    series: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    skip: Annotated[Optional[int], Field(exclude_none=True)] = None
    sortDirection: Annotated[Optional[str], Field(exclude_none=True)] = None
    sortKey: Annotated[Optional[str], Field(exclude_none=True)] = None
    startDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    uuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None


class BodyDownloadReport(BaseModel):
    _id: str
    downloaded: bool


class BodyDownloadReportByPath(BaseModel):
    bucket_path: str
    id_report: str


class BodyReports(BaseModel):
    Additional: Annotated[Optional[Any], Field(exclude_none=True)] = None
    _id: Annotated[Optional[str], Field(exclude_none=True)] = None


class BucketFile(BaseModel):
    additional_information: str
    file_paths: list[str]
    zip_path: str


class CartaPorte_cartaPorteZipperRequest(BaseModel):
    Additional: Annotated[Optional[Any], Field(exclude_none=True)] = None
    Emisor_Rfc: Annotated[Optional[str], Field(exclude_none=True)] = None
    FechaEmision: Any
    Receptor_Rfc: Annotated[Optional[str], Field(exclude_none=True)] = None
    emails: list[str]


class CartaPorte_createCartaPorteReportExcelRequest(BaseModel):
    Additional: Annotated[Optional[Any], Field(exclude_none=True)] = None
    Emisor_Rfc: Annotated[Optional[str], Field(exclude_none=True)] = None
    FechaEmision: Any
    Receptor_Rfc: Annotated[Optional[str], Field(exclude_none=True)] = None
    emails: list[str]
    excludedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    includedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None


class CartaPorte_filterRequest(BaseModel):
    Additional: Annotated[Optional[Any], Field(exclude_none=True)] = None
    Emisor_Rfc: Annotated[Optional[str], Field(exclude_none=True)] = None
    FechaEmision: Any
    Receptor_Rfc: Annotated[Optional[str], Field(exclude_none=True)] = None
    hidden: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    show: Annotated[Optional[list[str]], Field(exclude_none=True)] = None


class ExcelizeFont(BaseModel):
    bold: Annotated[Optional[bool | None], Field(exclude_none=True)] = None
    color: Annotated[Optional[str | None], Field(exclude_none=True)] = None
    colorIndexed: Annotated[Optional[int | None], Field(exclude_none=True)] = None
    colorTheme: Annotated[Optional[int | None], Field(exclude_none=True)] = None
    colorTint: Annotated[Optional[float | None], Field(exclude_none=True)] = None
    family: Annotated[Optional[str | None], Field(exclude_none=True)] = None
    italic: Annotated[Optional[bool | None], Field(exclude_none=True)] = None
    size: Annotated[Optional[float | None], Field(exclude_none=True)] = None
    strike: Annotated[Optional[bool | None], Field(exclude_none=True)] = None
    underline: Annotated[Optional[str | None], Field(exclude_none=True)] = None
    vertAlign: Annotated[Optional[str | None], Field(exclude_none=True)] = None


class ExcelizeFill(BaseModel):
    color: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    pattern: Annotated[Optional[int | None], Field(exclude_none=True)] = None
    shading: Annotated[Optional[int | None], Field(exclude_none=True)] = None
    type: Annotated[Optional[str | None], Field(exclude_none=True)] = None


class ExcelizeBorder(BaseModel):
    color: Annotated[Optional[str | None], Field(exclude_none=True)] = None
    style: Annotated[Optional[int | None], Field(exclude_none=True)] = None
    type: Annotated[Optional[str | None], Field(exclude_none=True)] = None


class ExcelizeProtection(BaseModel):
    hidden: Annotated[Optional[bool], Field(exclude_none=True)] = None
    locked: Annotated[Optional[bool], Field(exclude_none=True)] = None


class ExcelizeAlignment(BaseModel):
    horizontal: Annotated[Optional[str | None], Field(exclude_none=True)] = None
    indent: Annotated[Optional[int | None], Field(exclude_none=True)] = None
    justifyLastLine: Annotated[Optional[bool | None], Field(exclude_none=True)] = None
    readingOrder: Annotated[Optional[int | None], Field(exclude_none=True)] = None
    relativeIndent: Annotated[Optional[int | None], Field(exclude_none=True)] = None
    shrinkToFit: Annotated[Optional[bool | None], Field(exclude_none=True)] = None
    textRotation: Annotated[Optional[int | None], Field(exclude_none=True)] = None
    vertical: Annotated[Optional[str | None], Field(exclude_none=True)] = None
    wrapText: Annotated[Optional[bool | None], Field(exclude_none=True)] = None


class ExcelizeStyle(BaseModel):
    alignment: Annotated[Optional[ExcelizeAlignment], Field(exclude_none=True)] = None
    border: Annotated[Optional[list[ExcelizeBorder]], Field(exclude_none=True)] = None
    customNumFmt: Annotated[Optional[str | None], Field(exclude_none=True)] = None
    decimalPlaces: Annotated[Optional[int | None], Field(exclude_none=True)] = None
    fill: Annotated[Optional[ExcelizeFill], Field(exclude_none=True)] = None
    font: Annotated[Optional[ExcelizeFont], Field(exclude_none=True)] = None
    negRed: Annotated[Optional[bool | None], Field(exclude_none=True)] = None
    numFmt: Annotated[Optional[int | None], Field(exclude_none=True)] = None
    protection: Annotated[Optional[ExcelizeProtection], Field(exclude_none=True)] = None


class Cell(BaseModel):
    key: str
    style: Annotated[Optional[ExcelizeStyle], Field(exclude_none=True)] = None
    value: Any


class ComercioExterior_createComercioExteriorReportExcelRequest(BaseModel):
    Additional: Annotated[Optional[Any], Field(exclude_none=True)] = None
    Emisor_Rfc: Annotated[Optional[str], Field(exclude_none=True)] = None
    FechaEmision: Any
    Receptor_Rfc: Annotated[Optional[str], Field(exclude_none=True)] = None
    emails: list[str]
    excludedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    includedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None


class ComercioExterior_filterRequest(BaseModel):
    Additional: Annotated[Optional[Any], Field(exclude_none=True)] = None
    Emisor_Rfc: Annotated[Optional[str], Field(exclude_none=True)] = None
    FechaEmision: Any
    Receptor_Rfc: Annotated[Optional[str], Field(exclude_none=True)] = None
    hidden: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    show: Annotated[Optional[list[str]], Field(exclude_none=True)] = None


class CompensacionSaldosAFavorNomina(BaseModel):
    anio: str
    remanenteSalFav: float
    saldoAFavor: float


class ComprobanteCDP(BaseModel):
    Anio: str
    Meses: str
    NumRegIdTrib: str
    Periodicidad: str
    ResidenciaFiscal: str
    condicionesPago: str
    descuento: Annotated[Optional[float | None], Field(exclude_none=True)] = None
    descuentoMXN: Annotated[Optional[float | None], Field(exclude_none=True)] = None
    domicilioFiscal: str
    equivalencia: Annotated[Optional[float | None], Field(exclude_none=True)] = None
    estatus: str
    factAtrAdquirentEmisor: str
    fechaCancelacion: Annotated[Optional[Date | None], Field(exclude_none=True)] = None
    fechaEmision: Annotated[Optional[Date | None], Field(exclude_none=True)] = None
    fechaPago: Annotated[Optional[str], Field(exclude_none=True)] = None
    fechaTimbrado: Annotated[Optional[Date | None], Field(exclude_none=True)] = None
    folio: str
    formaPago: str
    metodoPago: str
    moneda: str
    monto: Annotated[Optional[float | None], Field(exclude_none=True)] = None
    montoTotalPagos: Annotated[Optional[float | None], Field(exclude_none=True)] = None
    montoTotalPagosMXN: Annotated[Optional[float | None], Field(exclude_none=True)] = (
        None
    )
    nombreEmisor: str
    nombreReceptor: str
    numParcialidad: Annotated[Optional[int | None], Field(exclude_none=True)] = None
    pagado: Annotated[Optional[float | None], Field(exclude_none=True)] = None
    pagadoMxn: Annotated[Optional[float | None], Field(exclude_none=True)] = None
    regimenEmisor: str
    regimenReceptor: str
    rfcEmisor: str
    rfcReceptor: str
    saldoAnterior: Annotated[Optional[float | None], Field(exclude_none=True)] = None
    saldoAnteriorMxn: Annotated[Optional[float | None], Field(exclude_none=True)] = None
    saldoInsoluto: Annotated[Optional[float | None], Field(exclude_none=True)] = None
    saldoInsolutoMxn: Annotated[Optional[float | None], Field(exclude_none=True)] = None
    serie: str
    serieFolio: str
    subtotal: float
    subtotalDescuento: float
    subtotalDescuentoMxn: float
    subtotalMXN: float
    tipo: str
    tipoCambio: float
    tipoComplemento: str
    tipoRelacion: str
    total: float
    totalMXN: float
    totalRetencionesIEPS: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalRetencionesIEPSMXN: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalRetencionesISR: Annotated[Optional[float | None], Field(exclude_none=True)] = (
        None
    )
    totalRetencionesISRMXN: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalRetencionesIVA: Annotated[Optional[float | None], Field(exclude_none=True)] = (
        None
    )
    totalRetencionesIVAMXN: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalTrasladosBaseIVA0: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalTrasladosBaseIVA0MXN: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalTrasladosBaseIVA16: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalTrasladosBaseIVA16MXN: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalTrasladosBaseIVA8: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalTrasladosBaseIVA8MXN: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalTrasladosBaseIVAExento: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalTrasladosBaseIVAExentoMXN: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalTrasladosImpuestoIVA0: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalTrasladosImpuestoIVA0MXN: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalTrasladosImpuestoIVA16: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalTrasladosImpuestoIVA16MXN: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalTrasladosImpuestoIVA8: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalTrasladosImpuestoIVA8MXN: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    usoCfdi: str
    uuid: str
    version: str
    versionPago: Annotated[Optional[str | None], Field(exclude_none=True)] = None
    vigencia: str = "Vigente"


class ImpuestoCdp(BaseModel):
    ObjetoImp: str
    Origen: str
    base: float
    baseMxn: Annotated[Optional[float | None], Field(exclude_none=True)] = None
    importe: Annotated[Optional[float | None], Field(exclude_none=True)] = None
    importeMxn: Annotated[Optional[float | None], Field(exclude_none=True)] = None
    impuesto: str
    tasaOCuota: Annotated[Optional[float | None], Field(exclude_none=True)] = None
    tipoFactor: str
    tipoImpuesto: str


class ComprobanteData(BaseModel):
    Anio: str
    Meses: str
    NumRegIdTrib: str
    Periodicidad: str
    ResidenciaFiscal: str
    condicionesPago: str
    descuento: Annotated[Optional[float | None], Field(exclude_none=True)] = None
    descuentoMXN: Annotated[Optional[float | None], Field(exclude_none=True)] = None
    domicilioFiscal: str
    estatus: str
    factAtrAdquirentEmisor: str
    fechaCancelacion: Annotated[Optional[Date | None], Field(exclude_none=True)] = None
    fechaEmision: Annotated[Optional[Date | None], Field(exclude_none=True)] = None
    fechaTimbrado: Annotated[Optional[Date | None], Field(exclude_none=True)] = None
    folio: str
    formaPago: str
    metodoPago: str
    moneda: str
    nombreEmisor: str
    nombreReceptor: str
    regimenEmisor: str
    regimenReceptor: str
    rfcEmisor: str
    rfcReceptor: str
    serie: str
    serieFolio: str
    subtotal: float
    subtotalDescuento: float
    subtotalDescuentoMxn: float
    subtotalMXN: float
    tipo: str
    tipoCambio: float
    tipoComplemento: str
    tipoRelacion: str
    total: float
    totalMXN: float
    usoCfdi: str
    uuid: str
    version: str
    vigencia: str = "Vigente"


class ComprobanteCdpPpd(BaseModel):
    CDP: ComprobanteData
    CtaBeneficiario: str | None = None
    CtaOrdenante: str | None = None
    Equuvalencia: float | None = None
    FechaPago: Date | None = None
    FormaPago: str | None = None
    MonedaPago: str | None = None
    MontoPago: float | None = None
    NomBancoOrdExt: str | None = None
    NumParcialidad: int | None = None
    PPD: ComprobanteData
    Pagado: float | None = None
    PagadoMxn: float | None = None
    RfcEmisorCtaBen: str | None = None
    RfcEmisorCtaOrd: str | None = None
    SaldoAnterior: float | None = None
    SaldoAnteriorMxn: float | None = None
    SaldoInsoluto: float | None = None
    SaldoInsolutoMxn: float | None = None
    TipoCambioPago: float | None = None
    VersionPago: str | None = None
    impuestos: list[ImpuestoCdp]
    montoTotalPagos: Annotated[Optional[float | None], Field(exclude_none=True)] = None
    montoTotalPagosMXN: Annotated[Optional[float | None], Field(exclude_none=True)] = (
        None
    )
    totalRetencionesIEPS: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalRetencionesIEPSMXN: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalRetencionesISR: Annotated[Optional[float | None], Field(exclude_none=True)] = (
        None
    )
    totalRetencionesISRMXN: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalRetencionesIVA: Annotated[Optional[float | None], Field(exclude_none=True)] = (
        None
    )
    totalRetencionesIVAMXN: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalTrasladosBaseIVA0: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalTrasladosBaseIVA0MXN: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalTrasladosBaseIVA16: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalTrasladosBaseIVA16MXN: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalTrasladosBaseIVA8: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalTrasladosBaseIVA8MXN: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalTrasladosBaseIVAExento: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalTrasladosBaseIVAExentoMXN: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalTrasladosImpuestoIVA0: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalTrasladosImpuestoIVA0MXN: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalTrasladosImpuestoIVA16: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalTrasladosImpuestoIVA16MXN: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalTrasladosImpuestoIVA8: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalTrasladosImpuestoIVA8MXN: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None


class SubsidioAlEmpleoNomina(BaseModel):
    subsidioCausado: float


class OtroPagoNomina(BaseModel):
    clave: str
    compensacionSaldosAFavor: Annotated[
        Optional[CompensacionSaldosAFavorNomina], Field(exclude_none=True)
    ] = None
    concepto: str
    importe: float
    subsidioAlEmpleo: Annotated[
        Optional[SubsidioAlEmpleoNomina], Field(exclude_none=True)
    ] = None
    tipoOtroPago: str


class HorasExtraNomina(BaseModel):
    dias: float
    horasExtra: float
    importePagado: float
    tipoHoras: str


class PercepcionNomina(BaseModel):
    accionesOTitulos: Annotated[
        Optional[AccionesOTitulosNomina], Field(exclude_none=True)
    ] = None
    clave: str
    concepto: str
    horasExtra: Annotated[
        Optional[list[HorasExtraNomina]], Field(exclude_none=True)
    ] = None
    importeExento: float
    importeGravado: float
    tipoPercepcion: str


class DeduccionNomina(BaseModel):
    clave: str
    concepto: str
    importe: float
    importeExento: float
    importeGravado: float
    tipoDeduccion: str


class IncapacidadNomina(BaseModel):
    diasIncapacidad: float
    importeMonetario: Annotated[Optional[float], Field(exclude_none=True)] = None
    tipoIncapacidad: str


class ConceptosNomina(BaseModel):
    deducciones: list[DeduccionNomina]
    incapacidades: list[IncapacidadNomina]
    otrosPagos: list[OtroPagoNomina]
    percepciones: list[PercepcionNomina]


class DetalleConceptosNomina(BaseModel):
    totalDeduccionExento: float | None = None
    totalDeduccionGravado: float | None = None
    totalImpuestosRetenidos: Annotated[Optional[float], Field(exclude_none=True)] = None
    totalJubilacionPensionRetiro: Annotated[
        Optional[float], Field(exclude_none=True)
    ] = None
    totalOtrasDeducciones: Annotated[Optional[float], Field(exclude_none=True)] = None
    totalPercepcionExento: float
    totalPercepcionGravado: float
    totalSeparacionIndemnizacion: Annotated[
        Optional[float], Field(exclude_none=True)
    ] = None
    totalSueldos: Annotated[Optional[float], Field(exclude_none=True)] = None


class ComprobanteNominaSabana(BaseModel):
    Anio: str
    Meses: str
    NumRegIdTrib: str
    Periodicidad: str
    ResidenciaFiscal: str
    antiguedad: str | None = None
    banco: str | None = None
    claveEntFed: str
    conceptos: ConceptosNomina
    condicionesPago: str
    cuentaBancaria: str | None = None
    curpEmisor: str | None = None
    curpReceptor: str
    departamento: str | None = None
    descuento: Annotated[Optional[float | None], Field(exclude_none=True)] = None
    descuentoMXN: Annotated[Optional[float | None], Field(exclude_none=True)] = None
    detalleConceptos: DetalleConceptosNomina
    domicilioFiscal: str
    estatus: str
    factAtrAdquirentEmisor: str
    fechaCancelacion: Annotated[Optional[Date | None], Field(exclude_none=True)] = None
    fechaEmision: Annotated[Optional[Date | None], Field(exclude_none=True)] = None
    fechaFinalPago: Date
    fechaIncioRelacionLaboral: Date | None = None
    fechaInicialPago: Date
    fechaPago: Date
    fechaTimbrado: Annotated[Optional[Date | None], Field(exclude_none=True)] = None
    folio: str
    formaPago: str
    horasExtra: list[HorasExtraNomina]
    metodoPago: str
    moneda: str
    nombreEmisor: str
    nombreReceptor: str
    numDiasPagados: float
    numEmpleado: str
    numSeguridadSocialReceptor: str | None = None
    periodicidadPago: str
    puesto: str | None = None
    regimenEmisor: str
    regimenReceptor: str
    registroPatronalEmisor: str | None = None
    rfcEmisor: str
    rfcPatronOrigenEmisor: str | None = None
    rfcReceptor: str
    riesgoPuesto: str | None = None
    salarioBaseCotApor: float | None = None
    salarioDiarioIntegrado: float | None = None
    serie: str
    serieFolio: str
    sindicalizado: str | None = None
    subtotal: float
    subtotalDescuento: float
    subtotalDescuentoMxn: float
    subtotalMXN: float
    tipo: str
    tipoCambio: float
    tipoComplemento: str
    tipoContrato: str
    tipoJornada: str | None = None
    tipoNomina: str
    tipoRegimen: str
    tipoRelacion: str
    total: float
    totalDeducciones: Annotated[Optional[float], Field(exclude_none=True)] = None
    totalMXN: float
    totalOtrosPagos: Annotated[Optional[float], Field(exclude_none=True)] = None
    totalPercepciones: Annotated[Optional[float], Field(exclude_none=True)] = None
    usoCfdi: str
    uuid: str
    version: str
    versionNomina: str
    vigencia: str = "Vigente"


class ComprobanteNominaTidy(BaseModel):
    claveFiscal: str
    claveInterna: str
    concepto: str
    emisorNombre: str
    emisorRegimenFiscal: str
    emisorRfc: str
    fechaEmision: str
    fechaFinalPago: str
    fechaInicialPago: str
    fechaPago: str
    moneda: str
    monto: float
    receptorNombre: str
    receptorRegimenFiscal: str
    receptorRfc: str
    subtotal: float
    subtotalMXN: float
    tipoConcepto: str
    tipoMonto: str
    tipoNomina: str
    total: float
    totalMXN: float
    uuid: str
    version: str
    versionNomina: str
    vigencia: str


class ComprobantePPD(BaseModel):
    CtaBeneficiario: str | None = None
    CtaOrdenante: str | None = None
    Equuvalencia: float | None = None
    FechaEmisionCDP: str | None = None
    FechaEmisionPPD: str
    FechaPago: str | None = None
    FolioCDP: str | None = None
    FolioPPD: str
    FormaPago: str | None = None
    Moneda: str | None = None
    Monto: float | None = None
    NomBancoOrdExt: str | None = None
    NombreEmisorCDP: str | None = None
    NombreEmisorPPD: str
    NombreReceptorCDP: str | None = None
    NombreReceptorPPD: str
    NumParcialidad: int | None = None
    Pagado: float | None = None
    PagadoMxn: float | None = None
    RegimenFiscalEmisorCDP: str | None = None
    RegimenFiscalEmisorPPD: str
    RegimenFiscalReceptorCDP: str | None = None
    RegimenFiscalReceptorPPD: str
    RfcEmisorCDP: str | None = None
    RfcEmisorCtaBen: str | None = None
    RfcEmisorCtaOrd: str | None = None
    RfcEmisorPPD: str
    RfcReceptorCDP: str | None = None
    RfcReceptorPPD: str
    SaldoAnterior: float | None = None
    SaldoAnteriorMxn: float | None = None
    SaldoInsoluto: float | None = None
    SaldoInsolutoMxn: float | None = None
    SerieCDP: str | None = None
    SeriePPD: str
    StatusPPD: str
    SubtotalCDP: float | None = None
    SubtotalMxnCDP: float | None = None
    SubtotalMxnPPD: float
    SubtotalPPD: float
    TipoCDP: str | None = None
    TipoCambio: float | None = None
    TipoPPD: str
    TotalCDP: float | None = None
    TotalMxnCDP: float | None = None
    TotalMxnPPD: float
    TotalPPD: float
    UuidCDP: str | None = None
    UuidPPD: str
    VersionCDP: str | None = None
    VersionPPD: str
    VersionPago: str | None = None
    VigenciaCDP: str = "Vigente"
    VigenciaPPD: str = "Vigente"
    montoTotalPagos: Annotated[Optional[float | None], Field(exclude_none=True)] = None
    montoTotalPagosMXN: Annotated[Optional[float | None], Field(exclude_none=True)] = (
        None
    )
    totalRetencionesIEPS: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalRetencionesIEPSMXN: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalRetencionesISR: Annotated[Optional[float | None], Field(exclude_none=True)] = (
        None
    )
    totalRetencionesISRMXN: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalRetencionesIVA: Annotated[Optional[float | None], Field(exclude_none=True)] = (
        None
    )
    totalRetencionesIVAMXN: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalTrasladosBaseIVA0: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalTrasladosBaseIVA0MXN: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalTrasladosBaseIVA16: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalTrasladosBaseIVA16MXN: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalTrasladosBaseIVA8: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalTrasladosBaseIVA8MXN: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalTrasladosBaseIVAExento: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalTrasladosBaseIVAExentoMXN: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalTrasladosImpuestoIVA0: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalTrasladosImpuestoIVA0MXN: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalTrasladosImpuestoIVA16: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalTrasladosImpuestoIVA16MXN: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalTrasladosImpuestoIVA8: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalTrasladosImpuestoIVA8MXN: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None


class ComprobantePagosV2(BaseModel):
    Anio: str
    Meses: str
    NumRegIdTrib: str
    Periodicidad: str
    ResidenciaFiscal: str
    cargadoEnKuantik: str
    condicionesPago: str
    descuento: Annotated[Optional[float | None], Field(exclude_none=True)] = None
    descuentoMXN: Annotated[Optional[float | None], Field(exclude_none=True)] = None
    domicilioFiscal: str
    equivalencia: Annotated[Optional[float | None], Field(exclude_none=True)] = None
    estatus: str
    factAtrAdquirentEmisor: str
    fechaCancelacion: Annotated[Optional[Date | None], Field(exclude_none=True)] = None
    fechaEmision: Annotated[Optional[Date | None], Field(exclude_none=True)] = None
    fechaPago: Annotated[Optional[str], Field(exclude_none=True)] = None
    fechaTimbrado: Annotated[Optional[Date | None], Field(exclude_none=True)] = None
    folio: str
    formaPago: str
    metodoPago: str
    moneda: str
    monto: Annotated[Optional[float | None], Field(exclude_none=True)] = None
    montoTotalPagos: Annotated[Optional[float | None], Field(exclude_none=True)] = None
    montoTotalPagosMXN: Annotated[Optional[float | None], Field(exclude_none=True)] = (
        None
    )
    nombreEmisor: str
    nombreReceptor: str
    numParcialidad: Annotated[Optional[int | None], Field(exclude_none=True)] = None
    pagado: Annotated[Optional[float | None], Field(exclude_none=True)] = None
    pagadoMxn: Annotated[Optional[float | None], Field(exclude_none=True)] = None
    regimenEmisor: str
    regimenReceptor: str
    rfcEmisor: str
    rfcReceptor: str
    saldoAnterior: Annotated[Optional[float | None], Field(exclude_none=True)] = None
    saldoAnteriorMxn: Annotated[Optional[float | None], Field(exclude_none=True)] = None
    saldoInsoluto: Annotated[Optional[float | None], Field(exclude_none=True)] = None
    saldoInsolutoMxn: Annotated[Optional[float | None], Field(exclude_none=True)] = None
    serie: str
    serieFolio: str
    subtotal: float
    subtotalDescuento: float
    subtotalDescuentoMxn: float
    subtotalMXN: float
    tipo: str
    tipoCambio: float
    tipoComplemento: str
    tipoRelacion: str
    total: float
    totalMXN: float
    totalRetencionesIEPS: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalRetencionesIEPSMXN: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalRetencionesISR: Annotated[Optional[float | None], Field(exclude_none=True)] = (
        None
    )
    totalRetencionesISRMXN: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalRetencionesIVA: Annotated[Optional[float | None], Field(exclude_none=True)] = (
        None
    )
    totalRetencionesIVAMXN: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalTrasladosBaseIVA0: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalTrasladosBaseIVA0MXN: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalTrasladosBaseIVA16: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalTrasladosBaseIVA16MXN: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalTrasladosBaseIVA8: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalTrasladosBaseIVA8MXN: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalTrasladosBaseIVAExento: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalTrasladosBaseIVAExentoMXN: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalTrasladosImpuestoIVA0: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalTrasladosImpuestoIVA0MXN: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalTrasladosImpuestoIVA16: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalTrasladosImpuestoIVA16MXN: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalTrasladosImpuestoIVA8: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalTrasladosImpuestoIVA8MXN: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    usoCfdi: str
    uuid: str
    uuidOrigen: str
    uuidPago: str
    version: str
    versionPago: Annotated[Optional[str | None], Field(exclude_none=True)] = None
    vigencia: str = "Vigente"


class ComprobantePueCdpResumen(BaseModel):
    Anio: str
    Meses: str
    NumRegIdTrib: str
    Periodicidad: str
    ResidenciaFiscal: str
    TotalImpuestoRetenido: float | None = None
    TotalImpuestoRetenidoMXN: float | None = None
    TotalImpuestoTraslado: float | None = None
    TotalImpuestoTrasladoBaseNoObjeto: float | None = None
    TotalImpuestoTrasladoBaseNoObjetoMXN: float | None = None
    TotalImpuestoTrasladoMXN: float | None = None
    TotalRetencionBaseIEPS: float | None = None
    TotalRetencionBaseISR: float | None = None
    TotalRetencionBaseIVA: float | None = None
    TotalRetencionBaseIVAMXN: float | None = None
    TotalRetencionImporteIEPS: float | None = None
    TotalRetencionImporteISR: float | None = None
    TotalRetencionImporteIVA: float | None = None
    TotalRetencionImporteIVAMXN: float | None = None
    TotalTrasladoBaseIEPS: float | None = None
    TotalTrasladoBaseIVAExcento: float | None = None
    TotalTrasladoBaseIVAExcentoMXN: float | None = None
    TotalTrasladoBaseIVATasa0: float | None = None
    TotalTrasladoBaseIVATasa0MXN: float | None = None
    TotalTrasladoBaseIVATasa16: float | None = None
    TotalTrasladoBaseIVATasa16MXN: float | None = None
    TotalTrasladoBaseIVATasa8: float | None = None
    TotalTrasladoBaseIVATasa8MXN: float | None = None
    TotalTrasladoImporteIEPS: float | None = None
    TotalTrasladoImporteIVAExcento: float | None = None
    TotalTrasladoImporteIVAExcentoMXN: float | None = None
    TotalTrasladoImporteIVATasa0: float | None = None
    TotalTrasladoImporteIVATasa0MXN: float | None = None
    TotalTrasladoImporteIVATasa16: float | None = None
    TotalTrasladoImporteIVATasa16MXN: float | None = None
    TotalTrasladoImporteIVATasa8: float | None = None
    TotalTrasladoImporteIVATasa8MXN: float | None = None
    condicionesPago: str
    descuento: Annotated[Optional[float | None], Field(exclude_none=True)] = None
    descuentoMXN: Annotated[Optional[float | None], Field(exclude_none=True)] = None
    domicilioFiscal: str
    efectoComprobante: str
    estatus: str
    factAtrAdquirentEmisor: str
    fechaCancelacion: Annotated[Optional[Date | None], Field(exclude_none=True)] = None
    fechaEmision: Annotated[Optional[Date | None], Field(exclude_none=True)] = None
    fechaPago: Annotated[Optional[Date | None], Field(exclude_none=True)] = None
    fechaTimbrado: Annotated[Optional[Date | None], Field(exclude_none=True)] = None
    folio: str
    formaPago: str
    metodoPago: str
    moneda: str
    nombreEmisor: str
    nombreReceptor: str
    operationId: str
    regimenEmisor: str
    regimenReceptor: str
    rfcEmisor: str
    rfcReceptor: str
    serie: str
    serieFolio: str
    subtotal: float
    subtotalDescuento: float
    subtotalDescuentoMxn: float
    subtotalMXN: float
    tipo: str
    tipoCambio: float
    tipoComplemento: str
    tipoRelacion: str
    total: float
    totalMXN: float
    usoCfdi: str
    uuid: str
    version: str
    vigencia: str = "Vigente"


class Impuesto(BaseModel):
    ObjetoImp: str
    base: float
    baseMxn: Annotated[Optional[float | None], Field(exclude_none=True)] = None
    importe: Annotated[Optional[float | None], Field(exclude_none=True)] = None
    importeMxn: Annotated[Optional[float | None], Field(exclude_none=True)] = None
    impuesto: str
    tasaOCuota: Annotated[Optional[float | None], Field(exclude_none=True)] = None
    tipoFactor: str
    tipoImpuesto: str


class ComprobantePueCdpSabana(BaseModel):
    Anio: str
    Meses: str
    NumRegIdTrib: str
    Periodicidad: str
    ResidenciaFiscal: str
    TipoCambioP: float | None = None
    TotalCdp: float | None = None
    TotalFacturaOrigen: float | None = None
    condicionesPago: str
    descuento: Annotated[Optional[float | None], Field(exclude_none=True)] = None
    descuentoMXN: Annotated[Optional[float | None], Field(exclude_none=True)] = None
    domicilioFiscal: str
    efectoComprobante: str
    equivalenciaDR: float
    estatus: str
    factAtrAdquirentEmisor: str
    fechaCancelacion: Annotated[Optional[Date | None], Field(exclude_none=True)] = None
    fechaEmision: Annotated[Optional[Date | None], Field(exclude_none=True)] = None
    fechaPago: Annotated[Optional[Date | None], Field(exclude_none=True)] = None
    fechaTimbrado: Annotated[Optional[Date | None], Field(exclude_none=True)] = None
    folio: str
    formaPago: str
    formaPagoP: str
    importePagadoDR: float
    impuestos: list[Impuesto]
    metodoPago: str
    moneda: str
    monedaDR: str
    monedaP: str
    nivel: int
    nombreEmisor: str
    nombreReceptor: str
    objetoImpDR: str
    regimenEmisor: str
    regimenReceptor: str
    rfcEmisor: str
    rfcReceptor: str
    serie: str
    serieFolio: str
    subtotal: float
    subtotalDescuento: float
    subtotalDescuentoMxn: float
    subtotalMXN: float
    tipo: str
    tipoCambio: float
    tipoComplemento: str
    tipoRelacion: str
    total: float
    totalMXN: float
    usoCfdi: str
    uuid: str
    uuidDR: str
    version: str
    vigencia: str = "Vigente"


class ComprobantePueCdpTidy(BaseModel):
    Anio: str
    Meses: str
    NumRegIdTrib: str
    Periodicidad: str
    ResidenciaFiscal: str
    TasaOCuota: Annotated[Optional[float | None], Field(exclude_none=True)] = None
    TipoCambioP: float | None = None
    TotalImpuestoTrasladoBaseNoObjeto: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    TotalImpuestoTrasladoBaseNoObjetoMXN: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    base: Annotated[Optional[float | None], Field(exclude_none=True)] = None
    conceptoImpuesto: str
    condicionesPago: str
    descuento: Annotated[Optional[float | None], Field(exclude_none=True)] = None
    descuentoMXN: Annotated[Optional[float | None], Field(exclude_none=True)] = None
    domicilioFiscal: str
    efectoComprobante: str
    equivalenciaDR: float
    estatus: str
    factAtrAdquirentEmisor: str
    fechaCancelacion: Annotated[Optional[Date | None], Field(exclude_none=True)] = None
    fechaEmision: Annotated[Optional[Date | None], Field(exclude_none=True)] = None
    fechaPago: Annotated[Optional[Date | None], Field(exclude_none=True)] = None
    fechaTimbrado: Annotated[Optional[Date | None], Field(exclude_none=True)] = None
    folio: str
    formaPago: str
    formaPagoP: str
    importe: Annotated[Optional[float | None], Field(exclude_none=True)] = None
    importePagadoDR: float
    impuestos: list[Impuesto]
    metodoPago: str
    moneda: str
    monedaDR: str
    monedaP: str
    nivel: int
    nivelOrigen: str
    nombreEmisor: str
    nombreReceptor: str
    objetoImpDR: str
    objetoImpuesto: str
    regimenEmisor: str
    regimenReceptor: str
    rfcEmisor: str
    rfcReceptor: str
    serie: str
    serieFolio: str
    subtotal: float
    subtotalDescuento: float
    subtotalDescuentoMxn: float
    subtotalMXN: float
    tasaCuota: str
    tipo: str
    tipoCambio: float
    tipoComplemento: str
    tipoFactor: str
    tipoImpuesto: str
    tipoRelacion: str
    total: float
    totalMXN: float
    usoCfdi: str
    uuid: str
    uuidDR: str
    version: str
    vigencia: str = "Vigente"


class ComprobantePuePpdGeneralCdpSabana(BaseModel):
    Comprobante: ComprobanteData
    cfdiCdp: str
    cfdiRelacionados: str
    conceptos: str
    estadoPago: str
    impuestos: list[Impuesto]
    listaNegraEmisor: str
    listaNegraReceptor: str
    nivel: int
    operationId: str
    totalCalculado: float
    totalCalculadoMxn: float
    totalCdps: float
    totalCdpsMxn: float
    totalImpuestosRetenidos: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalImpuestosRetenidosMxn: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalImpuestosTrasladados: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalImpuestosTrasladadosMxn: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None


class ComprobantePuePpdGeneralSabana(BaseModel):
    Comprobante: ComprobanteData
    cfdiCdp: str
    cfdiRelacionados: str
    conceptos: str
    estadoPago: str
    impuestos: list[Impuesto]
    listaNegraEmisor: str
    listaNegraReceptor: str
    operationId: str
    totalCalculado: float
    totalCalculadoMxn: float
    totalCdps: float
    totalCdpsMxn: float
    totalImpuestosRetenidos: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalImpuestosRetenidosMxn: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalImpuestosTrasladados: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalImpuestosTrasladadosMxn: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None


class ComprobantePuePpdGeneralSabanaMomentos(BaseModel):
    Comprobante: ComprobanteData
    cfdiCdp: str
    cfdiRelacionados: str
    estadoPago: str
    impuestos: list[Impuesto]
    operationId: str
    relacionadoSustitucion: Annotated[
        Optional[ComprobanteData], Field(exclude_none=True)
    ] = None
    relacionadoSustituida: Annotated[
        Optional[ComprobanteData], Field(exclude_none=True)
    ] = None
    totalCalculado: float
    totalCalculadoMxn: float
    totalCdps: float
    totalCdpsMxn: float
    totalImpuestosRetenidos: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalImpuestosRetenidosMxn: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalImpuestosTrasladados: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalImpuestosTrasladadosMxn: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None


class ComprobantePuePpdGeneralTidy(BaseModel):
    Comprobante: ComprobanteData
    EquivalenciaDR: Annotated[Optional[float], Field(exclude_none=True)] = None
    ImportePagadoDR: Annotated[Optional[float], Field(exclude_none=True)] = None
    MonedaDR: Annotated[Optional[str], Field(exclude_none=True)] = None
    TasaOCuota: Annotated[Optional[float | None], Field(exclude_none=True)] = None
    UuidDR: Annotated[Optional[str], Field(exclude_none=True)] = None
    base: Annotated[Optional[float | None], Field(exclude_none=True)] = None
    cfdiCdp: str
    cfdiRelacionados: str
    conceptoImpuesto: str
    estadoPago: str
    importe: Annotated[Optional[float | None], Field(exclude_none=True)] = None
    impuestos: list[Impuesto]
    objetoImpuesto: str
    tasaCuota: str
    tipoFactor: str
    tipoImpuesto: str
    totalCalculado: float
    totalCalculadoMxn: float
    totalCdps: float
    totalCdpsMxn: float
    totalImpuestosRetenidos: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalImpuestosRetenidosMxn: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalImpuestosTrasladados: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalImpuestosTrasladadosMxn: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None


class ComprobanteReferenciaRelacionado(BaseModel):
    fechaCancelacionRelReferencia: Annotated[
        Optional[Date | None], Field(exclude_none=True)
    ] = None
    fechaEmisionRelReferencia: Annotated[
        Optional[Date | None], Field(exclude_none=True)
    ] = None
    subtotalMXNRelReferencia: float
    uuidRelReferencia: Annotated[Optional[str], Field(exclude_none=True)] = None
    vigenciaRelReferencia: str = "Vigente"


class ComprobanteRelacionado(BaseModel):
    comprobante: ComprobanteData
    tipoRelacion: str


class TotalesRelacionado(BaseModel):
    sumaDeTotal: float
    sumaDeTotalMxn: float


class ComprobanteRelacionadosResumen(BaseModel):
    Comprobante: ComprobanteData
    anticipo07: Annotated[Optional[TotalesRelacionado], Field(exclude_none=True)] = None
    cfdiCdp: str
    cfdiRelacionados: str
    devolucion03: Annotated[Optional[TotalesRelacionado], Field(exclude_none=True)] = (
        None
    )
    estadoPago: str
    notaCredito01: Annotated[Optional[TotalesRelacionado], Field(exclude_none=True)] = (
        None
    )
    notaDebito02: Annotated[Optional[TotalesRelacionado], Field(exclude_none=True)] = (
        None
    )
    sustitucion04: Annotated[Optional[TotalesRelacionado], Field(exclude_none=True)] = (
        None
    )
    totalCalculado: float
    totalCalculadoMxn: float
    totalCdps: float
    totalCdpsMxn: float
    traslados05: Annotated[Optional[TotalesRelacionado], Field(exclude_none=True)] = (
        None
    )
    trasladosPrevios06: Annotated[
        Optional[TotalesRelacionado], Field(exclude_none=True)
    ] = None


class ComprobanteRelacionadosSabana(BaseModel):
    Comprobante: ComprobanteData
    anticipo07: Annotated[Optional[ComprobanteData], Field(exclude_none=True)] = None
    cdp: Annotated[Optional[ComprobanteData], Field(exclude_none=True)] = None
    devolucion03: Annotated[Optional[ComprobanteData], Field(exclude_none=True)] = None
    equivalencia: Annotated[Optional[float | None], Field(exclude_none=True)] = None
    fechaPago: Annotated[Optional[str], Field(exclude_none=True)] = None
    formaPago: Annotated[Optional[str | None], Field(exclude_none=True)] = None
    moneda: Annotated[Optional[str | None], Field(exclude_none=True)] = None
    monto: Annotated[Optional[float | None], Field(exclude_none=True)] = None
    montoTotalPagos: Annotated[Optional[float | None], Field(exclude_none=True)] = None
    montoTotalPagosMXN: Annotated[Optional[float | None], Field(exclude_none=True)] = (
        None
    )
    notaCredito01: Annotated[Optional[ComprobanteData], Field(exclude_none=True)] = None
    notaDebito02: Annotated[Optional[ComprobanteData], Field(exclude_none=True)] = None
    numParcialidad: Annotated[Optional[int | None], Field(exclude_none=True)] = None
    pagado: Annotated[Optional[float | None], Field(exclude_none=True)] = None
    pagadoMxn: Annotated[Optional[float | None], Field(exclude_none=True)] = None
    saldoAnterior: Annotated[Optional[float | None], Field(exclude_none=True)] = None
    saldoAnteriorMxn: Annotated[Optional[float | None], Field(exclude_none=True)] = None
    saldoInsoluto: Annotated[Optional[float | None], Field(exclude_none=True)] = None
    saldoInsolutoMxn: Annotated[Optional[float | None], Field(exclude_none=True)] = None
    sustitucion04: Annotated[Optional[ComprobanteData], Field(exclude_none=True)] = None
    tipoCambio: Annotated[Optional[float | None], Field(exclude_none=True)] = None
    totalRetencionesIEPS: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalRetencionesIEPSMXN: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalRetencionesISR: Annotated[Optional[float | None], Field(exclude_none=True)] = (
        None
    )
    totalRetencionesISRMXN: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalRetencionesIVA: Annotated[Optional[float | None], Field(exclude_none=True)] = (
        None
    )
    totalRetencionesIVAMXN: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalTrasladosBaseIVA0: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalTrasladosBaseIVA0MXN: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalTrasladosBaseIVA16: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalTrasladosBaseIVA16MXN: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalTrasladosBaseIVA8: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalTrasladosBaseIVA8MXN: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalTrasladosBaseIVAExento: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalTrasladosBaseIVAExentoMXN: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalTrasladosImpuestoIVA0: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalTrasladosImpuestoIVA0MXN: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalTrasladosImpuestoIVA16: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalTrasladosImpuestoIVA16MXN: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalTrasladosImpuestoIVA8: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    totalTrasladosImpuestoIVA8MXN: Annotated[
        Optional[float | None], Field(exclude_none=True)
    ] = None
    traslados05: Annotated[Optional[ComprobanteData], Field(exclude_none=True)] = None
    trasladosPrevios06: Annotated[
        Optional[ComprobanteData], Field(exclude_none=True)
    ] = None
    versionPago: Annotated[Optional[str | None], Field(exclude_none=True)] = None


class ComprobanteRelacionadosTidy(BaseModel):
    Anio: str
    Meses: str
    NumRegIdTrib: str
    Periodicidad: str
    ResidenciaFiscal: str
    cdp: Annotated[Optional[ComprobanteCDP], Field(exclude_none=True)] = None
    condicionesPago: str
    descuento: Annotated[Optional[float | None], Field(exclude_none=True)] = None
    descuentoMXN: Annotated[Optional[float | None], Field(exclude_none=True)] = None
    domicilioFiscal: str
    estatus: str
    factAtrAdquirentEmisor: str
    fechaCancelacion: Annotated[Optional[Date | None], Field(exclude_none=True)] = None
    fechaEmision: Annotated[Optional[Date | None], Field(exclude_none=True)] = None
    fechaTimbrado: Annotated[Optional[Date | None], Field(exclude_none=True)] = None
    folio: str
    formaPago: str
    metodoPago: str
    moneda: str
    nombreEmisor: str
    nombreReceptor: str
    operationId: str
    regimenEmisor: str
    regimenReceptor: str
    relacionado: Annotated[
        Optional[ComprobanteRelacionado], Field(exclude_none=True)
    ] = None
    relacionadoReferencia: Annotated[
        Optional[ComprobanteReferenciaRelacionado], Field(exclude_none=True)
    ] = None
    rfcEmisor: str
    rfcReceptor: str
    serie: str
    serieFolio: str
    subtotal: float
    subtotalDescuento: float
    subtotalDescuentoMxn: float
    subtotalMXN: float
    tipo: str
    tipoCambio: float
    tipoComplemento: str
    tipoRelacion: str
    total: float
    totalMXN: float
    usoCfdi: str
    uuid: str
    version: str
    vigencia: str = "Vigente"


class ConceptoNominaRow(BaseModel):
    claveFiscal: str
    claveInterna: str
    concepto: str
    fechaFin: str
    fechaInicio: str
    monto: float
    tipoConcepto: str
    tipoMonto: str


class RecordHeaders(BaseModel):
    dataType: str
    defaultRecord: Annotated[Optional[str], Field(exclude_none=True)] = None
    key: str
    order: int
    title: str


class Custom_createCustomExcelReportRequest(BaseModel):
    checkColumns: Annotated[Optional[bool], Field(exclude_none=True)] = None
    data: list[Any]
    direction: Annotated[Optional[int], Field(exclude_none=True)] = None
    emails: list[str]
    headers: Annotated[Optional[list[RecordHeaders]], Field(exclude_none=True)] = None
    sortData: Annotated[Optional[str], Field(exclude_none=True)] = None
    title: Annotated[Optional[str], Field(exclude_none=True)] = None


class Custom_createCustomJsonRequest(BaseModel):
    checkColumns: Annotated[Optional[bool], Field(exclude_none=True)] = None
    data: list[Any]
    direction: Annotated[Optional[int], Field(exclude_none=True)] = None
    emails: list[str]
    headers: Annotated[Optional[list[RecordHeaders]], Field(exclude_none=True)] = None
    sortData: Annotated[Optional[str], Field(exclude_none=True)] = None
    title: Annotated[Optional[str], Field(exclude_none=True)] = None


class Rows(BaseModel):
    row: list[Cell]
    styleRow: Annotated[Optional[ExcelizeStyle], Field(exclude_none=True)] = None


class Custom_createCustomStyleExcelReportRequest(BaseModel):
    checkColumns: Annotated[Optional[bool], Field(exclude_none=True)] = None
    data: list[Rows]
    direction: Annotated[Optional[int], Field(exclude_none=True)] = None
    emails: list[str]
    headers: Annotated[Optional[list[RecordHeaders]], Field(exclude_none=True)] = None
    sortData: Annotated[Optional[str], Field(exclude_none=True)] = None
    styleMain: Annotated[Optional[ExcelizeStyle], Field(exclude_none=True)] = None
    title: Annotated[Optional[str], Field(exclude_none=True)] = None


class Custom_createSyncCustomExcelReportRequest(BaseModel):
    checkColumns: Annotated[Optional[bool], Field(exclude_none=True)] = None
    data: list[Any]
    direction: Annotated[Optional[int], Field(exclude_none=True)] = None
    emails: list[str]
    headers: Annotated[Optional[list[RecordHeaders]], Field(exclude_none=True)] = None
    sortData: Annotated[Optional[str], Field(exclude_none=True)] = None
    title: Annotated[Optional[str], Field(exclude_none=True)] = None


class Custom_createSyncCustomStyleExcelReportRequest(BaseModel):
    checkColumns: Annotated[Optional[bool], Field(exclude_none=True)] = None
    data: list[Rows]
    direction: Annotated[Optional[int], Field(exclude_none=True)] = None
    emails: list[str]
    headers: Annotated[Optional[list[RecordHeaders]], Field(exclude_none=True)] = None
    sortData: Annotated[Optional[str], Field(exclude_none=True)] = None
    styleMain: Annotated[Optional[ExcelizeStyle], Field(exclude_none=True)] = None
    title: Annotated[Optional[str], Field(exclude_none=True)] = None


class Directory_createDirectoryRequest(BaseModel):
    Additional: Annotated[Optional[Any], Field(exclude_none=True)] = None
    Comprobante: bool
    Emisor_Rfc: Annotated[Optional[str], Field(exclude_none=True)] = None
    FechaEmision: Any
    Receptor_Rfc: Annotated[Optional[str], Field(exclude_none=True)] = None
    Transaccion: str
    Vigente: bool
    emails: list[str]
    excludedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    includedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None


class Directory_lastDirectoryRequest(BaseModel):
    Additional: Annotated[Optional[Any], Field(exclude_none=True)] = None
    Comprobante: bool
    Emisor_Rfc: Annotated[Optional[str], Field(exclude_none=True)] = None
    FechaEmision: Any
    Receptor_Rfc: Annotated[Optional[str], Field(exclude_none=True)] = None
    Transaccion: str
    Vigente: bool
    emails: list[str]
    excludedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    includedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None


class ErrorDetail(BaseModel):
    location: Annotated[Optional[str], Field(exclude_none=True)] = None
    message: Annotated[Optional[str], Field(exclude_none=True)] = None
    value: Annotated[Optional[Any], Field(exclude_none=True)] = None


class ErrorModel(BaseModel):
    detail: Annotated[Optional[str], Field(exclude_none=True)] = None
    errors: Annotated[Optional[list[ErrorDetail]], Field(exclude_none=True)] = None
    instance: Annotated[Optional[str], Field(exclude_none=True)] = None
    status: Annotated[Optional[int], Field(exclude_none=True)] = None
    title: Annotated[Optional[str], Field(exclude_none=True)] = None
    type: Annotated[Optional[str], Field(exclude_none=True)] = None


class General_createGeneralReportExcelRequest(BaseModel):
    Additional: Annotated[Optional[Any], Field(exclude_none=True)] = None
    Emisor_Rfc: Annotated[Optional[str], Field(exclude_none=True)] = None
    FechaEmision: Any
    Receptor_Rfc: Annotated[Optional[str], Field(exclude_none=True)] = None
    emails: list[str]
    excludedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    includedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None


class General_filterRequest(BaseModel):
    Additional: Annotated[Optional[Any], Field(exclude_none=True)] = None
    Emisor_Rfc: Annotated[Optional[str], Field(exclude_none=True)] = None
    FechaEmision: Any
    Receptor_Rfc: Annotated[Optional[str], Field(exclude_none=True)] = None
    hidden: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    show: Annotated[Optional[list[str]], Field(exclude_none=True)] = None


class HealthCheckSchema(BaseModel):
    status: str
    version: str


class Metadata(BaseModel):
    limit: int
    skip: int
    sortDirection: str
    sortKey: str
    total: int


class KoreResponse(BaseModel):
    data: list[Any]
    message: Annotated[Optional[str], Field(exclude_none=True)] = None
    metadata: Metadata


class NominaDetalleGeneral(BaseModel):
    endDate: str
    monto: float
    startDate: str
    tipoConcepto: str
    tipoMonto: str


class Nomina_createReportNominaConceptosExcelRequest(BaseModel):
    advancedFilter: Annotated[Optional[Any], Field(exclude_none=True)] = None
    emails: list[str]
    endDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    excludedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    filterDateBy: str = "emision"
    folios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    includedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    limit: Annotated[Optional[int], Field(exclude_none=True)] = None
    notFolios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSerieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSeries: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notUuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    rfcEmisor: Annotated[Optional[str], Field(exclude_none=True)] = None
    rfcReceptor: Annotated[Optional[str], Field(exclude_none=True)] = None
    serieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    series: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    skip: Annotated[Optional[int], Field(exclude_none=True)] = None
    sortDirection: Annotated[Optional[str], Field(exclude_none=True)] = None
    sortKey: Annotated[Optional[str], Field(exclude_none=True)] = None
    startDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    uuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None


class Nomina_createReportNominaDetallesGeneralesExcelRequest(BaseModel):
    advancedFilter: Annotated[Optional[Any], Field(exclude_none=True)] = None
    emails: list[str]
    endDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    excludedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    filterDateBy: str = "emision"
    folios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    includedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    limit: Annotated[Optional[int], Field(exclude_none=True)] = None
    notFolios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSerieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSeries: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notUuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    rfcEmisor: Annotated[Optional[str], Field(exclude_none=True)] = None
    rfcReceptor: Annotated[Optional[str], Field(exclude_none=True)] = None
    serieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    series: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    skip: Annotated[Optional[int], Field(exclude_none=True)] = None
    sortDirection: Annotated[Optional[str], Field(exclude_none=True)] = None
    sortKey: Annotated[Optional[str], Field(exclude_none=True)] = None
    startDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    uuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None


class Nomina_createReportNominaSabanaExcelRequest(BaseModel):
    advancedFilter: Annotated[Optional[Any], Field(exclude_none=True)] = None
    emails: list[str]
    endDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    excludedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    filterDateBy: str = "emision"
    folios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    includedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    limit: Annotated[Optional[int], Field(exclude_none=True)] = None
    notFolios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSerieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSeries: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notUuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    rfcEmisor: Annotated[Optional[str], Field(exclude_none=True)] = None
    rfcReceptor: Annotated[Optional[str], Field(exclude_none=True)] = None
    serieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    series: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    skip: Annotated[Optional[int], Field(exclude_none=True)] = None
    sortDirection: Annotated[Optional[str], Field(exclude_none=True)] = None
    sortKey: Annotated[Optional[str], Field(exclude_none=True)] = None
    startDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    tipoNomina: Annotated[Optional[str], Field(exclude_none=True)] = None
    uuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None


class Nomina_createReportNominaSabanaRfcExcelRequest(BaseModel):
    advancedFilter: Annotated[Optional[Any], Field(exclude_none=True)] = None
    emails: list[str]
    endDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    excludedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    filterDateBy: str = "emision"
    folios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    includedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    limit: Annotated[Optional[int], Field(exclude_none=True)] = None
    notFolios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSerieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSeries: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notUuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    rfcEmisor: Annotated[Optional[str], Field(exclude_none=True)] = None
    rfcReceptor: Annotated[Optional[str], Field(exclude_none=True)] = None
    serieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    series: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    skip: Annotated[Optional[int], Field(exclude_none=True)] = None
    sortDirection: Annotated[Optional[str], Field(exclude_none=True)] = None
    sortKey: Annotated[Optional[str], Field(exclude_none=True)] = None
    startDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    tipoNomina: Annotated[Optional[str], Field(exclude_none=True)] = None
    uuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None


class Nomina_createReportNominaTidyExcelRequest(BaseModel):
    advancedFilter: Annotated[Optional[Any], Field(exclude_none=True)] = None
    emails: list[str]
    endDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    excludedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    filterDateBy: str = "emision"
    folios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    includedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    limit: Annotated[Optional[int], Field(exclude_none=True)] = None
    notFolios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSerieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSeries: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notUuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    rfcEmisor: Annotated[Optional[str], Field(exclude_none=True)] = None
    rfcReceptor: Annotated[Optional[str], Field(exclude_none=True)] = None
    serieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    series: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    skip: Annotated[Optional[int], Field(exclude_none=True)] = None
    sortDirection: Annotated[Optional[str], Field(exclude_none=True)] = None
    sortKey: Annotated[Optional[str], Field(exclude_none=True)] = None
    startDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    uuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None


class Nomina_getReportNominaConceptosJSONRequest(BaseModel):
    advancedFilter: Annotated[Optional[Any], Field(exclude_none=True)] = None
    endDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    filterDateBy: str = "emision"
    folios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    limit: Annotated[Optional[int], Field(exclude_none=True)] = None
    notFolios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSerieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSeries: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notUuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    rfcEmisor: Annotated[Optional[str], Field(exclude_none=True)] = None
    rfcReceptor: Annotated[Optional[str], Field(exclude_none=True)] = None
    serieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    series: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    skip: Annotated[Optional[int], Field(exclude_none=True)] = None
    sortDirection: Annotated[Optional[str], Field(exclude_none=True)] = None
    sortKey: Annotated[Optional[str], Field(exclude_none=True)] = None
    startDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    uuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None


class Nomina_getReportNominaDetallesGeneralesJSONRequest(BaseModel):
    advancedFilter: Annotated[Optional[Any], Field(exclude_none=True)] = None
    endDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    filterDateBy: str = "emision"
    folios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    limit: Annotated[Optional[int], Field(exclude_none=True)] = None
    notFolios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSerieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSeries: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notUuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    rfcEmisor: Annotated[Optional[str], Field(exclude_none=True)] = None
    rfcReceptor: Annotated[Optional[str], Field(exclude_none=True)] = None
    serieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    series: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    skip: Annotated[Optional[int], Field(exclude_none=True)] = None
    sortDirection: Annotated[Optional[str], Field(exclude_none=True)] = None
    sortKey: Annotated[Optional[str], Field(exclude_none=True)] = None
    startDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    uuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None


class Nomina_getReportNominaJSONRequest(BaseModel):
    advancedFilter: Annotated[Optional[Any], Field(exclude_none=True)] = None
    endDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    filterDateBy: str = "emision"
    folios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    limit: Annotated[Optional[int], Field(exclude_none=True)] = None
    notFolios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSerieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSeries: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notUuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    rfcEmisor: Annotated[Optional[str], Field(exclude_none=True)] = None
    rfcReceptor: Annotated[Optional[str], Field(exclude_none=True)] = None
    serieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    series: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    skip: Annotated[Optional[int], Field(exclude_none=True)] = None
    sortDirection: Annotated[Optional[str], Field(exclude_none=True)] = None
    sortKey: Annotated[Optional[str], Field(exclude_none=True)] = None
    startDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    tipoNomina: Annotated[Optional[str], Field(exclude_none=True)] = None
    uuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None


class Nomina_getReportNominaTidyJSONRequest(BaseModel):
    advancedFilter: Annotated[Optional[Any], Field(exclude_none=True)] = None
    endDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    filterDateBy: str = "emision"
    folios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    limit: Annotated[Optional[int], Field(exclude_none=True)] = None
    notFolios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSerieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSeries: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notUuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    rfcEmisor: Annotated[Optional[str], Field(exclude_none=True)] = None
    rfcReceptor: Annotated[Optional[str], Field(exclude_none=True)] = None
    serieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    series: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    skip: Annotated[Optional[int], Field(exclude_none=True)] = None
    sortDirection: Annotated[Optional[str], Field(exclude_none=True)] = None
    sortKey: Annotated[Optional[str], Field(exclude_none=True)] = None
    startDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    uuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None


class Pagos_cdpImpuestosRequest(BaseModel):
    advancedFilter: Annotated[Optional[Any], Field(exclude_none=True)] = None
    emails: list[str]
    endDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    excludedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    filterDateBy: Annotated[Optional[str], Field(exclude_none=True)] = None
    folios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    includedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    limit: Annotated[Optional[int], Field(exclude_none=True)] = None
    notFolios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSerieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSeries: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notUuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    rfcEmisor: Annotated[Optional[str], Field(exclude_none=True)] = None
    rfcReceptor: Annotated[Optional[str], Field(exclude_none=True)] = None
    serieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    series: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    skip: Annotated[Optional[int], Field(exclude_none=True)] = None
    sortDirection: Annotated[Optional[str], Field(exclude_none=True)] = None
    sortKey: Annotated[Optional[str], Field(exclude_none=True)] = None
    startDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    uuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None


class Pagos_createPagosReportExcelRequest(BaseModel):
    advancedFilter: Annotated[Optional[Any], Field(exclude_none=True)] = None
    emails: list[str]
    endDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    excludedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    filterDateBy: Annotated[Optional[str], Field(exclude_none=True)] = None
    folios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    includedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    limit: Annotated[Optional[int], Field(exclude_none=True)] = None
    notFolios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSerieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSeries: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notUuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    reportType: str = "OnlyUUID"
    rfcEmisor: Annotated[Optional[str], Field(exclude_none=True)] = None
    rfcReceptor: Annotated[Optional[str], Field(exclude_none=True)] = None
    serieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    series: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    skip: Annotated[Optional[int], Field(exclude_none=True)] = None
    sortDirection: Annotated[Optional[str], Field(exclude_none=True)] = None
    sortKey: Annotated[Optional[str], Field(exclude_none=True)] = None
    startDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    uuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None


class Pagos_getPagosReportJsonRequest(BaseModel):
    advancedFilter: Annotated[Optional[Any], Field(exclude_none=True)] = None
    endDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    filterDateBy: Annotated[Optional[str], Field(exclude_none=True)] = None
    folios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    limit: Annotated[Optional[int], Field(exclude_none=True)] = None
    notFolios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSerieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSeries: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notUuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    rfcEmisor: Annotated[Optional[str], Field(exclude_none=True)] = None
    rfcReceptor: Annotated[Optional[str], Field(exclude_none=True)] = None
    serieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    series: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    skip: Annotated[Optional[int], Field(exclude_none=True)] = None
    sortDirection: Annotated[Optional[str], Field(exclude_none=True)] = None
    sortKey: Annotated[Optional[str], Field(exclude_none=True)] = None
    startDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    uuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None


class Pagos_reportCdpPpdExcelRequest(BaseModel):
    advancedFilter: Annotated[Optional[Any], Field(exclude_none=True)] = None
    emails: list[str]
    endDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    excludedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    filterDateBy: Annotated[Optional[str], Field(exclude_none=True)] = None
    folios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    includedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    limit: Annotated[Optional[int], Field(exclude_none=True)] = None
    notFolios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSerieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSeries: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notUuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    rfcEmisor: Annotated[Optional[str], Field(exclude_none=True)] = None
    rfcReceptor: Annotated[Optional[str], Field(exclude_none=True)] = None
    serieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    series: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    skip: Annotated[Optional[int], Field(exclude_none=True)] = None
    sortDirection: Annotated[Optional[str], Field(exclude_none=True)] = None
    sortKey: Annotated[Optional[str], Field(exclude_none=True)] = None
    startDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    uuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None


class Pagos_reportCdpPpdJsonRequest(BaseModel):
    advancedFilter: Annotated[Optional[Any], Field(exclude_none=True)] = None
    endDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    filterDateBy: Annotated[Optional[str], Field(exclude_none=True)] = None
    folios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    limit: Annotated[Optional[int], Field(exclude_none=True)] = None
    notFolios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSerieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSeries: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notUuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    rfcEmisor: Annotated[Optional[str], Field(exclude_none=True)] = None
    rfcReceptor: Annotated[Optional[str], Field(exclude_none=True)] = None
    serieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    series: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    skip: Annotated[Optional[int], Field(exclude_none=True)] = None
    sortDirection: Annotated[Optional[str], Field(exclude_none=True)] = None
    sortKey: Annotated[Optional[str], Field(exclude_none=True)] = None
    startDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    uuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None


class Pagos_reportPpdGeneralExcelRequest(BaseModel):
    advancedFilter: Annotated[Optional[Any], Field(exclude_none=True)] = None
    emails: list[str]
    endDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    excludedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    folios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    includedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    limit: Annotated[Optional[int], Field(exclude_none=True)] = None
    notFolios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSerieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSeries: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notUuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    rfcEmisor: Annotated[Optional[str], Field(exclude_none=True)] = None
    rfcReceptor: Annotated[Optional[str], Field(exclude_none=True)] = None
    serieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    series: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    skip: Annotated[Optional[int], Field(exclude_none=True)] = None
    sortDirection: Annotated[Optional[str], Field(exclude_none=True)] = None
    sortKey: Annotated[Optional[str], Field(exclude_none=True)] = None
    startDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    uuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None


class Pagos_reportPpdGeneralJsonRequest(BaseModel):
    advancedFilter: Annotated[Optional[Any], Field(exclude_none=True)] = None
    endDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    folios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    limit: Annotated[Optional[int], Field(exclude_none=True)] = None
    notFolios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSerieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSeries: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notUuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    rfcEmisor: Annotated[Optional[str], Field(exclude_none=True)] = None
    rfcReceptor: Annotated[Optional[str], Field(exclude_none=True)] = None
    serieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    series: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    skip: Annotated[Optional[int], Field(exclude_none=True)] = None
    sortDirection: Annotated[Optional[str], Field(exclude_none=True)] = None
    sortKey: Annotated[Optional[str], Field(exclude_none=True)] = None
    startDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    uuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None


class QueueSchema(BaseModel):
    big: int
    limit: int
    medium: int
    semFilter: int
    smallest: int
    super: int
    workers: int


class Relacionados_createPueCdpResumenGrafosReportJSONRequest(BaseModel):
    advancedFilter: Annotated[Optional[Any], Field(exclude_none=True)] = None
    endDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    excludedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    folios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    includedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    limit: Annotated[Optional[int], Field(exclude_none=True)] = None
    notFolios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSerieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSeries: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notUuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    rfcEmisor: Annotated[Optional[str], Field(exclude_none=True)] = None
    rfcReceptor: Annotated[Optional[str], Field(exclude_none=True)] = None
    serieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    series: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    skip: Annotated[Optional[int], Field(exclude_none=True)] = None
    sortDirection: Annotated[Optional[str], Field(exclude_none=True)] = None
    sortKey: Annotated[Optional[str], Field(exclude_none=True)] = None
    startDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    uuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None


class Relacionados_createPueCdpResumenReportExcelRequest(BaseModel):
    advancedFilter: Annotated[Optional[Any], Field(exclude_none=True)] = None
    emails: list[str]
    endDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    excludedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    folios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    includedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    limit: Annotated[Optional[int], Field(exclude_none=True)] = None
    notFolios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSerieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSeries: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notUuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    rfcEmisor: Annotated[Optional[str], Field(exclude_none=True)] = None
    rfcReceptor: Annotated[Optional[str], Field(exclude_none=True)] = None
    serieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    series: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    skip: Annotated[Optional[int], Field(exclude_none=True)] = None
    sortDirection: Annotated[Optional[str], Field(exclude_none=True)] = None
    sortKey: Annotated[Optional[str], Field(exclude_none=True)] = None
    startDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    uuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None


class Relacionados_createPueCdpResumenReportJSONRequest(BaseModel):
    advancedFilter: Annotated[Optional[Any], Field(exclude_none=True)] = None
    endDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    excludedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    folios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    includedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    limit: Annotated[Optional[int], Field(exclude_none=True)] = None
    notFolios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSerieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSeries: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notUuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    rfcEmisor: Annotated[Optional[str], Field(exclude_none=True)] = None
    rfcReceptor: Annotated[Optional[str], Field(exclude_none=True)] = None
    serieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    series: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    skip: Annotated[Optional[int], Field(exclude_none=True)] = None
    sortDirection: Annotated[Optional[str], Field(exclude_none=True)] = None
    sortKey: Annotated[Optional[str], Field(exclude_none=True)] = None
    startDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    uuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None


class Relacionados_createPueCdpSabanaReportExcelRequest(BaseModel):
    advancedFilter: Annotated[Optional[Any], Field(exclude_none=True)] = None
    emails: list[str]
    endDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    excludedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    folios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    includedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    limit: Annotated[Optional[int], Field(exclude_none=True)] = None
    notFolios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSerieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSeries: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notUuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    rfcEmisor: Annotated[Optional[str], Field(exclude_none=True)] = None
    rfcReceptor: Annotated[Optional[str], Field(exclude_none=True)] = None
    serieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    series: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    skip: Annotated[Optional[int], Field(exclude_none=True)] = None
    sortDirection: Annotated[Optional[str], Field(exclude_none=True)] = None
    sortKey: Annotated[Optional[str], Field(exclude_none=True)] = None
    startDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    uuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None


class Relacionados_createPueCdpSabanaReportJSONRequest(BaseModel):
    advancedFilter: Annotated[Optional[Any], Field(exclude_none=True)] = None
    endDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    excludedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    folios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    includedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    limit: Annotated[Optional[int], Field(exclude_none=True)] = None
    notFolios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSerieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSeries: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notUuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    rfcEmisor: Annotated[Optional[str], Field(exclude_none=True)] = None
    rfcReceptor: Annotated[Optional[str], Field(exclude_none=True)] = None
    serieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    series: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    skip: Annotated[Optional[int], Field(exclude_none=True)] = None
    sortDirection: Annotated[Optional[str], Field(exclude_none=True)] = None
    sortKey: Annotated[Optional[str], Field(exclude_none=True)] = None
    startDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    uuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None


class Relacionados_createPueCdpTidyReportExcelRequest(BaseModel):
    advancedFilter: Annotated[Optional[Any], Field(exclude_none=True)] = None
    emails: list[str]
    endDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    excludedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    folios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    includedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    limit: Annotated[Optional[int], Field(exclude_none=True)] = None
    notFolios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSerieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSeries: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notUuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    rfcEmisor: Annotated[Optional[str], Field(exclude_none=True)] = None
    rfcReceptor: Annotated[Optional[str], Field(exclude_none=True)] = None
    serieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    series: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    skip: Annotated[Optional[int], Field(exclude_none=True)] = None
    sortDirection: Annotated[Optional[str], Field(exclude_none=True)] = None
    sortKey: Annotated[Optional[str], Field(exclude_none=True)] = None
    startDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    uuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None


class Relacionados_createPueCdpTidyReportJSONRequest(BaseModel):
    advancedFilter: Annotated[Optional[Any], Field(exclude_none=True)] = None
    endDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    excludedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    folios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    includedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    limit: Annotated[Optional[int], Field(exclude_none=True)] = None
    notFolios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSerieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSeries: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notUuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    rfcEmisor: Annotated[Optional[str], Field(exclude_none=True)] = None
    rfcReceptor: Annotated[Optional[str], Field(exclude_none=True)] = None
    serieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    series: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    skip: Annotated[Optional[int], Field(exclude_none=True)] = None
    sortDirection: Annotated[Optional[str], Field(exclude_none=True)] = None
    sortKey: Annotated[Optional[str], Field(exclude_none=True)] = None
    startDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    uuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None


class Relacionados_createPuePpdGeneralCdpSabanaReportExcelRequest(BaseModel):
    advancedFilter: Annotated[Optional[Any], Field(exclude_none=True)] = None
    emails: list[str]
    endDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    excludedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    folios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    includedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    includedMetodosPago: list[str]
    limit: Annotated[Optional[int], Field(exclude_none=True)] = None
    notFolios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSerieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSeries: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notUuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    rfcEmisor: Annotated[Optional[str], Field(exclude_none=True)] = None
    rfcReceptor: Annotated[Optional[str], Field(exclude_none=True)] = None
    serieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    series: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    skip: Annotated[Optional[int], Field(exclude_none=True)] = None
    sortDirection: Annotated[Optional[str], Field(exclude_none=True)] = None
    sortKey: Annotated[Optional[str], Field(exclude_none=True)] = None
    startDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    uuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None


class Relacionados_createPuePpdGeneralCdpSabanaReportJSONRequest(BaseModel):
    advancedFilter: Annotated[Optional[Any], Field(exclude_none=True)] = None
    endDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    excludedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    folios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    includedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    includedMetodosPago: list[str]
    limit: Annotated[Optional[int], Field(exclude_none=True)] = None
    notFolios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSerieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSeries: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notUuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    rfcEmisor: Annotated[Optional[str], Field(exclude_none=True)] = None
    rfcReceptor: Annotated[Optional[str], Field(exclude_none=True)] = None
    serieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    series: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    skip: Annotated[Optional[int], Field(exclude_none=True)] = None
    sortDirection: Annotated[Optional[str], Field(exclude_none=True)] = None
    sortKey: Annotated[Optional[str], Field(exclude_none=True)] = None
    startDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    uuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None


class Relacionados_createPuePpdGeneralSabanaMomenReportExcelRequest(BaseModel):
    advancedFilter: Annotated[Optional[Any], Field(exclude_none=True)] = None
    emails: list[str]
    endDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    excludedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    folios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    includedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    includedMetodosPago: list[str]
    limit: Annotated[Optional[int], Field(exclude_none=True)] = None
    notFolios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSerieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSeries: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notUuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    rfcEmisor: Annotated[Optional[str], Field(exclude_none=True)] = None
    rfcReceptor: Annotated[Optional[str], Field(exclude_none=True)] = None
    serieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    series: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    skip: Annotated[Optional[int], Field(exclude_none=True)] = None
    sortDirection: Annotated[Optional[str], Field(exclude_none=True)] = None
    sortKey: Annotated[Optional[str], Field(exclude_none=True)] = None
    startDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    uuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None


class Relacionados_createPuePpdGeneralSabanaMomenReportJSONRequest(BaseModel):
    advancedFilter: Annotated[Optional[Any], Field(exclude_none=True)] = None
    endDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    excludedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    folios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    includedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    includedMetodosPago: list[str]
    limit: Annotated[Optional[int], Field(exclude_none=True)] = None
    notFolios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSerieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSeries: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notUuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    rfcEmisor: Annotated[Optional[str], Field(exclude_none=True)] = None
    rfcReceptor: Annotated[Optional[str], Field(exclude_none=True)] = None
    serieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    series: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    skip: Annotated[Optional[int], Field(exclude_none=True)] = None
    sortDirection: Annotated[Optional[str], Field(exclude_none=True)] = None
    sortKey: Annotated[Optional[str], Field(exclude_none=True)] = None
    startDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    uuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None


class Relacionados_createPuePpdGeneralSabanaPagosGrafosExcelRequest(BaseModel):
    advancedFilter: Annotated[Optional[Any], Field(exclude_none=True)] = None
    emails: list[str]
    endDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    excludedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    folios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    includedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    limit: Annotated[Optional[int], Field(exclude_none=True)] = None
    notFolios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSerieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSeries: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notUuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    rfcEmisor: Annotated[Optional[str], Field(exclude_none=True)] = None
    rfcReceptor: Annotated[Optional[str], Field(exclude_none=True)] = None
    serieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    series: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    skip: Annotated[Optional[int], Field(exclude_none=True)] = None
    sortDirection: Annotated[Optional[str], Field(exclude_none=True)] = None
    sortKey: Annotated[Optional[str], Field(exclude_none=True)] = None
    startDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    uuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None


class Relacionados_createPuePpdGeneralSabanaPagosGrafosReportJSONRequest(BaseModel):
    advancedFilter: Annotated[Optional[Any], Field(exclude_none=True)] = None
    endDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    excludedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    folios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    includedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    limit: Annotated[Optional[int], Field(exclude_none=True)] = None
    notFolios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSerieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSeries: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notUuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    rfcEmisor: Annotated[Optional[str], Field(exclude_none=True)] = None
    rfcReceptor: Annotated[Optional[str], Field(exclude_none=True)] = None
    serieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    series: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    skip: Annotated[Optional[int], Field(exclude_none=True)] = None
    sortDirection: Annotated[Optional[str], Field(exclude_none=True)] = None
    sortKey: Annotated[Optional[str], Field(exclude_none=True)] = None
    startDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    uuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None


class Relacionados_createPuePpdGeneralSabanaPagosReportExcelRequest(BaseModel):
    advancedFilter: Annotated[Optional[Any], Field(exclude_none=True)] = None
    emails: list[str]
    endDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    excludedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    folios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    includedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    limit: Annotated[Optional[int], Field(exclude_none=True)] = None
    notFolios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSerieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSeries: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notUuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    rfcEmisor: Annotated[Optional[str], Field(exclude_none=True)] = None
    rfcReceptor: Annotated[Optional[str], Field(exclude_none=True)] = None
    serieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    series: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    skip: Annotated[Optional[int], Field(exclude_none=True)] = None
    sortDirection: Annotated[Optional[str], Field(exclude_none=True)] = None
    sortKey: Annotated[Optional[str], Field(exclude_none=True)] = None
    startDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    uuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None


class Relacionados_createPuePpdGeneralSabanaPagosReportJSONRequest(BaseModel):
    advancedFilter: Annotated[Optional[Any], Field(exclude_none=True)] = None
    endDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    excludedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    folios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    includedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    limit: Annotated[Optional[int], Field(exclude_none=True)] = None
    notFolios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSerieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSeries: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notUuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    rfcEmisor: Annotated[Optional[str], Field(exclude_none=True)] = None
    rfcReceptor: Annotated[Optional[str], Field(exclude_none=True)] = None
    serieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    series: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    skip: Annotated[Optional[int], Field(exclude_none=True)] = None
    sortDirection: Annotated[Optional[str], Field(exclude_none=True)] = None
    sortKey: Annotated[Optional[str], Field(exclude_none=True)] = None
    startDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    uuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None


class Relacionados_createPuePpdGeneralSabanaReportExcelRequest(BaseModel):
    advancedFilter: Annotated[Optional[Any], Field(exclude_none=True)] = None
    emails: list[str]
    endDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    excludedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    folios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    includedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    includedMetodosPago: list[str]
    limit: Annotated[Optional[int], Field(exclude_none=True)] = None
    notFolios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSerieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSeries: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notUuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    reportHeadersOrderId: Annotated[Optional[str], Field(exclude_none=True)] = None
    rfcEmisor: Annotated[Optional[str], Field(exclude_none=True)] = None
    rfcReceptor: Annotated[Optional[str], Field(exclude_none=True)] = None
    serieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    series: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    skip: Annotated[Optional[int], Field(exclude_none=True)] = None
    sortDirection: Annotated[Optional[str], Field(exclude_none=True)] = None
    sortKey: Annotated[Optional[str], Field(exclude_none=True)] = None
    startDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    uuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None


class Relacionados_createPuePpdGeneralSabanaReportJSONRequest(BaseModel):
    advancedFilter: Annotated[Optional[Any], Field(exclude_none=True)] = None
    endDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    excludedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    folios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    includedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    includedMetodosPago: list[str]
    limit: Annotated[Optional[int], Field(exclude_none=True)] = None
    notFolios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSerieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSeries: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notUuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    rfcEmisor: Annotated[Optional[str], Field(exclude_none=True)] = None
    rfcReceptor: Annotated[Optional[str], Field(exclude_none=True)] = None
    serieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    series: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    skip: Annotated[Optional[int], Field(exclude_none=True)] = None
    sortDirection: Annotated[Optional[str], Field(exclude_none=True)] = None
    sortKey: Annotated[Optional[str], Field(exclude_none=True)] = None
    startDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    uuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None


class Relacionados_createPuePpdGeneralSabanaTrasladoReportExcelRequest(BaseModel):
    advancedFilter: Annotated[Optional[Any], Field(exclude_none=True)] = None
    emails: list[str]
    endDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    excludedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    folios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    includedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    limit: Annotated[Optional[int], Field(exclude_none=True)] = None
    notFolios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSerieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSeries: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notUuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    rfcEmisor: Annotated[Optional[str], Field(exclude_none=True)] = None
    rfcReceptor: Annotated[Optional[str], Field(exclude_none=True)] = None
    serieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    series: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    skip: Annotated[Optional[int], Field(exclude_none=True)] = None
    sortDirection: Annotated[Optional[str], Field(exclude_none=True)] = None
    sortKey: Annotated[Optional[str], Field(exclude_none=True)] = None
    startDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    uuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None


class Relacionados_createPuePpdGeneralSabanaTrasladoReportJSONRequest(BaseModel):
    advancedFilter: Annotated[Optional[Any], Field(exclude_none=True)] = None
    endDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    excludedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    folios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    includedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    limit: Annotated[Optional[int], Field(exclude_none=True)] = None
    notFolios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSerieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSeries: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notUuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    rfcEmisor: Annotated[Optional[str], Field(exclude_none=True)] = None
    rfcReceptor: Annotated[Optional[str], Field(exclude_none=True)] = None
    serieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    series: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    skip: Annotated[Optional[int], Field(exclude_none=True)] = None
    sortDirection: Annotated[Optional[str], Field(exclude_none=True)] = None
    sortKey: Annotated[Optional[str], Field(exclude_none=True)] = None
    startDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    uuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None


class Relacionados_createPuePpdGeneralTidyReportExcelRequest(BaseModel):
    advancedFilter: Annotated[Optional[Any], Field(exclude_none=True)] = None
    emails: list[str]
    endDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    excludedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    folios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    includedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    includedMetodosPago: list[str]
    limit: Annotated[Optional[int], Field(exclude_none=True)] = None
    notFolios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSerieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSeries: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notUuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    rfcEmisor: Annotated[Optional[str], Field(exclude_none=True)] = None
    rfcReceptor: Annotated[Optional[str], Field(exclude_none=True)] = None
    serieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    series: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    skip: Annotated[Optional[int], Field(exclude_none=True)] = None
    sortDirection: Annotated[Optional[str], Field(exclude_none=True)] = None
    sortKey: Annotated[Optional[str], Field(exclude_none=True)] = None
    startDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    uuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None


class Relacionados_createPuePpdGeneralTidyReportJSONRequest(BaseModel):
    advancedFilter: Annotated[Optional[Any], Field(exclude_none=True)] = None
    endDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    excludedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    folios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    includedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    includedMetodosPago: list[str]
    limit: Annotated[Optional[int], Field(exclude_none=True)] = None
    notFolios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSerieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSeries: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notUuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    rfcEmisor: Annotated[Optional[str], Field(exclude_none=True)] = None
    rfcReceptor: Annotated[Optional[str], Field(exclude_none=True)] = None
    serieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    series: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    skip: Annotated[Optional[int], Field(exclude_none=True)] = None
    sortDirection: Annotated[Optional[str], Field(exclude_none=True)] = None
    sortKey: Annotated[Optional[str], Field(exclude_none=True)] = None
    startDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    uuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None


class Relacionados_createPuePpdGeneralTidyTrasladoReportExcelRequest(BaseModel):
    advancedFilter: Annotated[Optional[Any], Field(exclude_none=True)] = None
    emails: list[str]
    endDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    excludedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    folios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    includedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    limit: Annotated[Optional[int], Field(exclude_none=True)] = None
    notFolios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSerieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSeries: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notUuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    rfcEmisor: Annotated[Optional[str], Field(exclude_none=True)] = None
    rfcReceptor: Annotated[Optional[str], Field(exclude_none=True)] = None
    serieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    series: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    skip: Annotated[Optional[int], Field(exclude_none=True)] = None
    sortDirection: Annotated[Optional[str], Field(exclude_none=True)] = None
    sortKey: Annotated[Optional[str], Field(exclude_none=True)] = None
    startDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    uuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None


class Relacionados_createPuePpdGeneralTidyTrasladoReportJSONRequest(BaseModel):
    advancedFilter: Annotated[Optional[Any], Field(exclude_none=True)] = None
    endDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    excludedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    folios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    includedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    limit: Annotated[Optional[int], Field(exclude_none=True)] = None
    notFolios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSerieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSeries: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notUuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    rfcEmisor: Annotated[Optional[str], Field(exclude_none=True)] = None
    rfcReceptor: Annotated[Optional[str], Field(exclude_none=True)] = None
    serieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    series: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    skip: Annotated[Optional[int], Field(exclude_none=True)] = None
    sortDirection: Annotated[Optional[str], Field(exclude_none=True)] = None
    sortKey: Annotated[Optional[str], Field(exclude_none=True)] = None
    startDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    uuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None


class Relacionados_createPuePpdResumenReportExcelRequest(BaseModel):
    advancedFilter: Annotated[Optional[Any], Field(exclude_none=True)] = None
    emails: list[str]
    endDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    excludedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    folios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    includedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    includedMetodosPago: list[str]
    limit: Annotated[Optional[int], Field(exclude_none=True)] = None
    notFolios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSerieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSeries: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notUuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    rfcEmisor: Annotated[Optional[str], Field(exclude_none=True)] = None
    rfcReceptor: Annotated[Optional[str], Field(exclude_none=True)] = None
    serieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    series: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    skip: Annotated[Optional[int], Field(exclude_none=True)] = None
    sortDirection: Annotated[Optional[str], Field(exclude_none=True)] = None
    sortKey: Annotated[Optional[str], Field(exclude_none=True)] = None
    startDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    uuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None


class Relacionados_createRelacionadosPuePpdGrafosTidyReportJSONRequest(BaseModel):
    advancedFilter: Annotated[Optional[Any], Field(exclude_none=True)] = None
    endDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    folios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    includedMetodosPago: list[str]
    limit: Annotated[Optional[int], Field(exclude_none=True)] = None
    notFolios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSerieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSeries: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notUuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    rfcEmisor: Annotated[Optional[str], Field(exclude_none=True)] = None
    rfcReceptor: Annotated[Optional[str], Field(exclude_none=True)] = None
    serieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    series: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    skip: Annotated[Optional[int], Field(exclude_none=True)] = None
    sortDirection: Annotated[Optional[str], Field(exclude_none=True)] = None
    sortKey: Annotated[Optional[str], Field(exclude_none=True)] = None
    startDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    uuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None


class Relacionados_createRelacionadosPuePpdSabanaReportExcelRequest(BaseModel):
    advancedFilter: Annotated[Optional[Any], Field(exclude_none=True)] = None
    emails: list[str]
    endDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    excludedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    folios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    includedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    includedMetodosPago: list[str]
    limit: Annotated[Optional[int], Field(exclude_none=True)] = None
    notFolios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSerieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSeries: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notUuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    rfcEmisor: Annotated[Optional[str], Field(exclude_none=True)] = None
    rfcReceptor: Annotated[Optional[str], Field(exclude_none=True)] = None
    serieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    series: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    skip: Annotated[Optional[int], Field(exclude_none=True)] = None
    sortDirection: Annotated[Optional[str], Field(exclude_none=True)] = None
    sortKey: Annotated[Optional[str], Field(exclude_none=True)] = None
    startDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    uuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None


class Relacionados_createRelacionadosResumenReportJSONRequest(BaseModel):
    advancedFilter: Annotated[Optional[Any], Field(exclude_none=True)] = None
    endDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    folios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    includedMetodosPago: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    limit: Annotated[Optional[int], Field(exclude_none=True)] = None
    notFolios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSerieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSeries: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notUuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    rfcEmisor: Annotated[Optional[str], Field(exclude_none=True)] = None
    rfcReceptor: Annotated[Optional[str], Field(exclude_none=True)] = None
    serieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    series: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    skip: Annotated[Optional[int], Field(exclude_none=True)] = None
    sortDirection: Annotated[Optional[str], Field(exclude_none=True)] = None
    sortKey: Annotated[Optional[str], Field(exclude_none=True)] = None
    startDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    uuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None


class Relacionados_createRelacionadosTidyReportExcelRequest(BaseModel):
    advancedFilter: Annotated[Optional[Any], Field(exclude_none=True)] = None
    emails: list[str]
    endDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    excludedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    folios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    includedHeaders: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    includedMetodosPago: list[str]
    limit: Annotated[Optional[int], Field(exclude_none=True)] = None
    notFolios: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSerieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notSeries: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    notUuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    rfcEmisor: Annotated[Optional[str], Field(exclude_none=True)] = None
    rfcReceptor: Annotated[Optional[str], Field(exclude_none=True)] = None
    serieFolio: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    series: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    skip: Annotated[Optional[int], Field(exclude_none=True)] = None
    sortDirection: Annotated[Optional[str], Field(exclude_none=True)] = None
    sortKey: Annotated[Optional[str], Field(exclude_none=True)] = None
    startDate: Annotated[Optional[str], Field(exclude_none=True)] = None
    uuids: Annotated[Optional[list[str]], Field(exclude_none=True)] = None


class Relacionados_registerNewReportHeadersOrderRequest(BaseModel):
    name: str
    reportHeaderOrder: list[str]


class Relacionados_registerUpdateReportHeadersOrderRequest(BaseModel):
    name: Annotated[Optional[str], Field(exclude_none=True)] = None
    reportHeaderOrder: Annotated[Optional[list[str]], Field(exclude_none=True)] = None


class ReportOrder(BaseModel):
    headerOrder: Annotated[Optional[list[str]], Field(exclude_none=True)] = None
    id: Annotated[Optional[str], Field(exclude_none=True)] = None
    name: Annotated[Optional[str], Field(exclude_none=True)] = None


class Reports_blockReportRequest(BaseModel):
    Additional: Annotated[Optional[Any], Field(exclude_none=True)] = None
    _id: Annotated[Optional[str], Field(exclude_none=True)] = None
    block: bool


class Reprocess_reprocess_reportRequest(BaseModel):
    id: str


class RequestReportSchema(BaseModel):
    bucket_files: list[BucketFile]
    email: list[str]
    email_bcc: list[str]
    email_cc: Any
    period: str
    rfc: str
    show_not_found: bool
    tipo_archivo: str


class ResponseBool(BaseModel):
    data: bool
    detail: str
    success: bool


class ResponseKoreResponse(BaseModel):
    data: KoreResponse
    detail: str
    success: bool


class ResponseListComprobanteCdpPpd(BaseModel):
    data: list[ComprobanteCdpPpd]
    detail: str
    success: bool


class ResponseListComprobanteNominaSabana(BaseModel):
    data: list[ComprobanteNominaSabana]
    detail: str
    success: bool


class ResponseListComprobanteNominaTidy(BaseModel):
    data: list[ComprobanteNominaTidy]
    detail: str
    success: bool


class ResponseListComprobantePPD(BaseModel):
    data: list[ComprobantePPD]
    detail: str
    success: bool


class ResponseListComprobantePagosV2(BaseModel):
    data: list[ComprobantePagosV2]
    detail: str
    success: bool


class ResponseListComprobantePueCdpResumen(BaseModel):
    data: list[ComprobantePueCdpResumen]
    detail: str
    success: bool


class ResponseListComprobantePueCdpSabana(BaseModel):
    data: list[ComprobantePueCdpSabana]
    detail: str
    success: bool


class ResponseListComprobantePueCdpTidy(BaseModel):
    data: list[ComprobantePueCdpTidy]
    detail: str
    success: bool


class ResponseListComprobantePuePpdGeneralCdpSabana(BaseModel):
    data: list[ComprobantePuePpdGeneralCdpSabana]
    detail: str
    success: bool


class ResponseListComprobantePuePpdGeneralSabana(BaseModel):
    data: list[ComprobantePuePpdGeneralSabana]
    detail: str
    success: bool


class ResponseListComprobantePuePpdGeneralSabanaMomentos(BaseModel):
    data: list[ComprobantePuePpdGeneralSabanaMomentos]
    detail: str
    success: bool


class ResponseListComprobantePuePpdGeneralTidy(BaseModel):
    data: list[ComprobantePuePpdGeneralTidy]
    detail: str
    success: bool


class ResponseListComprobanteRelacionadosResumen(BaseModel):
    data: list[ComprobanteRelacionadosResumen]
    detail: str
    success: bool


class ResponseListComprobanteRelacionadosSabana(BaseModel):
    data: list[ComprobanteRelacionadosSabana]
    detail: str
    success: bool


class ResponseListComprobanteRelacionadosTidy(BaseModel):
    data: list[ComprobanteRelacionadosTidy]
    detail: str
    success: bool


class ResponseListConceptoNominaRow(BaseModel):
    data: list[ConceptoNominaRow]
    detail: str
    success: bool


class ResponseListAny(BaseModel):
    data: list[Any]
    detail: str
    success: bool


class ResponseListNominaDetalleGeneral(BaseModel):
    data: list[NominaDetalleGeneral]
    detail: str
    success: bool


class ResponseListReportOrder(BaseModel):
    data: list[ReportOrder]
    detail: str
    success: bool


class ResponseListString(BaseModel):
    data: list[str]
    detail: str
    success: bool


class ResponseMapStringAny(BaseModel):
    data: Any
    detail: str
    success: bool


class ResponseMapStringObjectID(BaseModel):
    data: dict[str, str]
    detail: str
    success: bool


class ResponseObjectID(BaseModel):
    data: str
    detail: str
    success: bool


class ResponseQueueSchema(BaseModel):
    data: QueueSchema
    detail: str
    success: bool


class ResponseReportOrder(BaseModel):
    data: ReportOrder
    detail: str
    success: bool


class ResponseRequestReportSchema(BaseModel):
    data: RequestReportSchema
    detail: str
    success: bool


class ResponseString(BaseModel):
    data: str
    detail: str
    success: bool
