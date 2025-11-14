# en utils/dates.py
import pandas as pd


def normalize_to_utc(series: pd.Series) -> pd.Series:
    series = pd.to_datetime(series, errors="coerce")
    try:
        return (
            series.dt.tz_localize("UTC")
            if series.dt.tz is None
            else series.dt.tz_convert("UTC")
        )
    except TypeError:
        return series.apply(
            lambda x: x.tz_localize("UTC")
            if pd.notna(x) and x.tzinfo is None
            else x.tz_convert("UTC")
            if pd.notna(x)
            else x
        )
