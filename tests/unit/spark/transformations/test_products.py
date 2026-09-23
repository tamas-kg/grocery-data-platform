from decimal import Decimal

from pyspark.sql import SparkSession
from pyspark.testing.utils import assertDataFrameEqual

from grocery.spark.transformations.products import (
    calculate_product_margin, calculate_product_margin_percentage)


def test_calculate_product_margin(spark: SparkSession) -> None:
    input_df = spark.createDataFrame(
        [
            ("product-1", Decimal("2.50"), Decimal("4.00")),
            ("product-2", Decimal("5.25"), Decimal("8.75")),
        ],
        schema="""
            product_id string,
            unit_cost decimal(10,2),
            unit_price decimal(10,2)
        """,
    )

    expected_df = spark.createDataFrame(
        [
            (
                "product-1",
                Decimal("2.50"),
                Decimal("4.00"),
                Decimal("1.50"),
            ),
            (
                "product-2",
                Decimal("5.25"),
                Decimal("8.75"),
                Decimal("3.50"),
            ),
        ],
        schema="""
            product_id string,
            unit_cost decimal(10,2),
            unit_price decimal(10,2),
            unit_margin decimal(11,2)
        """,
    )

    actual_df = calculate_product_margin(input_df)

    assertDataFrameEqual(actual_df, expected_df)


def test_calculate_product_margin_percentage(
    spark: SparkSession,
) -> None:
    input_df = spark.createDataFrame(
        [
            ("product-1", Decimal("2.00"), Decimal("4.00")),
            ("product-2", Decimal("6.00"), Decimal("8.00")),
        ],
        schema="""
            product_id string,
            unit_cost decimal(10,2),
            unit_price decimal(10,2)
        """,
    )

    expected_df = spark.createDataFrame(
        [
            ("product-1", Decimal("2.00"), Decimal("4.00"), 0.5),
            ("product-2", Decimal("6.00"), Decimal("8.00"), 0.25),
        ],
        schema="""
            product_id string,
            unit_cost decimal(10,2),
            unit_price decimal(10,2),
            margin_percentage double
        """,
    )

    actual_df = calculate_product_margin_percentage(input_df)

    assertDataFrameEqual(actual_df, expected_df)