import argparse
import os
from pathlib import Path

from pyspark.sql import functions as F

from grocery.config.loader import load_sources
from grocery.pipelines.ingestion import ingest_source
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
        df = ingest_source(
            spark=spark,
            config=config,
            config_dir=config_path.parent,
        )

        bronze_df = (
            df.withColumn("_ingested_at", F.current_timestamp())
            .withColumn("_source_name", F.lit(config.source_name))
        )

        table_name = f"workspace.bronze.{config.source_name}"

        (
            bronze_df.write
            .format("delta")
            .mode("overwrite")
            .saveAsTable(table_name)
        )

        print(f"Written: {table_name}")


if __name__ == "__main__":
    main()