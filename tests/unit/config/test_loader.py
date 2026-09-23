from pathlib import Path
import pytest
from pydantic import ValidationError
from grocery.config.loader import load_sources


def test_load_sources(tmp_path: Path):
    config_path = tmp_path / "sources.yaml"

    config_path.write_text(
        """
        sources:
          - source_name: test_source
            source_type: file
            source_format: parquet
            path_or_table: data/test.parquet
            key_columns:
              - id
            schema_ref: schemas/test.json
            load_type: full
        """
    )

    sources = load_sources(config_path)

    assert len(sources) == 1

    source = sources[0]

    assert source.source_name == "test_source"
    assert source.source_type == "file"
    assert source.source_format == "parquet"
    assert source.path_or_table == "data/test.parquet"
    assert source.key_columns == ["id"]
    assert source.schema_ref == "schemas/test.json"
    assert source.load_type == "full"

def test_load_sources_rejects_invalid_source(tmp_path):
    config_path = tmp_path / "sources.yaml"

    config_path.write_text(
        """
        sources:
          - source_name: test_source
            source_type: invalid
            source_format: parquet
            path_or_table: data/test.parquet
            key_columns:
              - id
            schema_ref: schemas/test.json
            load_type: full
        """
    )

    with pytest.raises(ValidationError):
        load_sources(config_path)