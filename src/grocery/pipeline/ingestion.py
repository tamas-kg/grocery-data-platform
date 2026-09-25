from pathlib import Path

from pyspark.sql import DataFrame, SparkSession

from grocery.config.models import SourceConfig
from grocery.config.schema_loader import load_spark_schema
from grocery.spark.readers import read_source


def ingest_source(
    spark: SparkSession,
    config: SourceConfig,
    config_dir: Path,
) -> DataFrame:
    schema_path = config_dir / config.schema_ref
    schema = load_spark_schema(schema_path)

    return read_source(
        spark=spark,
        config=config,
        schema=schema,
    )

def ingest_sources(
    spark: SparkSession,
    configs: list[SourceConfig],
    config_dir: Path,
) -> dict[str, DataFrame]:
    return {
        config.source_name: ingest_source(
            spark=spark,
            config=config,
            config_dir=config_dir,
        )
        for config in configs
    }