from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def calculate_line_revenue(df: DataFrame) -> DataFrame:
    return df.withColumn(
        "line_revenue",
        F.col("quantity") * F.col("unit_price"),
    )