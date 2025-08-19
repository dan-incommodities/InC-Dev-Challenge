from __future__ import annotations
import pandas as pd
from pathlib import Path

REQUIRED = {
    "entry_time", "exit_time", "entry_price", "exit_price"
}


class CSVDayaheadDataSource:
    def __init__(self, path: str | Path):
        self.path = Path(path)

    def load(self, *, end_now: pd.Timestamp | None = None) -> pd.DataFrame:
        df = pd.read_csv(self.path, parse_dates=["entry_time", "exit_time"]).copy()
        missing = REQUIRED - set(df.columns)
        if missing:
            raise ValueError(f"Missing required columns: {missing}")
        df["hour"] = df["exit_time"].dt.hour
        df["premium"] = df["exit_price"] - df["entry_price"]
        df = df.set_index(["entry_time", "hour"]).sort_index()
        if end_now is not None:
            df = df.loc[pd.IndexSlice[:end_now, :]]
        return df
