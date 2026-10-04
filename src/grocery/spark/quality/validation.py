from pyspark.sql import DataFrame

from grocery.spark.quality.checks import (
    find_duplicate_keys,
    find_null_keys,
)
from grocery.spark.quality.models import QualityCheck


def validate_keys(
    df: DataFrame,
    key_columns: list[str],
) -> list[QualityCheck]:
    return [
        QualityCheck(
            name="null_keys",
            violations=find_null_keys(df, key_columns),
        ),
        QualityCheck(
            name="duplicate_keys",
            violations=find_duplicate_keys(df, key_columns),
        ),
    ]
