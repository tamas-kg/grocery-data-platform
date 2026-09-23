from pathlib import Path

import yaml

from grocery.config.models import SourceConfig


def load_sources(path: Path) -> list[SourceConfig]:
    with path.open() as file:
        config = yaml.safe_load(file)

    return [
        SourceConfig.model_validate(source)
        for source in config["sources"]
    ]