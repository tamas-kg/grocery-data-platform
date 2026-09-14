import logging
from collections.abc import Sequence
from decimal import Decimal
from pathlib import Path
from uuid import UUID

from grocery.generation.customers import CustomerGenerator
from grocery.generation.orderlines import OrderLineGenerator
from grocery.generation.orders import OrderGenerator
from grocery.generation.products import ProductGenerator
from grocery.generation.random import create_rng
from grocery.generation.stores import StoreGenerator
from grocery.generation.vendors import VendorGenerator
from grocery.io.parquet import ParquetWriter
from grocery.io.schemas import (
    CUSTOMER_SCHEMA,
    ORDER_LINE_SCHEMA,
    ORDER_SCHEMA,
    PRODUCT_SCHEMA,
    STORE_SCHEMA,
    VENDOR_SCHEMA,
)
from grocery.pipeline.config import GenerationConfig

logger = logging.getLogger(__name__)


class GroceryDataGenerator:

    def __init__(self, config: GenerationConfig) -> None:
        self._config = config

    def run(self) -> None:
        vendors = self._generate_vendors()
        customers = self._generate_customers()
        stores = self._generate_stores()
        products = self._generate_products(vendors)
        orders = self._generate_orders(customers, stores)
        self._generate_order_lines(orders, products)

    def _generate_vendors(self):
        logger.info("Generating vendors")

        generator = VendorGenerator(
            rng=create_rng(self._config.seed, "vendors"),
        )

        vendors = list(
            generator.generate(self._config.vendor_count)
        )

        ParquetWriter(
            schema=VENDOR_SCHEMA,
        ).write(
            vendors,
            self._config.output_dir / "vendors.parquet",
        )

        return vendors

    def _generate_customers(self):
        logger.info("Generating customers")

        generator = CustomerGenerator(
            rng=create_rng(self._config.seed, "customers"),
        )

        customers = list(
            generator.generate(self._config.customer_count)
        )

        ParquetWriter(
            schema=CUSTOMER_SCHEMA,
        ).write(
            customers,
            self._config.output_dir / "customers.parquet",
        )

        return customers

    def _generate_stores(self):
        logger.info("Generating stores")

        generator = StoreGenerator(
            rng=create_rng(self._config.seed, "stores"),
        )

        stores = list(
            generator.generate(self._config.store_count)
        )

        ParquetWriter(
            schema=STORE_SCHEMA,
        ).write(
            stores,
            self._config.output_dir / "stores.parquet",
        )

        return stores

    def _generate_products(self, vendors):
        logger.info("Generating products")

        vendor_ids = [
            vendor.vendor_id
            for vendor in vendors
        ]

        generator = ProductGenerator(
            rng=create_rng(self._config.seed, "products"),
            vendor_ids=vendor_ids,
        )

        products = list(
            generator.generate(self._config.product_count)
        )

        ParquetWriter(
            schema=PRODUCT_SCHEMA,
        ).write(
            products,
            self._config.output_dir / "products.parquet",
        )

        return products

    def _generate_orders(self, customers, stores):
        logger.info("Generating orders")

        customer_ids = [
            customer.customer_id
            for customer in customers
        ]

        store_ids = [
            store.store_id
            for store in stores
        ]

        generator = OrderGenerator(
            rng=create_rng(self._config.seed, "orders"),
            customer_ids=customer_ids,
            store_ids=store_ids,
            start_timestamp=self._config.order_start_timestamp,
            end_timestamp=self._config.order_end_timestamp,
        )

        orders = list(
            generator.generate(self._config.order_count)
        )

        ParquetWriter(
            schema=ORDER_SCHEMA,
        ).write(
            orders,
            self._config.output_dir / "orders.parquet",
        )

        return orders

    def _generate_order_lines(self, orders, products) -> None:
        logger.info("Generating order lines")

        order_ids = [
            order.order_id
            for order in orders
        ]

        product_prices = {
            product.product_id: product.unit_price
            for product in products
        }

        generator = OrderLineGenerator(
            rng=create_rng(self._config.seed, "order_lines"),
            order_ids=order_ids,
            product_prices=product_prices,
        )

        order_lines = generator.generate(
            self._config.order_line_count
        )

        ParquetWriter(
            schema=ORDER_LINE_SCHEMA,
        ).write(
            order_lines,
            self._config.output_dir / "order_lines.parquet",
        )