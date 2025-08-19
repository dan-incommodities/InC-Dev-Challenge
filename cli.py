from __future__ import annotations
import argparse
from src.utils.config import load_config, build_component
from src.engine.backtest_engine import BacktestEngine


def main():
    parser = argparse.ArgumentParser(description="DAH Backtest CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    run = sub.add_parser("backtest", help="Run a backtest")
    run.add_argument("--config", required=True, help="Path to YAML config")

    args = parser.parse_args()

    if args.cmd == "backtest":
        cfg = load_config(args.config)
        engine = BacktestEngine(cfg)
        engine.run()


if __name__ == "__main__":
    main()
