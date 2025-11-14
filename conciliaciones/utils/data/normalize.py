import pandas as pd
from k_link.utils.files.abc_datasource import DataFrame
from k_link.utils.pydantic_types import Date
from pandas import Series, json_normalize


def concatenate_data(ds_base: DataFrame, df_temp: DataFrame) -> pd.DataFrame:
    return pd.concat([df_temp, ds_base], ignore_index=True)


def normalize_df(df: pd.DataFrame) -> pd.DataFrame:
    normalized_dfs = []

    for i, column in enumerate(df.columns):
        # Asignar nombre válido a la columna
        col_name = column if column and not pd.isna(column) else f"unnamed_{i}"
        col_data: Series = df[column]
        col_values = col_data.dropna()

        if not col_values.empty and isinstance(col_values.iloc[0], dict):
            # Si hay diccionarios, normalizar
            final_df = json_normalize(col_data)  # type: ignore
            final_df.columns = [f"{subcol}" for subcol in final_df.columns]
        else:
            # Para columnas vacías o no diccionarios, mantener la original con nombre válido
            final_df = col_data.to_frame(name=col_name)

        normalized_dfs.append(final_df)

    # Combina todas las columnas normalizadas en un único DataFrame
    result_df = pd.concat(normalized_dfs, axis=1)
    return result_df


def normalize_date(year: int | str | None, month: int | str | None) -> Date:
    """ "
    Normaliza una fecha basada en año y mes dados.

    Args:
        year (Optional[int | str]): Año como entero o cadena.
        month (Optional[int | str]): Mes como entero o cadena.

    Returns:
        Date: Fecha normalizada.
    """
    today = Date()

    if isinstance(year, str):
        year = int(year)
    if isinstance(month, str):
        month = int(month)

    if year and month:
        today = today.replace(year=year, month=month, day=1)
    else:
        if year is not None:
            today = today.replace(year=year)
        if month is not None:
            today = today.replace(month=month)

    return today


def validate_date(year: int | None, month: int | None) -> Date:
    validated_date = Date()
    if year is not None and month is not None:
        validated_date = normalize_date(year, month)
    if year is not None:
        validated_date.replace(year=year)
    if month is not None:
        validated_date.replace(month=month)

    return validated_date
