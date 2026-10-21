import argparse
import os

from grocery.pipelines.order_analytics import build_order_analytics
from grocery.pipelines.product_analytics import build_product_analytics
from grocery.spark.session import create_spark_session


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--execution-mode",
        choices=["local", "connect", "databricks"],
        default=None,
    )
    args = parser.parse_args()

    if args.execution_mode is not None:
        os.environ["GROCERY_EXECUTION_MODE"] = args.execution_mode

    spark = create_spark_session()

    orders = spark.table("workspace.silver.orders")
    order_lines = spark.table("workspace.silver.order_lines")
    products = spark.table("workspace.silver.products")

    outputs = {
        "order_analytics": build_order_analytics(
            orders=orders,
            order_lines=order_lines,
        ),
        "product_analytics": build_product_analytics(
            products=products,
        ),
    }

    for name, df in outputs.items():
        table_name = f"workspace.gold.{name}"

        (
            df.write
            .format("delta")
            .mode("overwrite")
            .saveAsTable(table_name)
        )

        print(f"Written: {table_name}")


if __name__ == "__main__":
    main()