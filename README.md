# quant-dah-starter-repo

Framework-first skeleton for day-ahead hourly power contracts. Pairs with `INSTRUCTIONS.md` for candidates.

## Quickstart
```bash
python -m venv .venv && source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -e .
python cli.py backtest --config configs/baseline.yaml
```

## Repo layout
- `src/` – engine and swappable components
- `configs/` – example config using the baseline model and policy
- `tests/` – acceptance tests (leakage, bounds, PnL bookkeeping)
- `cli.py` – simple CLI for backtest runs

## Data
Place the provided `data_dah.csv` in the repo root (same folder as `cli.py`), or set an absolute path in your config.

## Artifacts
Runs write to `artifacts/<run_id>` with metrics JSON, plots, and logs.
