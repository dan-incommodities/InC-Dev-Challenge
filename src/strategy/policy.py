from __future__ import annotations
from typing import Protocol, Tuple
import numpy as np


class StrategyPolicy(Protocol):
    def target_positions(self, preds: np.ndarray, bounds: Tuple[int, int]) -> np.ndarray:
        ...
