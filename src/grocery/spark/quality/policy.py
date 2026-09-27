from grocery.spark.quality.models import (
    QualityCheck,
    QualityFailure,
)


def evaluate_checks(
    checks: list[QualityCheck],
) -> list[QualityFailure]:
    failures = []

    for check in checks:
        violation_count = check.violations.count()

        if violation_count > 0:
            failures.append(
                QualityFailure(
                    check_name=check.name,
                    violation_count=violation_count,
                )
            )

    return failures