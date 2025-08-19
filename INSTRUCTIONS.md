# Candidate Instructions — Day-Ahead Hourly (DAH) Trading Framework

**Objective:** Build an extensible research & backtesting framework for DAH power contracts, demonstrating architecture, correctness, testing, and operability — not just a single predictive model.

You will:
1. Implement/extend the swappable components described below.
2. Run a chronological walk-forward backtest.
3. Produce an out-of-sample performance report.
4. Demonstrate no data leakage and enforce position constraints.

We’ve provided:
- A minimal skeleton (engine, interfaces, baseline model & policy, broker, reporter, CLI).
- An example config in `configs/baseline.yaml`.
- Acceptance tests in `tests/`.
- A baseline “yesterday’s premium” model.

---

## Contracts & Setup (recap)
- At **entry_time ~ 11:50** each day, you can take positions for the 24 delivery hours of the next day.
- Positions are **forced closed at delivery** (i.e., at each `exit_time`).
- **Per-hour bounds:** default `[-10, +10]` units. You may make this configurable.
- Your P&L per hour is `position * (exit_price - entry_price) - costs`.

## Data
- File: `data_dah.csv` (provided separately).
- Key columns: `entry_time`, `exit_time`, `entry_price`, `exit_price`, and feature columns such as `wind_forecast_provider*`, `solar_forecast_provider*`, `load_forecast_provider*`.
- Treat all rows with the same `entry_time` as one DAH decision set for the next day.

---

## Component contracts (interfaces)
You can alter/extend the APIs, but **keep the separation of concerns**.

- **DataSource**
  - Loads and returns a DataFrame indexed by `(entry_time, hour)` with required columns.
  - Ensures filtering by `end_now` and provides features known at `entry_time`.

- **SignalModel**
  - `fit(df_past) -> self` uses only data with `entry_time < t` for day `t`.
  - `predict(df_today) -> np.ndarray[24]` outputs expected premiums per hour.

- **StrategyPolicy**
  - `target_positions(preds, bounds) -> np.ndarray[24]` maps predictions to bounded positions.

- **RiskManager**
  - Enforces bounds and optional daily exposure caps; logs any clipping.

- **Broker**
  - Computes fills at `entry_price` and closes at `exit_price`; applies fees/slippage.

- **BacktestEngine**
  - Walks days chronologically, performs `fit/predict/policy/risk/broker`, aggregates metrics.

- **Reporter**
  - Writes a metrics JSON and a cumulative P&L plot, plus a Markdown/HTML summary.

---

## What to deliver
- Clean, typed code with a small README describing your design choices.
- Pass the provided tests; add your own where useful.
- Produce a cumulative OOS P&L plot and a short write-up on in-sample vs OOS behavior.
- Keep runs reproducible: seed(s), config snapshot, logs, and artifacts per run.

Timebox yourself (we expect architecture-first code, not perfect models).

**Stretch (pick any 1–2):** feature pipeline DAG, portfolio of two strategies, paper-trading mode, or resume-from-checkpoint.

---

## Scoring rubric (100 pts)
- Architecture & Extensibility (25)
- Correctness (20)
- Testing & CI (15)
- Performance & Hygiene (15)
- Operability (10)
- Communication (15)

Good luck — we’re looking for framework thinking.
