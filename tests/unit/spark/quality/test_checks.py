from pyspark.sql import SparkSession
from pyspark.testing.utils import assertDataFrameEqual

from grocery.spark.quality.checks import find_duplicate_keys, find_null_keys


def test_find_null_keys(spark: SparkSession) -> None:
    df = spark.createDataFrame(
        [
            ("order-1", "customer-1"),
            (None, "customer-2"),
            ("order-3", "customer-3"),
        ],
        schema="""
            order_id string,
            customer_id string
        """,
    )

    actual_df = find_null_keys(
        df,
        key_columns=["order_id"],
    )

    expected_df = spark.createDataFrame(
        [
            (None, "customer-2"),
        ],
        schema=df.schema,
    )

    assertDataFrameEqual(actual_df, expected_df)


def test_find_duplicate_keys(spark: SparkSession) -> None:
    df = spark.createDataFrame(
        [
            ("order-1",),
            ("order-1",),
            ("order-2",),
            ("order-3",),
            ("order-3",),
            ("order-3",),
        ],
        schema="order_id string",
    )

    actual_df = find_duplicate_keys(
        df,
        key_columns=["order_id"],
    )

    expected_df = spark.createDataFrame(
        [
            ("order-1", 2),
            ("order-3", 3),
        ],
        schema="""
            order_id string,
            count long
        """,
    )

    assertDataFrameEqual(actual_df, expected_df)
