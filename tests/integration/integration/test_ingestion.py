import json
from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.testing.utils import assertDataFrameEqual

from grocery.config.models import SourceConfig
from grocery.pipelines.ingestion import ingest_source


def test_ingest_source(
    spark: SparkSession,
    tmp_path: Path,
) -> None:
    source_path = tmp_path / "orders"

    input_df = spark.createDataFrame(
        [
            ("order-1", "customer-1"),
            ("order-2", "customer-2"),
        ],
        schema="""
            order_id string,
            customer_id string
        """,
    )

    input_df.write.parquet(str(source_path))

    schema_dir = tmp_path / "schemas"
    schema_dir.mkdir()

    schema_path = schema_dir / "orders.json"

    schema_path.write_text(
        json.dumps(
            {
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
        )
    )

    config = SourceConfig(
        source_name="orders",
        source_type="file",
        source_format="parquet",
        path_or_table=str(source_path),
        key_columns=["order_id"],
        schema_ref="schemas/orders.json",
        load_type="full",
    )

    actual_df = ingest_source(
        spark=spark,
        config=config,
        config_dir=tmp_path,
    )

    assertDataFrameEqual(actual_df, input_df)