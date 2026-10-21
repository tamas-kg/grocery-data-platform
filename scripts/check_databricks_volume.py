from grocery.spark.session import create_spark_session


def main() -> None:
    spark = create_spark_session()

    orders = spark.read.parquet(
        "/Volumes/workspace/grocery/landing/source/orders_*.parquet"
    )

    orders.printSchema()
    orders.show(5, truncate=False)


if __name__ == "__main__":
    main()