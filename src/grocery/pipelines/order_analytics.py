from pyspark.sql import DataFrame

from grocery.spark.transformations.orders import (
    calculate_order_revenue,
)


def build_order_analytics(
    orders: DataFrame,
    order_lines: DataFrame,
) -> DataFrame:
    return calculate_order_revenue(
        orders=orders,
        order_lines=order_lines,
    )