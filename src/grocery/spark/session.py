import os

from pyspark.sql import SparkSession


def create_spark_session() -> SparkSession:
    mode = os.getenv("GROCERY_EXECUTION_MODE", "local")

    if mode == "connect":
        from databricks.connect import DatabricksSession

        return (
            DatabricksSession.builder
            .profile("dev")
            .serverless()
            .getOrCreate()
        )

    if mode == "databricks":
        return SparkSession.builder.getOrCreate()

    if mode == "local":
        return (
            SparkSession.builder
            .appName("grocery-data-platform")
            .master("local[*]")
            .getOrCreate()
        )

    raise ValueError(f"Unsupported execution mode: {mode}")