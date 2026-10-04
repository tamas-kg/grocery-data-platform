from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def find_null_keys(
    df: DataFrame,
    key_columns: list[str],
) -> DataFrame:
    condition = F.lit(False)

    for column in key_columns:
        condition = condition | F.col(column).isNull()

    return df.filter(condition)


def find_duplicate_keys(
    df: DataFrame,
    key_columns: list[str],
) -> DataFrame:
    return df.groupBy(*key_columns).count().filter(F.col("count") > 1)
