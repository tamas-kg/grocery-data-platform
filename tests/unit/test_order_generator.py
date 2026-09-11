from random import Random
from uuid import UUID
from datetime import datetime
import pytest

from grocery.generation.orders import OrderGenerator


CUSTOMER_IDS = [
    UUID("10000000-0000-4000-8000-000000000001"),
    UUID("10000000-0000-4000-8000-000000000002"),
    UUID("10000000-0000-4000-8000-000000000003"),
]

STORE_IDS = [
    UUID("20000000-0000-4000-8000-000000000001"),
    UUID("20000000-0000-4000-8000-000000000002"),
]


def test_generation_is_deterministic() -> None:
    generator1 = OrderGenerator(
        Random(42),
        customer_ids=CUSTOMER_IDS,
        store_ids=STORE_IDS,
    )
    generator2 = OrderGenerator(
        Random(42),
        customer_ids=CUSTOMER_IDS,
        store_ids=STORE_IDS,
    )

    orders_1 = list(generator1.generate(25))
    orders_2 = list(generator2.generate(25))

    assert orders_1 == orders_2


def test_different_seeds_produce_different_orders() -> None:
    generator1 = OrderGenerator(
        Random(42),
        customer_ids=CUSTOMER_IDS,
        store_ids=STORE_IDS,
    )
    generator2 = OrderGenerator(
        Random(43),
        customer_ids=CUSTOMER_IDS,
        store_ids=STORE_IDS,
    )

    orders_1 = list(generator1.generate(25))
    orders_2 = list(generator2.generate(25))

    assert orders_1 != orders_2


def test_generates_no_orders_when_count_is_zero() -> None:
    generator = OrderGenerator(
        Random(42),
        customer_ids=CUSTOMER_IDS,
        store_ids=STORE_IDS,
    )

    orders = list(generator.generate(0))

    assert orders == []


def test_rejects_negative_count() -> None:
    generator = OrderGenerator(
        Random(42),
        customer_ids=CUSTOMER_IDS,
        store_ids=STORE_IDS,
    )

    with pytest.raises(ValueError):
        list(generator.generate(-1))


def test_rejects_empty_customer_ids() -> None:
    generator = OrderGenerator(
        Random(42),
        customer_ids=[],
        store_ids=STORE_IDS,
    )

    with pytest.raises(ValueError):
        list(generator.generate(10))


def test_rejects_empty_store_ids() -> None:
    generator = OrderGenerator(
        Random(42),
        customer_ids=CUSTOMER_IDS,
        store_ids=[],
    )

    with pytest.raises(ValueError):
        list(generator.generate(10))


def test_orders_reference_existing_customers() -> None:
    generator = OrderGenerator(
        Random(42),
        customer_ids=CUSTOMER_IDS,
        store_ids=STORE_IDS,
    )

    orders = list(generator.generate(100))

    assert all(
        order.customer_id in CUSTOMER_IDS
        for order in orders
    )


def test_orders_reference_existing_stores() -> None:
    generator = OrderGenerator(
        Random(42),
        customer_ids=CUSTOMER_IDS,
        store_ids=STORE_IDS,
    )

    orders = list(generator.generate(100))

    assert all(
        order.store_id in STORE_IDS
        for order in orders
    )


def test_order_ids_are_unique() -> None:
    generator = OrderGenerator(
        Random(42),
        customer_ids=CUSTOMER_IDS,
        store_ids=STORE_IDS,
    )

    orders = list(generator.generate(1000))

    order_ids = [order.order_id for order in orders]

    assert len(order_ids) == len(set(order_ids))


def test_orders_have_valid_timestamps_and_statuses() -> None:
    generator = OrderGenerator(
        Random(42),
        customer_ids=CUSTOMER_IDS,
        store_ids=STORE_IDS,
    )

    orders = list(generator.generate(100))

    start = datetime(2020, 1, 1)
    end = datetime(2025, 1, 1)

    assert all(start <= order.order_timestamp <= end for order in orders)
    assert all(order.status for order in orders)