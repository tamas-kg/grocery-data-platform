from grocery.spark.session import create_spark_session


def main() -> None:
    spark = create_spark_session()

    orders = spark.read.parquet("data/source/orders_*.parquet")
    order_lines = spark.read.parquet("data/source/order_lines_*.parquet")
    products = spark.read.parquet("data/source/products_*.parquet")

    orders.printSchema()
    order_lines.printSchema()
    products.printSchema()

    orders.show(10, truncate=False)
    order_lines.show(10, truncate=False)
    products.show(10, truncate=False)

    print(orders.count())
    print(order_lines.count())
    print(products.count())

    orders.select("status").distinct().show()
    order_lines.select("quantity").summary().show()

    spark.stop()


if __name__ == "__main__":
    main()