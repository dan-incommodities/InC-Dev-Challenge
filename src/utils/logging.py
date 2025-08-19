from __future__ import annotations
import logging
from pathlib import Path


def setup_logging(artifacts_dir: Path) -> None:
    log_file = artifacts_dir / "run.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file, mode="w"),
            logging.StreamHandler(),
        ],
    )
