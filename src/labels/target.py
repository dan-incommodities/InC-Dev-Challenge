from __future__ import annotations
import pandas as pd


def premium(df_day: pd.DataFrame) -> pd.Series:
    """Return realized premium for the day (length 24)."""
    return df_day["premium"].astype(float)
