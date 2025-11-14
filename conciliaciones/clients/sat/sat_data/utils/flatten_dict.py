def flatten_dict(nested_dict, parent_key="", separator="_"):
    """Función para aplanar diccionarios

    Args:
        nested_dict (_dict_): Diccionario anidado que se va a procesar (aplanar)
        parent_key (str, optional): Clave padre
        separator (str, optional): Separador "_"

    Returns:
        _dict_: Diccionario ya aplanado

    Ejemplo de uso:
    "data": [
        {
            "Comprobante": {
                "descuento": 0,
                "folio": "string",
            },
            "R01": {
                "sumaDeTotal": 0
            },
            "R02": {
                "sumaDeTotal": 1
            }
        }
    ],

    Output:
    {
        "Comprobante_descuento": 0,
        "Comprobante_folio": "string",
        "R01_sumaDeTotal": 0,
        "R02_sumaDeTotal": 1
    }

    """
    flat_dict = {}

    for key, value in nested_dict.items():
        new_key = f"{parent_key}{separator}{key}" if parent_key else key

        if isinstance(value, dict):
            flat_dict.update(flatten_dict(value, new_key, separator=separator))
        else:
            flat_dict[new_key] = value

    return flat_dict
