import logging
from pathlib import Path
from random import Random
from datetime import datetime

from grocery.io.parquet import ParquetWriter
from grocery.pipeline.config import GenerationConfig
from grocery.pipeline.generate import GroceryDataGenerator


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)


def main() -> None:
    config = GenerationConfig(
        seed=42,
        output_dir=Path("data/source"),
        vendor_count=100,
        customer_count=10_000,
        store_count=50,
        product_count=5_000,
        order_count=100_000,
        order_line_count=300_000,
        order_start_timestamp=datetime(2024, 1, 1),
        order_end_timestamp=datetime(2024, 2, 1),
    )

    generator = GroceryDataGenerator(
        rng=Random(42),
        writer=ParquetWriter(),
    )

    generator.run(config)


if __name__ == "__main__":
    main()