from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def calculate_product_margin(df: DataFrame) -> DataFrame:
    return df.withColumn(
        "unit_margin",
        F.col("unit_price") - F.col("unit_cost"),
    )


def calculate_product_margin_percentage(df: DataFrame) -> DataFrame:
    return df.withColumn(
        "margin_percentage",
        F.when(
            F.col("unit_price") != 0,
            (F.col("unit_price") - F.col("unit_cost"))
            / F.col("unit_price"),
        ).otherwise(F.lit(0.0)),
    )