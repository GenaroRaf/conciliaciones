from enum import Enum

from pydantic import BaseModel


class TipoImpuesto(Enum):
    ISR = "001"
    IVA = "002"
    IEPS = "003"


class Impuesto(BaseModel):
    tipoImpuesto: str
    base: float
    baseMxn: float | None = None
    impuesto: str
    tipoFactor: str
    tasaOCuota: float | None = None
    importe: float | None = None
    importeMxn: float | None = None
