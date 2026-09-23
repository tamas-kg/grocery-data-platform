from decimal import Decimal

from pyspark.sql import SparkSession
from pyspark.testing.utils import assertDataFrameEqual

from grocery.spark.transformations.orders import calculate_order_revenue


def test_calculate_order_revenue(spark: SparkSession) -> None:
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
            ("line-1", "order-1", 2, Decimal("3.50")),
            ("line-2", "order-1", 1, Decimal("5.00")),
            ("line-3", "order-2", 3, Decimal("2.00")),
        ],
        schema="""
            order_line_id string,
            order_id string,
            quantity int,
            unit_price decimal(10,2)
        """,
    )

    actual_df = calculate_order_revenue(
        orders,
        order_lines,
    )

    expected_df = spark.createDataFrame(
    [
        ("order-1", "customer-1", Decimal("12.00")),
        ("order-2", "customer-2", Decimal("6.00")),
        ("order-3", "customer-3", None),
    ],
    schema="""
        order_id string,
        customer_id string,
        order_revenue decimal(31,2)
    """,
    )

    assertDataFrameEqual(actual_df, expected_df)