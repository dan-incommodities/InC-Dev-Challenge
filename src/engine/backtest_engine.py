from __future__ import annotations
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any
import numpy as np
import pandas as pd

from src.utils.config import Config, build_component
from src.utils.logging import setup_logging
from src.utils.calendar import entry_days


log = logging.getLogger(__name__)


@dataclass
class BacktestEngine:
    cfg: Config

    def run(self) -> None:
        artifacts = self.cfg.artifacts_dir
        setup_logging(artifacts)
        log.info("Artifacts dir: %s", artifacts)

        # Build components
        data_cfg = self.cfg.raw["data"]
        comp = self.cfg.raw["components"]
        ds = build_component(comp["datasource"], path=data_cfg["path"])  # type: ignore[arg-type]
        model = build_component(comp["model"])  # type: ignore[call-arg]
        policy = build_component(comp["policy"])  # type: ignore[call-arg]
        risk = build_component(comp["risk"], **self.cfg.raw.get("risk", {}))  # type: ignore[arg-type]
        broker = build_component(comp["broker"], **self.cfg.raw.get("costs", {}))  # type: ignore[arg-type]
        reporter = build_component(comp["reporter"], artifacts_dir=artifacts)  # type: ignore[call-arg]

        # Load data up to end_now for *features* availability
        engine_cfg = self.cfg.raw.get("engine", {})
        end_now = pd.to_datetime(engine_cfg.get("end_now")) if engine_cfg.get("end_now") else None
        full = ds.load(end_now=end_now)

        start = pd.to_datetime(engine_cfg.get("start")) if engine_cfg.get("start") else full.index.get_level_values(0).min()
        end = pd.to_datetime(engine_cfg.get("end")) if engine_cfg.get("end") else full.index.get_level_values(0).max()

        days = [d for d in entry_days(full) if (d >= start and d <= end)]
        log.info("Running backtest from %s to %s (%d days)", start.date(), end.date(), len(days))

        daily_pnl = {}
        for i, day in enumerate(days):
            # Fit on strictly prior days
            past = full.loc[pd.IndexSlice[: day - pd.Timedelta("1ns"), :]]
            today = full.loc[(day, slice(None))]
            log.debug("Day %s: fit on %d rows, predict on 24", day, len(past))

            model.fit(past)
            preds = model.predict(today)

            # Policy -> targets -> risk
            lo, hi = tuple(self.cfg.raw.get("risk", {}).get("per_hour_bounds", [-10, 10]))
            targets = policy.target_positions(preds, (lo, hi))
            targets = risk.enforce(targets)

            # Broker settle and collect P&L
            res = broker.settle(today, targets)
            daily_pnl[day] = res["daily_pnl"]

        pnl_series = pd.Series(daily_pnl).sort_index()
        reporter.save(pnl_series)
        log.info("Done. Metrics and plot saved to %s", artifacts)
