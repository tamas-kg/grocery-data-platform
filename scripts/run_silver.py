import argparse
import os
from pathlib import Path

from grocery.config.loader import load_sources
from grocery.pipelines.exceptions import DataQualityError
from grocery.pipelines.ingestion import validate_source
from grocery.spark.session import create_spark_session


def main() -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument(
    "--config",
    type=Path,
    default=Path("config/sources_databricks.yaml"),
    )
    parser.add_argument(
    "--execution-mode",
    choices=["local", "connect", "databricks"],
    default=None,
    )

    args = parser.parse_args()

    if args.execution_mode is not None:
        os.environ["GROCERY_EXECUTION_MODE"] = args.execution_mode

    # Create Spark only after selecting the execution mode.
    spark = create_spark_session()

    config_path = args.config
    configs = load_sources(config_path)

    for config in configs:
        source_table = f"workspace.bronze.{config.source_name}"
        target_table = f"workspace.silver.{config.source_name}"

        df = spark.table(source_table)

        failures = validate_source(df, config)

        if failures:
            summary = ", ".join(
                f"{failure.check_name}={failure.violation_count}"
                for failure in failures
            )
            raise DataQualityError(
                f"Data quality validation failed for "
                f"{config.source_name}: {summary}"
            )

        (
            df.write
            .format("delta")
            .mode("overwrite")
            .saveAsTable(target_table)
        )

        print(f"Written: {target_table}")


if __name__ == "__main__":
    main()