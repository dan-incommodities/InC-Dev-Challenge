from __future__ import annotations
import pandas as pd


def entry_days(df: pd.DataFrame) -> pd.DatetimeIndex:
    # Requires a MultiIndex with level 0 = entry_time
    return df.index.get_level_values("entry_time").unique().sort_values()
