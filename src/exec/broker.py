from __future__ import annotations
import numpy as np
import pandas as pd


class SimpleBroker:
    def __init__(self, fee_per_mwh: float = 0.0, bps_per_trade: float = 0.0):
        self.fee = fee_per_mwh
        self.bps = bps_per_trade / 1e4  # convert bps to fraction

    def settle(self, df_day: pd.DataFrame, targets: np.ndarray) -> dict:
        entry = df_day["entry_price"].to_numpy(float)
        exit_ = df_day["exit_price"].to_numpy(float)
        prem = exit_ - entry
        notional = np.abs(targets) * entry
        # round-trip costs: open + close
        costs = 2 * (np.abs(targets) * self.fee + notional * self.bps)
        pnl = targets * prem - costs
        return {
            "hourly_pnl": pnl,
            "hourly_premium": prem,
            "hourly_entry": entry,
            "hourly_exit": exit_,
            "hourly_costs": costs,
            "daily_pnl": float(pnl.sum()),
        }
