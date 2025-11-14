from typing import Annotated

from k_link.utils.pydantic_types import Date
from pydantic import BaseModel, Field


class Metadata(BaseModel):
    total: int
    skip: int
    limit: int


class Contribuyente(BaseModel):
    rfc: Annotated[str, Field(alias="Rfc")]
    nombre: Annotated[str, Field(alias="Nombre")]
    regimen_fiscal: Annotated[str | None, Field(alias="RegimenFiscal")] = None
    uso_cfdi: Annotated[str | None, Field(alias="UsoCFDI")] = None


class KoreCfdi(BaseModel):
    comprobante: Annotated[bool, Field(alias="Comprobante")]
    uuid: Annotated[str, Field(alias="Uuid")]
    emisor: Annotated[Contribuyente, Field(alias="Emisor")]
    receptor: Annotated[Contribuyente, Field(alias="Receptor")]
    fecha_emision: Annotated[Date, Field(alias="FechaEmision", default_factory=Date)]
    fecha_timbrado: Annotated[Date, Field(alias="FechaTibrado", default_factory=Date)]
    folio: Annotated[str | None, Field(alias="Folio")] = None
    serie: Annotated[str | None, Field(alias="Serie")] = None
    total: Annotated[float, Field(alias="Total")]
    subtotal: Annotated[float | None, Field(alias="Subtotal")] = None
    impuestos: Annotated[float | None, Field(alias="Impuesto")] = None
    moneda: Annotated[str | None, Field(alias="Moneda")] = None
    tipo_cambio: Annotated[str | None, Field(alias="TipoCambio")] = None
    tipo_comprobante: Annotated[str | None, Field(alias="TipoComprobante")] = None
    metodo_pago: Annotated[str | None, Field(alias="MetodoPago")] = None
    vigente: Annotated[bool, Field(alias="Vigente")]


class KoreResponse(BaseModel):
    metadata: Metadata
    data: list[KoreCfdi]
