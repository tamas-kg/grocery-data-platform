from pyspark.sql import DataFrame
from pyspark.sql import functions as F

from grocery.spark.transformations.order_lines import calculate_line_revenue


def calculate_order_revenue(
    orders: DataFrame,
    order_lines: DataFrame,
) -> DataFrame:
    order_revenue = (
        calculate_line_revenue(order_lines)
        .groupBy("order_id")
        .agg(
            F.sum("line_revenue").alias("order_revenue"),
        )
    )

    return orders.join(
        order_revenue,
        on="order_id",
        how="left",
    )