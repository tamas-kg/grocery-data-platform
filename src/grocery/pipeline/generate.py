from random import Random
from pathlib import Path
import logging

from grocery.generation.customers import CustomerGenerator
from grocery.generation.orderlines import OrderLineGenerator
from grocery.generation.orders import OrderGenerator
from grocery.generation.products import ProductGenerator
from grocery.generation.stores import StoreGenerator
from grocery.generation.vendors import VendorGenerator
from grocery.io.parquet import ParquetWriter
from grocery.generation.random import create_rng
from grocery.pipeline.config import GenerationConfig

logger = logging.getLogger(__name__)

class GroceryDataGenerator:

    def __init__(
        self,
        rng: Random,
        writer: ParquetWriter,
    ) -> None:
        self._rng = rng
        self._writer = writer

    def run(self, config: GenerationConfig) -> None:
        output_dir = config.output_dir

        logger.info("Generating vendors...")
        vendors = list(
            VendorGenerator(
                create_rng(config.seed, "vendors")
            ).generate(config.vendor_count)
)

        vendor_ids = [
            vendor.vendor_id
            for vendor in vendors
        ]

        self._writer.write(
            vendors,
            output_dir / "vendors.parquet",
        )

        logger.info("Generating customers...")
        customers = list(
            CustomerGenerator(
                create_rng(config.seed, "customers")
            ).generate(config.customer_count)
        )

        customer_ids = [
            customer.customer_id
            for customer in customers
        ]

        self._writer.write(
            customers,
            output_dir / "customers.parquet",
        )

        logger.info("Generating stores...")
        stores = list(
            StoreGenerator(
                create_rng(config.seed, "stores")
            ).generate(config.store_count)
        )

        store_ids = [
            store.store_id
            for store in stores
        ]

        self._writer.write(
            stores,
            output_dir / "stores.parquet",
        )

        logger.info("Generating products...")
        products = list(
            ProductGenerator(
                create_rng(config.seed, "products"),
                vendor_ids,
            ).generate(config.product_count)
        )

        product_prices = {
            product.product_id: product.unit_price
            for product in products
        }

        self._writer.write(
            products,
            output_dir / "products.parquet",
        )

        logger.info("Generating orders...")
        orders = list(
            OrderGenerator(
                create_rng(config.seed, "orders"),
                customer_ids,
                store_ids,
                start_timestamp=config.order_start_timestamp,
                end_timestamp=config.order_end_timestamp,
            ).generate(config.order_count)
        )

        order_ids = [
            order.order_id
            for order in orders
        ]

        self._writer.write(
            orders,
            output_dir / "orders.parquet",
        )

        logger.info("Generating order lines...")
        order_lines = OrderLineGenerator(
            create_rng(config.seed, "order_lines"),
            order_ids,
            product_prices,
        ).generate(config.order_line_count)

        self._writer.write(
            order_lines,
            output_dir / "order_lines.parquet",
        )