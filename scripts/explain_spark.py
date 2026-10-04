from decimal import Decimal

from grocery.spark.quality.checks import find_duplicate_keys
from grocery.spark.session import create_spark_session
from grocery.spark.transformations.order_lines import calculate_line_revenue
from grocery.spark.transformations.orders import calculate_order_revenue

spark = create_spark_session()

order_lines = spark.createDataFrame(
    [
        ("order-1", 2, Decimal("3.50")),
        ("order-2", 4, Decimal("2.00")),
    ],
    schema="""
        order_id string,
        quantity long,
        unit_price decimal(10,2)
    """,
)

result = calculate_line_revenue(order_lines)

result.explain(mode="extended")
print("\nLINE REVENUE")
calculate_line_revenue(order_lines).explain(mode="extended")
print("\nDUPLICATE KEYS")
find_duplicate_keys(
    order_lines,
    ["order_id"],
).explain(mode="extended")

print("ORDERS")
orders = spark.createDataFrame(
    [
        ("order-1", "customer-1"),
        ("order-2", "customer-2"),
    ],
    schema="""
        order_id string,
        customer_id string
    """,
)

order_revenue = calculate_order_revenue(
    orders,
    order_lines,
)

order_revenue.explain(mode="formatted")
spark.stop()
