import pandas as pd
from k_link.extensions import Nativo
from loggerk import LoggerK

SYMBOLS = ["%", "$"]


class ValidaDataTypes:
    _logger: LoggerK

    def __init__(self, values: pd.Series, dtype: Nativo, date_format: str):
        super().__init__()
        self._logger = LoggerK(self.__class__.__name__)
        self.values = values
        self.dtype = dtype
        self.date_format = date_format

    def validate_data(self) -> pd.Series:
        # Limpia los valores iniciales
        clean_values = self.values.apply(self.clean_value)

        # Selecciona la función de validación adecuada
        if self.dtype == Nativo.INT:
            func = self.validate_int
        elif self.dtype == Nativo.FLOAT:
            func = self.validate_float
        elif self.dtype == Nativo.EU_NUM:
            func = self.validate_european_number
        elif self.dtype == Nativo.STRING:
            func = self.validate_str
        elif self.dtype == Nativo.DATE:
            func = self.validate_date
        else:
            raise ValueError(f"Tipo de dato no soportado: {self.dtype}")

        # Aplica la validación
        clean_values = clean_values.apply(func)
        return clean_values

    def validate_int(self, value) -> int | None:
        """Valida si un valor es un entero. Si no, devuelve None."""
        try:
            return int(float(value.replace(",", "").replace(".", "")))
        except ValueError:
            return None

    def validate_european_number(self, value) -> float | None:
        """
        Valida si un valor es un número en formato europeo (coma como separador decimal).
        Si es válido, lo convierte a un flotante. Si no, devuelve None.
        """
        try:
            # Reemplaza separador de miles (.) y convierte la coma en punto (.)
            value = value.replace(".", "").replace(",", ".")
            return float(value)
        except (ValueError, AttributeError):
            return None

    def validate_float(self, value) -> float | None:
        """Valida si un valor es un flotante. Si no, devuelve None."""
        try:
            return float(value.replace(",", ""))
        except ValueError:
            return None

    def validate_str(self, value) -> str | None:
        """Valida si un valor es una cadena. Si no, devuelve None."""
        return value.strip() if isinstance(value, str) else None

    def validate_date(self, value) -> pd.Timestamp | None:
        """
        Valida si un valor es una fecha según el formato especificado. Si no, devuelve None.
        """
        try:
            value = pd.to_datetime(value, format=self.date_format, errors="coerce")

            return value if not pd.isna(value) else None

        except Exception as e:
            self._logger.warning(f"Error al validar fecha '{value}': {e}")
            return None

    def clean_value(self, value) -> str:
        """
        Limpia los valores eliminando espacios, símbolos y caracteres innecesarios.
        """
        if not isinstance(value, str):
            value = str(value)
        value = value.strip()  # Elimina espacios antes/después
        for symbol in SYMBOLS:
            value = value.replace(symbol, "")
        return value
