from __future__ import annotations
import importlib
import yaml
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict


@dataclass
class Config:
    raw: Dict[str, Any]

    @property
    def artifacts_dir(self) -> Path:
        run = self.raw.get("run", {})
        root = Path(run.get("artifacts_dir", "artifacts"))
        rid = run.get("run_id", "run")
        p = root / rid
        p.mkdir(parents=True, exist_ok=True)
        return p


def load_config(path: str | Path) -> Config:
    with open(path, "r") as f:
        raw = yaml.safe_load(f)
    return Config(raw)


def build_component(target: str, **kwargs):
    """Instantiate a component from a string like 'pkg.mod:ClassName'."""
    module_path, class_name = target.split(":")
    mod = importlib.import_module(module_path)
    cls = getattr(mod, class_name)
    return cls(**kwargs)
