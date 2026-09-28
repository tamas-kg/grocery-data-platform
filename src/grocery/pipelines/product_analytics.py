from pyspark.sql import DataFrame

from grocery.spark.transformations.products import (
    calculate_product_margin,
    calculate_product_margin_percentage,
)


def build_product_analytics(
    products: DataFrame,
) -> DataFrame:
    return calculate_product_margin_percentage(
        calculate_product_margin(products)
    )