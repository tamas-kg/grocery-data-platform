def test_spark_starts(spark):
    assert spark.range(10).count() == 10