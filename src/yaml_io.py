from pathlib import Path
from typing import Any

import yaml


def read_yaml(path: Path) -> Any:
    data = yaml.safe_load(path.read_text())
    if data is None:
        raise ValueError(f"YAML file is empty: {path}")
    return data
