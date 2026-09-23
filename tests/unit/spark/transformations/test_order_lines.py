from decimal import Decimal

from pyspark.sql import SparkSession
from pyspark.sql.types import (
    DecimalType,
    IntegerType,
    StringType,
    StructField,
    StructType,
)
from pyspark.testing.utils import assertDataFrameEqual

from grocery.spark.transformations.order_lines import calculate_line_revenue


def test_calculate_line_revenue(spark: SparkSession) -> None:
    input_schema = StructType([
        StructField("order_line_id", StringType(), False),
        StructField("quantity", IntegerType(), False),
        StructField("unit_price", DecimalType(10, 2), False),
    ])

    input_df = spark.createDataFrame(
        [
            ("line-1", 2, Decimal("3.50")),
            ("line-2", 3, Decimal("4.25")),
        ],
        schema=input_schema,
    )

    expected_df = spark.createDataFrame(
        [
            ("line-1", 2, Decimal("3.50"), Decimal("7.00")),
            ("line-2", 3, Decimal("4.25"), Decimal("12.75")),
        ],
        schema="""
            order_line_id string,
            quantity int,
            unit_price decimal(10,2),
            line_revenue decimal(21,2)
        """,
    )

    actual_df = calculate_line_revenue(input_df)

    assertDataFrameEqual(actual_df, expected_df)