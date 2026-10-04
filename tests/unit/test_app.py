from pathlib import Path
from unittest.mock import patch

from pyspark.sql import SparkSession

from grocery.app import run_pipeline
from grocery.config.models import SourceConfig


def test_run_pipeline_builds_expected_outputs(
    spark: SparkSession,
    tmp_path: Path,
) -> None:
    config_path = tmp_path / "sources.yaml"

    configs = [
        SourceConfig(
            source_name="orders",
            source_type="file",
            source_format="parquet",
            path_or_table="orders.parquet",
            key_columns=["order_id"],
            schema_ref="schemas/orders.json",
            load_type="full",
        ),
        SourceConfig(
            source_name="order_lines",
            source_type="file",
            source_format="parquet",
            path_or_table="order_lines.parquet",
            key_columns=["order_line_id"],
            schema_ref="schemas/order_lines.json",
            load_type="full",
        ),
        SourceConfig(
            source_name="products",
            source_type="file",
            source_format="parquet",
            path_or_table="products.parquet",
            key_columns=["product_id"],
            schema_ref="schemas/products.json",
            load_type="full",
        ),
    ]

    orders = spark.createDataFrame(
        [("order-1",)],
        schema="order_id string",
    )

    order_lines = spark.createDataFrame(
        [("line-1",)],
        schema="order_line_id string",
    )

    products = spark.createDataFrame(
        [("product-1",)],
        schema="product_id string",
    )

    order_analytics = spark.createDataFrame(
        [("order-1",)],
        schema="order_id string",
    )

    product_analytics = spark.createDataFrame(
        [("product-1",)],
        schema="product_id string",
    )

    with (
        patch(
            "grocery.app.load_sources",
            return_value=configs,
        ),
        patch(
            "grocery.app.ingest_and_validate_sources",
            return_value={
                "orders": orders,
                "order_lines": order_lines,
                "products": products,
            },
        ),
        patch(
            "grocery.app.build_order_analytics",
            return_value=order_analytics,
        ) as mock_build_orders,
        patch(
            "grocery.app.build_product_analytics",
            return_value=product_analytics,
        ) as mock_build_products,
    ):
        result = run_pipeline(
            spark=spark,
            config_path=config_path,
        )

    assert result == {
        "order_analytics": order_analytics,
        "product_analytics": product_analytics,
    }

    mock_build_orders.assert_called_once_with(
        orders=orders,
        order_lines=order_lines,
    )

    mock_build_products.assert_called_once_with(
        products=products,
    )
