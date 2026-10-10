from decimal import Decimal

from databricks.connect import DatabricksSession

from grocery.spark.transformations.orders import (
    calculate_order_revenue,
)


def main() -> None:
    spark = (
        DatabricksSession.builder
        .profile("dev")
        .serverless()
        .getOrCreate()
    )

    orders = spark.createDataFrame(
        [
            ("order-1", "customer-1"),
            ("order-2", "customer-2"),
        ],
        schema="""
            order_id string,
            customer_id string
        """,
    )

    order_lines = spark.createDataFrame(
        [
            ("line-1", "order-1", 2, Decimal("4.00")),
            ("line-2", "order-1", 1, Decimal("3.00")),
        ],
        schema="""
            order_line_id string,
            order_id string,
            quantity long,
            unit_price decimal(10,2)
        """,
    )

    result = calculate_order_revenue(
        orders=orders,
        order_lines=order_lines,
    )

    result.show()


if __name__ == "__main__":
    main()