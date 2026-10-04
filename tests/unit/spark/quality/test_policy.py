from pyspark.sql import SparkSession

from grocery.spark.quality.models import QualityCheck
from grocery.spark.quality.policy import evaluate_checks


def test_evaluate_checks_returns_failures(
    spark: SparkSession,
) -> None:
    violations = spark.createDataFrame(
        [
            ("order-1",),
            ("order-2",),
        ],
        schema="order_id string",
    )

    checks = [
        QualityCheck(
            name="duplicate_keys",
            violations=violations,
        )
    ]

    failures = evaluate_checks(checks)

    assert len(failures) == 1
    assert failures[0].check_name == "duplicate_keys"
    assert failures[0].violation_count == 2


def test_evaluate_checks_returns_no_failures(
    spark: SparkSession,
) -> None:
    violations = spark.createDataFrame(
        [],
        schema="order_id string",
    )

    checks = [
        QualityCheck(
            name="duplicate_keys",
            violations=violations,
        )
    ]

    failures = evaluate_checks(checks)

    assert failures == []
