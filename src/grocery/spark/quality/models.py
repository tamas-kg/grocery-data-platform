from dataclasses import dataclass

from pyspark.sql import DataFrame


@dataclass(frozen=True, slots=True)
class QualityCheck:
    name: str
    violations: DataFrame


@dataclass(frozen=True, slots=True)
class QualityFailure:
    check_name: str
    violation_count: int
