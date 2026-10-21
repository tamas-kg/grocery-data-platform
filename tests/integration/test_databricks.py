import pytest

from grocery.pipelines.order_analytics import build_order_analytics
from grocery.spark.session import create_spark_session


@pytest.fixture(scope="module")
def spark():
    session = create_spark_session()
    yield session


@pytest.mark.databricks
def test_read_silver_table(spark):
    df = spark.table("workspace.silver.orders")

    assert df.count() > 0
    assert "order_id" in df.columns


@pytest.mark.databricks
def test_order_analytics_on_databricks(spark):
    orders = spark.table("workspace.silver.orders")
    order_lines = spark.table("workspace.silver.order_lines")

    result = build_order_analytics(orders, order_lines)

    assert result.count() == orders.count()