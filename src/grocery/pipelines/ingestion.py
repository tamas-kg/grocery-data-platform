from pathlib import Path

from pyspark.sql import DataFrame, SparkSession

from grocery.config.models import SourceConfig
from grocery.config.schema_loader import load_spark_schema
from grocery.spark.readers import read_source
from grocery.spark.quality.models import QualityFailure
from grocery.spark.quality.policy import evaluate_checks
from grocery.spark.quality.validation import validate_keys
from grocery.pipelines.exceptions import DataQualityError


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


def validate_source(
    df: DataFrame,
    config: SourceConfig,
) -> list[QualityFailure]:
    checks = validate_keys(
        df=df,
        key_columns=config.key_columns,
    )

    return evaluate_checks(checks)


def ingest_and_validate_source(
    spark: SparkSession,
    config: SourceConfig,
    config_dir: Path,
) -> DataFrame:
    df = ingest_source(
        spark=spark,
        config=config,
        config_dir=config_dir,
    )

    failures = validate_source(
        df=df,
        config=config,
    )

    if failures:
        failure_summary = ", ".join(
            f"{failure.check_name}={failure.violation_count}"
            for failure in failures
        )

        raise DataQualityError(
            f"Data quality validation failed for "
            f"{config.source_name}: {failure_summary}"
        )

    return df


def ingest_and_validate_sources(
    spark: SparkSession,
    configs: list[SourceConfig],
    config_dir: Path,
) -> dict[str, DataFrame]:
    return {
        config.source_name: ingest_and_validate_source(
            spark=spark,
            config=config,
            config_dir=config_dir,
        )
        for config in configs
    }