from __future__ import annotations
from typing import Protocol
import numpy as np
import pandas as pd


class SignalModel(Protocol):
    def fit(self, df_past: pd.DataFrame) -> "SignalModel":
        ...

    def predict(self, df_today: pd.DataFrame) -> np.ndarray:  # shape (24,)
        ...
