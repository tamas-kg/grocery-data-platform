import json
from pathlib import Path

from pyspark.sql.types import StructType


def load_spark_schema(path: Path) -> StructType:
    with path.open() as file:
        schema_json = json.load(file)

    return StructType.fromJson(schema_json)