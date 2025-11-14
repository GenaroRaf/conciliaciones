from enum import Enum


def hex_to_argb(hex_color: str) -> str:
    """Convierte #RRGGBB a FFRRGGBB para openpyxl y valida formato."""
    if not hex_color:
        raise ValueError("El color no puede ser None o vacío")

    if hex_color.startswith("#"):
        hex_color = hex_color[1:]

    if len(hex_color) != 6:
        raise ValueError(f"Color inválido: '{hex_color}'. Debe tener 6 dígitos hex.")

    return f"FF{hex_color.upper()}"


class ColoresHeaders(Enum):
    AZUL_ULTRAMAR = ["#0B79AA", "#065E8E", "#004D82", "#00456B", "#00415E"]
    VERDE_MENTA = ["#A2F9D8", "#81EAC4", "#68D9B4", "#52CEA2", "#36C18C"]
    AZUL_NAUTICO = ["#39B6D3", "#2396B5", "#1B7A9A", "#0F6E87", "#065466"]
    AZUL_FISCAL = ["#C6E3F7", "#73C1EF", "#0093E5", "#0075AF", "#006896"]
    VERDE_CLIENTES = ["#C8EBE4", "#43C9AF", "#00B894", "#00A787", "#009E80"]
    AZUL_CIELO_PROVEEDORES = ["#C2DDEA", "#5EA4BF", "#4393B0", "#2983A2", "#1B7A9A"]
    AMARILLO_EMPLEADOS = ["#FCF0B7", "#FDEA96", "#FFE05F", "#F6CE24", "#EFC30C"]
    ROJO_CANCELADO = ["#dc5035"]


class ColoresTexto(Enum):
    COLORES_TEXTO = ["#FFFFFF", "#000000"]  # Blanco y negro


class HeaderStyles(Enum):
    ERP = {
        "bg_color": hex_to_argb(ColoresHeaders.VERDE_CLIENTES.value[1]),
        "font_color": hex_to_argb(ColoresTexto.COLORES_TEXTO.value[1]),
    }
    CLEAN_DATA = {
        "bg_color": hex_to_argb(ColoresHeaders.AZUL_NAUTICO.value[1]),
        "font_color": hex_to_argb(ColoresTexto.COLORES_TEXTO.value[0]),
    }
    SAT = {
        "bg_color": hex_to_argb(ColoresHeaders.AZUL_FISCAL.value[3]),
        "font_color": hex_to_argb(ColoresTexto.COLORES_TEXTO.value[0]),
    }
    PIVOTE = {
        "bg_color": hex_to_argb(ColoresHeaders.AMARILLO_EMPLEADOS.value[0]),
        "font_color": hex_to_argb(ColoresTexto.COLORES_TEXTO.value[1]),
    }
    DIFF = {
        "bg_color": hex_to_argb(ColoresHeaders.AMARILLO_EMPLEADOS.value[2]),
        "font_color": hex_to_argb(ColoresTexto.COLORES_TEXTO.value[1]),
    }
    LABEL = {
        "bg_color": hex_to_argb(ColoresHeaders.AMARILLO_EMPLEADOS.value[1]),
        "font_color": hex_to_argb(ColoresTexto.COLORES_TEXTO.value[1]),
    }
    VALIDATION = {
        "bg_color": hex_to_argb(ColoresHeaders.AMARILLO_EMPLEADOS.value[1]),
        "font_color": hex_to_argb(ColoresTexto.COLORES_TEXTO.value[1]),
    }
    REPORT_TYPE = {
        "bg_color": hex_to_argb(ColoresHeaders.AZUL_CIELO_PROVEEDORES.value[1]),
        "font_color": hex_to_argb(ColoresTexto.COLORES_TEXTO.value[0]),
    }


class DataStyles(Enum):
    FECHA = {"num_format": "yyyy-mm-dd"}
    TEXTO = {"align": "left"}
    NUMERO = {"num_format": "#,##0.00", "align": "right"}
    MONEDA = {"num_format": "$#,##0.00", "align": "right"}
    PORCENTAJE = {"align": "right", "border": 1, "num_format": "0.00%"}
    BOOLEANO = {"align": "left"}
    INTEGER = {"align": "left"}


class SummaryStyles(Enum):
    HEADER = {
        "bold": True,
        "font_size": 14,
        "align": "center",
        "valign": "vcenter",
        "fg_color": hex_to_argb(ColoresHeaders.AZUL_FISCAL.value[3]),
        "border": 1,
        "font_color": hex_to_argb(ColoresTexto.COLORES_TEXTO.value[0]),
    }

    SUBHEADER = {
        "bold": True,
        "font_size": 12,
        "align": "left",
        "fg_color": hex_to_argb(ColoresHeaders.VERDE_CLIENTES.value[1]),
        "border": 1,
    }

    DATA = {
        "font_size": 10,
        "align": "left",
        "fg_color": hex_to_argb(ColoresTexto.COLORES_TEXTO.value[0]),
        "border": 1,
    }

    TABLE_HEADER = {
        "bold": True,
        "align": "center",
        "valign": "vcenter",
        "fg_color": hex_to_argb(ColoresHeaders.VERDE_CLIENTES.value[1]),
        "border": 1,
    }


class PivotTableStyles(Enum):
    MERGE = {
        "bold": True,
        "align": "center",
        "valign": "vcenter",
        "border": 1,
        "bg_color": hex_to_argb(ColoresHeaders.AZUL_FISCAL.value[3]),
        "font_color": hex_to_argb("#FFFFFF"),
    }

    PIVOT_HEADER = {
        "bold": True,
        "bg_color": hex_to_argb(ColoresHeaders.VERDE_CLIENTES.value[1]),
        "align": "center",
        "valign": "vcenter",
        "border": 1,
    }

    NUMERO = {"bold": True, "num_format": "#,##0", "border": 1, "align": "right"}
    MONEDA = {"bold": True, "num_format": "$#,##0.00", "border": 1, "align": "right"}
    TEXTO = {"bold": True, "align": "left", "border": 1}


class CellStyle(Enum):
    TIPO_MONEDA = {"font_color": hex_to_argb(ColoresHeaders.AZUL_FISCAL.value[2])}
    TEXTO = {"bold": True, "align": "left", "border": 1}
    CANCELADO = {"font_color": hex_to_argb(ColoresHeaders.ROJO_CANCELADO.value[0])}
