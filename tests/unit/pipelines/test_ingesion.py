from pathlib import Path
from unittest.mock import patch

from pyspark.sql import SparkSession

from grocery.config.models import SourceConfig
from grocery.pipelines.ingestion import ingest_and_validate_sources, validate_source


def test_validate_source_returns_no_failures(
    spark: SparkSession,
) -> None:
    df = spark.createDataFrame(
        [
            ("order-1",),
            ("order-2",),
        ],
        schema="order_id string",
    )

    config = SourceConfig(
        source_name="orders",
        source_type="file",
        source_format="parquet",
        path_or_table="unused",
        key_columns=["order_id"],
        schema_ref="schemas/orders.json",
        load_type="full",
    )

    failures = validate_source(
        df=df,
        config=config,
    )

    assert failures == []


def test_validate_source_returns_key_failures(
    spark: SparkSession,
) -> None:
    df = spark.createDataFrame(
        [
            ("order-1",),
            ("order-1",),
            (None,),
        ],
        schema="order_id string",
    )

    config = SourceConfig(
        source_name="orders",
        source_type="file",
        source_format="parquet",
        path_or_table="unused",
        key_columns=["order_id"],
        schema_ref="schemas/orders.json",
        load_type="full",
    )

    failures = validate_source(
        df=df,
        config=config,
    )

    failures_by_name = {
        failure.check_name: failure.violation_count for failure in failures
    }

    assert failures_by_name == {
        "null_keys": 1,
        "duplicate_keys": 1,
    }


def test_ingest_and_validate_sources_returns_dataframes_by_source_name(
    spark: SparkSession,
    tmp_path: Path,
) -> None:
    orders_config = SourceConfig(
        source_name="orders",
        source_type="file",
        source_format="parquet",
        path_or_table="orders.parquet",
        key_columns=["order_id"],
        schema_ref="schemas/orders.json",
        load_type="full",
    )

    products_config = SourceConfig(
        source_name="products",
        source_type="file",
        source_format="parquet",
        path_or_table="products.parquet",
        key_columns=["product_id"],
        schema_ref="schemas/products.json",
        load_type="full",
    )

    orders_df = spark.createDataFrame(
        [("order-1",)],
        schema="order_id string",
    )

    products_df = spark.createDataFrame(
        [("product-1",)],
        schema="product_id string",
    )

    with patch(
        "grocery.pipelines.ingestion.ingest_and_validate_source",
        side_effect=[orders_df, products_df],
    ):
        result = ingest_and_validate_sources(
            spark=spark,
            configs=[
                orders_config,
                products_config,
            ],
            config_dir=tmp_path,
        )

    assert set(result) == {
        "orders",
        "products",
    }

    assert result["orders"] is orders_df
    assert result["products"] is products_df
