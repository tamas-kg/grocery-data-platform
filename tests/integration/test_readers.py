from decimal import Decimal
from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql.types import (
    DecimalType,
    LongType,
    StringType,
    StructField,
    StructType,
)
from pyspark.testing.utils import assertDataFrameEqual

from grocery.config.models import SourceConfig
from grocery.spark.readers import read_source


def test_read_parquet_source_with_explicit_schema(
    spark: SparkSession,
    tmp_path: Path,
) -> None:
    source_path = tmp_path / "order_lines"

    input_df = spark.createDataFrame(
        [
            ("line-1", "order-1", 2, Decimal("3.50")),
            ("line-2", "order-1", 1, Decimal("5.00")),
        ],
        schema="""
            order_line_id string,
            order_id string,
            quantity long,
            unit_price decimal(10,2)
        """,
    )

    input_df.write.parquet(str(source_path))

    schema = StructType(
        [
            StructField("order_line_id", StringType(), True),
            StructField("order_id", StringType(), True),
            StructField("quantity", LongType(), True),
            StructField("unit_price", DecimalType(10, 2), True),
        ]
    )

    config = SourceConfig(
        source_name="order_lines",
        source_type="file",
        source_format="parquet",
        path_or_table=str(source_path),
        key_columns=["order_line_id"],
        schema_ref="schemas/order_lines.json",
        load_type="full",
    )

    actual_df = read_source(
        spark=spark,
        config=config,
        schema=schema,
    )

    assertDataFrameEqual(actual_df, input_df)