# InC-Dev-Challenge
Framework-first quant dev challenge: build a pluggable day-ahead power backtester with CLI, tests, and OOS report. Fork to start and open a PR.
# Quant DAH Framework Challenge

**Build a small, extensible backtesting framework** for day-ahead hourly (DAH) power contracts. We use this as our *quant developer* hiring exercise to assess framework thinking, software quality, and operability—not just modeling chops.

> 📣 **How to participate:** **Fork this repo**, complete the tasks below, and submit a PR titled `Submission: <Your Name>`.

---

## Why this challenge?
We’re hiring a quant developer who can design and ship robust framework tooling:
- Clean abstractions (data → model → policy → risk → broker → metrics)
- Correctness (no leakage, constraints, accounting)
- Engineering quality (tests, CLI, reproducibility, CI)

The starter gives you a working skeleton and baseline strategy so you can focus on architecture and polish.

---

## Quickstart
```bash
git fork <this repo> && git clone <your fork>
cd <repo>
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e .
# Place or point to the dataset:
# by default we look for ./data_dah.csv (or set path in configs/baseline.yaml)
python cli.py backtest --config configs/baseline.yaml
