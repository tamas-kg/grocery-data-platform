from pyspark.sql import SparkSession

from grocery.config.models import SourceConfig
from grocery.pipelines.ingestion import validate_source


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
        failure.check_name: failure.violation_count
        for failure in failures
    }

    assert failures_by_name == {
        "null_keys": 1,
        "duplicate_keys": 1,
    }