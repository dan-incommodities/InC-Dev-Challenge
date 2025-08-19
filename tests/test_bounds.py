import numpy as np
from src.risk.manager import SimpleRiskManager


def test_bounds_and_daily_cap():
    risk = SimpleRiskManager(per_hour_bounds=(-10, 10), daily_abs_cap=50)
    targets = np.array([20] * 24)
    enforced = risk.enforce(targets)
    assert enforced.max() <= 10
    assert abs(enforced).sum() <= 50
