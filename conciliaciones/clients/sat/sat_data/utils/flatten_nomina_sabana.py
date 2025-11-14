import re

from conciliaciones.clients.sat.sat_data.utils.flatten_dict import flatten_dict


def get_concepto_name(prefix: str, name: str, tipo: str, clave: str) -> str:
    return f"{prefix}-{tipo} Clave {clave} Importe {name}"


def get_concepto_headers_dict(nomina_item: dict) -> dict:
    conceptos_headers = {}
    conceptos_percepciones_headers = {}
    conceptos_deducciones_headers = {}
    conceptos_otros_pagos_headers = {}
    conceptos_incapacidades_headers = {}
    horas_extra_headers = {}

    conceptos = nomina_item.get("conceptos", {})

    percepciones = conceptos.get("percepciones") or []
    for percepcion in percepciones:
        gravado_name = get_concepto_name(
            "P",
            f"Gravado {percepcion.get('concepto', '')}",
            percepcion.get("tipoPercepcion", ""),
            percepcion.get("clave", ""),
        )
        conceptos_percepciones_headers[gravado_name] = percepcion.get(
            "importeGravado", 0
        )

        exento_name = get_concepto_name(
            "P",
            f"Exento {percepcion.get('concepto', '')}",
            percepcion.get("tipoPercepcion", ""),
            percepcion.get("clave", ""),
        )
        conceptos_percepciones_headers[exento_name] = percepcion.get("importeExento", 0)

    # Procesar deducciones (ordenadas)
    deducciones = conceptos.get("deducciones") or []
    for deduccion in deducciones:
        name = get_concepto_name(
            "D",
            deduccion.get("concepto", ""),
            deduccion.get("tipoDeduccion", ""),
            deduccion.get("clave", ""),
        )
        conceptos_deducciones_headers[name] = deduccion.get("importe", 0)

    # Procesar otros pagos (ordenados)
    otros_pagos = conceptos.get("otrosPagos") or []
    for otro_pago in otros_pagos:
        name = get_concepto_name(
            "O",
            otro_pago.get("concepto", ""),
            otro_pago.get("tipoOtroPago", ""),
            otro_pago.get("clave", ""),
        )
        conceptos_otros_pagos_headers[name] = otro_pago.get("importe", 0)

    # Procesar incapacidades (ordenadas)
    incapacidades = conceptos.get("incapacidades") or []
    for incapacidad in incapacidades:
        name = f"I Importe Incapacidad {incapacidad.get('tipoIncapacidad', '')}"
        conceptos_incapacidades_headers[name] = incapacidad.get("importeMonetario", 0)

    conceptos_headers = {
        **conceptos_percepciones_headers,
        **conceptos_deducciones_headers,
        **conceptos_otros_pagos_headers,
        **conceptos_incapacidades_headers,
    }

    # Procesar horas extra (ordenadas)
    horas_extra_ordenadas = sorted(
        nomina_item.get("horasExtra") or [], key=lambda x: x.get("tipoHoras", "")
    )

    for hora_extra in horas_extra_ordenadas:
        dias_header = f"Días Horas Extra {hora_extra.get('tipoHoras', '')}"
        horas_extra_headers[dias_header] = hora_extra.get("dias", 0)

        horas_header = f"Horas Extra {hora_extra.get('tipoHoras', '')}"
        horas_extra_headers[horas_header] = hora_extra.get("horasExtra", 0)

        importe_header = f"Importe Horas Extra {hora_extra.get('tipoHoras', '')}"
        horas_extra_headers[importe_header] = hora_extra.get("importePagado", 0)

    return {**conceptos_headers, **horas_extra_headers}


def get_nomina_headers_dict(nomina_item: dict) -> dict:
    flat_basic_data = flatten_dict(nomina_item)

    # Filtrar las columnas que contengan conceptos para evitar duplicados
    excluded_patterns = [
        "conceptos_deducciones",
        "conceptos_percepciones",
        "conceptos_otrosPagos",
        "conceptos_incapacidades",
        "horasExtra",
        "detalleConceptos_detallePercepcionesNomina_totalSueldos",
        "detalleConceptos_detallePercepcionesNomina_totalGravado",
        "detalleConceptos_detallePercepcionesNomina_totalExento",
        "detalleConceptos_detalleDeduccionesNomina_totalOtrasDeducciones",
        "detalleConceptos_detalleDeduccionesNomina_totalImpuestosRetenidos",
    ]

    for pattern in excluded_patterns:
        flat_basic_data = {k: v for k, v in flat_basic_data.items() if pattern not in k}

    concepto_headers = get_concepto_headers_dict(nomina_item)
    return {**flat_basic_data, **concepto_headers}


def order_headers_by_nomina(headers: list[str]) -> list[str]:
    weighs = {
        "P": 0,  # Percepciones
        "D": 1,  # Deducciones
        "O": 2,  # Otros pagos
        "I": 3,  # Incapacidades
    }
    weighs_horas_extra = {
        "D": 0,  # Días
        "H": 1,  # Horas
        "I": 2,  # Importe
    }

    def header_key(
        header,
    ):  # -> tuple[int, int, Any] | tuple[Literal[4], int, Any] | tuple...:# -> tuple[int, int, Any] | tuple[Literal[4], int, Any] | tuple...:
        # Para conceptos normales: P-XXX, D-XXX, O-XXX, I ...
        match = re.match(r"([PDOI])-?(\\d+)?", header)
        if match:
            tipo = match.group(1)
            num = int(match.group(2)) if match.group(2) else 0
            return (weighs.get(tipo, 99), num, header)
        # Para horas extra
        if header.startswith("Días Horas Extra"):
            return (4, weighs_horas_extra["D"], header)
        if header.startswith("Horas Extra"):
            return (4, weighs_horas_extra["H"], header)
        if header.startswith("Importe Horas Extra"):
            return (4, weighs_horas_extra["I"], header)
        # Otros al final
        return (5, 0, header)

    return sorted(headers, key=header_key)
