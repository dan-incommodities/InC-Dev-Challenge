import numpy as np
import pandas as pd
from src.exec.broker import SimpleBroker


def test_simple_pnl_no_costs():
    broker = SimpleBroker(fee_per_mwh=0.0, bps_per_trade=0.0)
    entry = np.array([50.0] * 24)
    exit_ = np.array([55.0] * 24)
    df = pd.DataFrame({"entry_price": entry, "exit_price": exit_})
    res = broker.settle(df, np.ones(24) * 10)
    assert abs(res["daily_pnl"] - (10 * (55 - 50) * 24)) < 1e-6


def test_costs_applied():
    broker = SimpleBroker(fee_per_mwh=0.1, bps_per_trade=10)  # 10 bps each leg
    entry = np.array([100.0] * 24)
    exit_ = np.array([100.0] * 24)
    df = pd.DataFrame({"entry_price": entry, "exit_price": exit_})
    res = broker.settle(df, np.ones(24) * 10)
    # round-trip cost = 2 * (abs(q)*fee + abs(q)*entry*bps)
    expected = -2 * (10 * 0.1 + 10 * 100 * 0.001) * 24
    assert abs(res["daily_pnl"] - expected) < 1e-6
