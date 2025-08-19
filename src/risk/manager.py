from __future__ import annotations
import numpy as np
from typing import Tuple


class SimpleRiskManager:
    def __init__(self, per_hour_bounds: Tuple[int, int] = (-10, 10), daily_abs_cap: int | None = 120):
        self.bounds = per_hour_bounds
        self.daily_abs_cap = daily_abs_cap

    def enforce(self, targets: np.ndarray) -> np.ndarray:
        lo, hi = self.bounds
        t = targets.astype(int)
        t = np.clip(t, lo, hi)
        if self.daily_abs_cap is not None:
            scale = min(1.0, self.daily_abs_cap / max(1, int(np.sum(np.abs(t)))))
            if scale < 1.0:
                t = (t * scale).astype(int)
        return t
