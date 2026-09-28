from decimal import Decimal

from pyspark.sql import SparkSession
from pyspark.testing.utils import assertDataFrameEqual

from grocery.pipelines.order_analytics import build_order_analytics


def test_build_order_analytics_calculates_order_revenue(
    spark: SparkSession,
) -> None:
    orders = spark.createDataFrame(
        [
            ("order-1", "customer-1"),
            ("order-2", "customer-2"),
            ("order-3", "customer-3"),
        ],
        schema="""
            order_id string,
            customer_id string
        """,
    )

    order_lines = spark.createDataFrame(
        [
            (
                "line-1",
                "order-1",
                "product-1",
                2,
                Decimal("3.00"),
            ),
            (
                "line-2",
                "order-1",
                "product-2",
                1,
                Decimal("5.00"),
            ),
            (
                "line-3",
                "order-2",
                "product-3",
                4,
                Decimal("2.00"),
            ),
        ],
        schema="""
            order_line_id string,
            order_id string,
            product_id string,
            quantity long,
            unit_price decimal(10,2)
        """,
    )

    result = build_order_analytics(
        orders=orders,
        order_lines=order_lines,
    )

    expected = spark.createDataFrame(
        [
            (
                "order-1",
                "customer-1",
                Decimal("11.00"),
            ),
            (
                "order-2",
                "customer-2",
                Decimal("8.00"),
            ),
            (
                "order-3",
                "customer-3",
                None,
            ),
        ],
        schema="""
            order_id string,
            customer_id string,
            order_revenue decimal(38,2)
        """,
    )

    assertDataFrameEqual(
        result,
        expected,
        checkRowOrder=False,
    )