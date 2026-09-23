import pytest
from pydantic import ValidationError

from grocery.config.models import SourceConfig


def test_valid_source_config():
    config = SourceConfig(
        source_name="orders",
        source_type="file",
        source_format="parquet",
        path_or_table="data/source/orders_*.parquet",
        key_columns=["order_id"],
        schema_ref="schemas/orders.json",
        load_type="full",
    )

    assert config.source_name == "orders"
    assert config.key_columns == ["order_id"]
    assert config.load_type == "full"


def test_key_columns_cannot_be_empty():
    with pytest.raises(ValidationError):
        SourceConfig(
            source_name="orders",
            source_type="file",
            source_format="parquet",
            path_or_table="data/source/orders_*.parquet",
            key_columns=[],
            schema_ref="schemas/orders.json",
            load_type="full",
        )


def test_incremental_source_requires_watermark():
    with pytest.raises(ValidationError):
        SourceConfig(
            source_name="orders",
            source_type="file",
            source_format="parquet",
            path_or_table="data/source/orders_*.parquet",
            key_columns=["order_id"],
            schema_ref="schemas/orders.json",
            load_type="incremental",
        )


def test_incremental_source_accepts_watermark():
    config = SourceConfig(
        source_name="orders",
        source_type="file",
        source_format="parquet",
        path_or_table="data/source/orders_*.parquet",
        key_columns=["order_id"],
        schema_ref="schemas/orders.json",
        watermark_column="updated_at",
        load_type="incremental",
    )

    assert config.watermark_column == "updated_at"