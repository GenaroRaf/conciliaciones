from copy import deepcopy

from conciliaciones.clients.sat.sat_data.models.impuesto import TipoImpuesto


def get_impuesto_header(impuesto: dict, es_impuesto: bool, es_mxn: bool) -> str:
    clave = "Impuesto " if es_impuesto else "Base "
    if es_mxn:
        clave += "MXN "

    tipo_impuesto = impuesto.get("tipoImpuesto", "")
    impuesto_val = impuesto.get("impuesto", "")
    tipo_factor = impuesto.get("tipoFactor", "")
    tasa = impuesto.get("tasaOCuota")

    if impuesto_val == TipoImpuesto.ISR.value:
        nombre_impuesto = "ISR"
    elif impuesto_val == TipoImpuesto.IVA.value:
        nombre_impuesto = "IVA"
    else:
        nombre_impuesto = "IEPS"

    clave += f"{tipo_impuesto} {nombre_impuesto} {tipo_factor}"
    if tasa is not None:
        clave += f" {round(tasa * 100, 2)} %"

    return clave.strip()


def procesar_impuestos(dict_response: dict, tipo_cambio: float = 1.0) -> list[dict]:
    nuevos_dicts = []
    vistos = set()

    impuestos = dict_response.get("impuestos", [])

    if not isinstance(impuestos, list) or len(impuestos) == 0:
        return [dict_response]

    for impuesto in impuestos:
        clave = get_impuesto_header(impuesto, es_impuesto=True, es_mxn=False)
        if clave in vistos:
            continue

        vistos.add(clave)

        nuevo_dict = deepcopy(dict_response)
        nuevo_dict[get_impuesto_header(impuesto, False, False)] = impuesto.get("base")
        nuevo_dict[get_impuesto_header(impuesto, False, True)] = (
            impuesto.get("base", 0) * tipo_cambio
        )
        nuevo_dict[get_impuesto_header(impuesto, True, False)] = impuesto.get("importe")
        if impuesto.get("importe") is not None:
            nuevo_dict[get_impuesto_header(impuesto, True, True)] = (
                impuesto["importe"] * tipo_cambio
            )

        nuevos_dicts.append(nuevo_dict)

    return nuevos_dicts
