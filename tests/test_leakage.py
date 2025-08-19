import pandas as pd
import numpy as np
from src.data.datasource import CSVDayaheadDataSource
from src.engine.backtest_engine import BacktestEngine
from src.utils.config import Config


class GuardModel:
    def __init__(self):
        self.max_fit_day = None
        self.fit_called_for = []

    def fit(self, df_past: pd.DataFrame):
        if len(df_past):
            days = df_past.index.get_level_values("entry_time").unique().sort_values()
            self.max_fit_day = days[-1]
        return self

    def predict(self, df_today: pd.DataFrame):
        day = df_today.index.get_level_values("entry_time").unique().item()
        # Asserts: engine must not pass future data to fit
        if self.max_fit_day is not None:
            assert self.max_fit_day < day, "Leakage: fit() saw >= today"
        return np.zeros(24)


def tiny_config(tmp_path, data_path):
    raw = {
        "run": {"run_id": "test", "artifacts_dir": str(tmp_path / "artifacts")},
        "data": {"path": str(data_path)},
        "engine": {},
        "risk": {"per_hour_bounds": [-10, 10]},
        "costs": {"fee_per_mwh": 0.0, "bps_per_trade": 0.0},
        "components": {
            "datasource": "src.data.datasource:CSVDayaheadDataSource",
            "model": "tests.test_leakage:GuardModel",
            "policy": "src.strategy.baseline:SignPolicy",
            "risk": "src.risk.manager:SimpleRiskManager",
            "broker": "src.exec.broker:SimpleBroker",
            "reporter": "src.metrics.reporter:Reporter",
        },
    }
    return Config(raw)


def test_no_leakage(tmp_path):
    # Use a tiny synthetic dataset if real CSV unavailable
    try:
        data_path = "data_dah.csv"
        _ = CSVDayaheadDataSource(data_path).load()
    except Exception:
        # Build 3 days synthetic
        rows = []
        for d in pd.date_range("2059-01-01", periods=3, tz="Europe/Berlin"):
            entry = pd.Timestamp(d.date()) + pd.Timedelta(hours=11, minutes=50)
            for h in range(24):
                rows.append({
                    "entry_time": entry,
                    "exit_time": (entry + pd.Timedelta(days=1)).tz_localize(None).tz_localize("Europe/Berlin").replace(hour=h),
                    "entry_price": 50.0,
                    "exit_price": 55.0,
                })
        import pandas as pd
        df = pd.DataFrame(rows)
        p = tmp_path / "tiny.csv"
        df.to_csv(p, index=False)
        data_path = str(p)

    cfg = tiny_config(tmp_path, data_path)
    engine = BacktestEngine(cfg)
    engine.run()
