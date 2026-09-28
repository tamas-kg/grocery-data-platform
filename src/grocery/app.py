from pathlib import Path

from pyspark.sql import DataFrame, SparkSession

from grocery.config.loader import load_sources
from grocery.pipelines.ingestion import ingest_and_validate_sources
from grocery.pipelines.order_analytics import build_order_analytics
from grocery.pipelines.product_analytics import build_product_analytics


def run_pipeline(
    spark: SparkSession,
    config_path: Path,
) -> dict[str, DataFrame]:
    configs = load_sources(config_path)

    datasets = ingest_and_validate_sources(
        spark=spark,
        configs=configs,
        config_dir=config_path.parent,
    )

    order_analytics = build_order_analytics(
        orders=datasets["orders"],
        order_lines=datasets["order_lines"],
    )

    product_analytics = build_product_analytics(
        products=datasets["products"],
    )

    return {
        "order_analytics": order_analytics,
        "product_analytics": product_analytics,
    }