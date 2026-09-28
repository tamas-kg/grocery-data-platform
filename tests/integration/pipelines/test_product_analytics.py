from decimal import Decimal

from pyspark.sql import SparkSession
from pyspark.testing.utils import assertDataFrameEqual

from grocery.pipelines.product_analytics import build_product_analytics


def test_build_product_analytics_calculates_margin_and_percentage(
    spark: SparkSession,
) -> None:
    products = spark.createDataFrame(
        [
            (
                "product-1",
                Decimal("2.00"),
                Decimal("4.00"),
            ),
            (
                "product-2",
                Decimal("3.00"),
                Decimal("4.00"),
            ),
        ],
        schema="""
            product_id string,
            unit_cost decimal(10,2),
            unit_price decimal(10,2)
        """,
    )

    result = build_product_analytics(products)

    expected = spark.createDataFrame(
        [
            (
                "product-1",
                Decimal("2.00"),
                Decimal("4.00"),
                Decimal("2.00"),
                0.5,
            ),
            (
                "product-2",
                Decimal("3.00"),
                Decimal("4.00"),
                Decimal("1.00"),
                0.25,
            ),
        ],
        schema="""
            product_id string,
            unit_cost decimal(10,2),
            unit_price decimal(10,2),
            unit_margin decimal(11,2),
            margin_percentage double
        """,
    )

    assertDataFrameEqual(
        result,
        expected,
        checkRowOrder=False,
    )