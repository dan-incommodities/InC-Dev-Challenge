from __future__ import annotations
import numpy as np
from typing import Tuple


class SignPolicy:
    """Take the sign of predicted premium, at max absolute size."""

    def __init__(self, size: int = 10):
        self.size = size

    def target_positions(self, preds: np.ndarray, bounds: Tuple[int, int]) -> np.ndarray:
        lo, hi = bounds
        pos = np.sign(preds) * min(self.size, hi)
        # ensure within [lo, hi]
        pos = np.clip(pos, lo, hi)
        return pos.astype(int)
