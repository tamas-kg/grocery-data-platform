import json
from decimal import Decimal
from pathlib import Path

import yaml
from pyspark.sql import SparkSession
from pyspark.testing.utils import assertDataFrameEqual

from grocery.app import run_pipeline


def test_run_pipeline_end_to_end(
    spark: SparkSession,
    tmp_path: Path,
) -> None:
    source_dir = tmp_path / "source"
    schema_dir = tmp_path / "schemas"

    source_dir.mkdir()
    schema_dir.mkdir()

    # ------------------------------------------------------------------
    # Arrange: source data
    # ------------------------------------------------------------------

    orders = spark.createDataFrame(
        [
            ("order-1", "customer-1"),
            ("order-2", "customer-2"),
            ("order-3", "customer-3"),
        ],
        schema="""
            order_id string,
            customer_id string
        """,
    )

    order_lines = spark.createDataFrame(
        [
            (
                "line-1",
                "order-1",
                "product-1",
                2,
                Decimal("4.00"),
            ),
            (
                "line-2",
                "order-1",
                "product-2",
                1,
                Decimal("3.00"),
            ),
            (
                "line-3",
                "order-2",
                "product-1",
                1,
                Decimal("4.00"),
            ),
        ],
        schema="""
            order_line_id string,
            order_id string,
            product_id string,
            quantity long,
            unit_price decimal(10,2)
        """,
    )

    products = spark.createDataFrame(
        [
            (
                "product-1",
                "vendor-1",
                "Dairy",
                "Milk",
                "Brand A",
                Decimal("2.00"),
                Decimal("4.00"),
            ),
            (
                "product-2",
                "vendor-1",
                "Bakery",
                "Bread",
                "Brand B",
                Decimal("2.00"),
                Decimal("3.00"),
            ),
        ],
        schema="""
            product_id string,
            vendor_id string,
            category string,
            name string,
            brand string,
            unit_cost decimal(10,2),
            unit_price decimal(10,2)
        """,
    )

    orders.write.parquet(str(source_dir / "orders"))
    order_lines.write.parquet(str(source_dir / "order_lines"))
    products.write.parquet(str(source_dir / "products"))

    # ------------------------------------------------------------------
    # Arrange: Spark schemas
    # ------------------------------------------------------------------

    orders_schema = {
        "type": "struct",
        "fields": [
            {
                "name": "order_id",
                "type": "string",
                "nullable": True,
                "metadata": {},
            },
            {
                "name": "customer_id",
                "type": "string",
                "nullable": True,
                "metadata": {},
            },
        ],
    }

    order_lines_schema = {
        "type": "struct",
        "fields": [
            {
                "name": "order_line_id",
                "type": "string",
                "nullable": True,
                "metadata": {},
            },
            {
                "name": "order_id",
                "type": "string",
                "nullable": True,
                "metadata": {},
            },
            {
                "name": "product_id",
                "type": "string",
                "nullable": True,
                "metadata": {},
            },
            {
                "name": "quantity",
                "type": "long",
                "nullable": True,
                "metadata": {},
            },
            {
                "name": "unit_price",
                "type": "decimal(10,2)",
                "nullable": True,
                "metadata": {},
            },
        ],
    }

    products_schema = {
        "type": "struct",
        "fields": [
            {
                "name": "product_id",
                "type": "string",
                "nullable": True,
                "metadata": {},
            },
            {
                "name": "vendor_id",
                "type": "string",
                "nullable": True,
                "metadata": {},
            },
            {
                "name": "category",
                "type": "string",
                "nullable": True,
                "metadata": {},
            },
            {
                "name": "name",
                "type": "string",
                "nullable": True,
                "metadata": {},
            },
            {
                "name": "brand",
                "type": "string",
                "nullable": True,
                "metadata": {},
            },
            {
                "name": "unit_cost",
                "type": "decimal(10,2)",
                "nullable": True,
                "metadata": {},
            },
            {
                "name": "unit_price",
                "type": "decimal(10,2)",
                "nullable": True,
                "metadata": {},
            },
        ],
    }

    with (schema_dir / "orders.json").open("w") as file:
        json.dump(orders_schema, file)

    with (schema_dir / "order_lines.json").open("w") as file:
        json.dump(order_lines_schema, file)

    with (schema_dir / "products.json").open("w") as file:
        json.dump(products_schema, file)

    # ------------------------------------------------------------------
    # Arrange: source configuration
    # ------------------------------------------------------------------

    config = {
        "sources": [
            {
                "source_name": "orders",
                "source_type": "file",
                "source_format": "parquet",
                "path_or_table": str(source_dir / "orders"),
                "key_columns": ["order_id"],
                "schema_ref": "schemas/orders.json",
                "load_type": "full",
            },
            {
                "source_name": "order_lines",
                "source_type": "file",
                "source_format": "parquet",
                "path_or_table": str(source_dir / "order_lines"),
                "key_columns": ["order_line_id"],
                "schema_ref": "schemas/order_lines.json",
                "load_type": "full",
            },
            {
                "source_name": "products",
                "source_type": "file",
                "source_format": "parquet",
                "path_or_table": str(source_dir / "products"),
                "key_columns": ["product_id"],
                "schema_ref": "schemas/products.json",
                "load_type": "full",
            },
        ]
    }

    config_path = tmp_path / "sources.yaml"

    with config_path.open("w") as file:
        yaml.safe_dump(config, file)

    # ------------------------------------------------------------------
    # Act
    # ------------------------------------------------------------------

    result = run_pipeline(
        spark=spark,
        config_path=config_path,
    )

    # ------------------------------------------------------------------
    # Assert: application outputs
    # ------------------------------------------------------------------

    assert set(result) == {
        "order_analytics",
        "product_analytics",
    }

    expected_orders = spark.createDataFrame(
        [
            (
                "order-1",
                "customer-1",
                Decimal("11.00"),
            ),
            (
                "order-2",
                "customer-2",
                Decimal("4.00"),
            ),
            (
                "order-3",
                "customer-3",
                None,
            ),
        ],
        schema="""
            order_id string,
            customer_id string,
            order_revenue decimal(38,2)
        """,
    )

    assertDataFrameEqual(
        result["order_analytics"],
        expected_orders,
        checkRowOrder=False,
    )

    expected_products = spark.createDataFrame(
        [
            (
                "product-1",
                "vendor-1",
                "Dairy",
                "Milk",
                "Brand A",
                Decimal("2.00"),
                Decimal("4.00"),
                Decimal("2.00"),
                0.5,
            ),
            (
                "product-2",
                "vendor-1",
                "Bakery",
                "Bread",
                "Brand B",
                Decimal("2.00"),
                Decimal("3.00"),
                Decimal("1.00"),
                1 / 3,
            ),
        ],
        schema="""
            product_id string,
            vendor_id string,
            category string,
            name string,
            brand string,
            unit_cost decimal(10,2),
            unit_price decimal(10,2),
            unit_margin decimal(11,2),
            margin_percentage double
        """,
    )

    assertDataFrameEqual(
        result["product_analytics"],
        expected_products,
        checkRowOrder=False,
    )
