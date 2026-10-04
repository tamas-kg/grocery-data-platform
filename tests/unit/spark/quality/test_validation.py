from pyspark.sql import SparkSession

from grocery.spark.quality.validation import validate_keys


def test_validate_keys_creates_expected_checks(
    spark: SparkSession,
) -> None:
    df = spark.createDataFrame(
        [
            ("order-1",),
            ("order-1",),
            (None,),
        ],
        schema="order_id string",
    )

    checks = validate_keys(
        df,
        key_columns=["order_id"],
    )

    assert [check.name for check in checks] == [
        "null_keys",
        "duplicate_keys",
    ]
