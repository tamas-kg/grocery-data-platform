import json
from pathlib import Path

from pyspark.sql.types import (
    DecimalType,
    LongType,
    StringType,
    StructType
)

from grocery.config.schema_loader import load_spark_schema


def test_load_spark_schema(tmp_path: Path) -> None:
    schema_path = tmp_path / "schema.json"

    schema_path.write_text(
        json.dumps(
            {
                "type": "struct",
                "fields": [
                    {
                        "name": "id",
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
                        "name": "price",
                        "type": "decimal(10,2)",
                        "nullable": True,
                        "metadata": {},
                    },
                ],
            }
        )
    )

    schema = load_spark_schema(schema_path)

    assert isinstance(schema, StructType)

    assert schema["id"].dataType == StringType()
    assert schema["quantity"].dataType == LongType()
    assert schema["price"].dataType == DecimalType(10, 2)