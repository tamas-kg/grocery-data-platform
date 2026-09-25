from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.types import StructType

from grocery.config.models import SourceConfig


def read_source(
    spark: SparkSession,
    config: SourceConfig,
    schema: StructType,
) -> DataFrame:
    if config.source_type != "file":
        raise ValueError(
            f"Unsupported source type: {config.source_type}"
        )

    return (
        spark.read
        .format(config.source_format)
        .schema(schema)
        .load(config.path_or_table)
    )