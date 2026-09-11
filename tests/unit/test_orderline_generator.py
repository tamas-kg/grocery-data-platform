from decimal import Decimal
from random import Random
from uuid import UUID

import pytest

from grocery.generation.orderlines import OrderLineGenerator


ORDER_IDS = [
    UUID("30000000-0000-4000-8000-000000000001"),
    UUID("30000000-0000-4000-8000-000000000002"),
]

PRODUCT_PRICES = {
    UUID("40000000-0000-4000-8000-000000000001"): Decimal("1.50"),
    UUID("40000000-0000-4000-8000-000000000002"): Decimal("2.75"),
    UUID("40000000-0000-4000-8000-000000000003"): Decimal("5.25"),
}


def test_generation_is_deterministic() -> None:
    generator1 = OrderLineGenerator(
        Random(42),
        order_ids=ORDER_IDS,
        product_prices=PRODUCT_PRICES,
    )
    generator2 = OrderLineGenerator(
        Random(42),
        order_ids=ORDER_IDS,
        product_prices=PRODUCT_PRICES,
    )

    lines_1 = list(generator1.generate(25))
    lines_2 = list(generator2.generate(25))

    assert lines_1 == lines_2


def test_different_seeds_produce_different_order_lines() -> None:
    generator1 = OrderLineGenerator(
        Random(42),
        order_ids=ORDER_IDS,
        product_prices=PRODUCT_PRICES,
    )
    generator2 = OrderLineGenerator(
        Random(43),
        order_ids=ORDER_IDS,
        product_prices=PRODUCT_PRICES,
    )

    lines_1 = list(generator1.generate(25))
    lines_2 = list(generator2.generate(25))

    assert lines_1 != lines_2


def test_generates_no_order_lines_when_count_is_zero() -> None:
    generator = OrderLineGenerator(
        Random(42),
        order_ids=ORDER_IDS,
        product_prices=PRODUCT_PRICES,
    )

    lines = list(generator.generate(0))

    assert lines == []


def test_rejects_negative_count() -> None:
    generator = OrderLineGenerator(
        Random(42),
        order_ids=ORDER_IDS,
        product_prices=PRODUCT_PRICES,
    )

    with pytest.raises(ValueError):
        list(generator.generate(-1))


def test_rejects_empty_order_ids() -> None:
    generator = OrderLineGenerator(
        Random(42),
        order_ids=[],
        product_prices=PRODUCT_PRICES,
    )

    with pytest.raises(ValueError):
        list(generator.generate(10))


def test_rejects_empty_product_prices() -> None:
    generator = OrderLineGenerator(
        Random(42),
        order_ids=ORDER_IDS,
        product_prices={},
    )

    with pytest.raises(ValueError):
        list(generator.generate(10))


def test_order_lines_reference_existing_orders() -> None:
    generator = OrderLineGenerator(
        Random(42),
        order_ids=ORDER_IDS,
        product_prices=PRODUCT_PRICES,
    )

    lines = list(generator.generate(100))

    assert all(
        line.order_id in ORDER_IDS
        for line in lines
    )


def test_order_lines_reference_existing_products() -> None:
    generator = OrderLineGenerator(
        Random(42),
        order_ids=ORDER_IDS,
        product_prices=PRODUCT_PRICES,
    )

    lines = list(generator.generate(100))

    assert all(
        line.product_id in PRODUCT_PRICES
        for line in lines
    )


def test_order_line_uses_product_price() -> None:
    generator = OrderLineGenerator(
        Random(42),
        order_ids=ORDER_IDS,
        product_prices=PRODUCT_PRICES,
    )

    lines = list(generator.generate(100))

    assert all(
        line.unit_price == PRODUCT_PRICES[line.product_id]
        for line in lines
    )


def test_order_line_ids_are_unique() -> None:
    generator = OrderLineGenerator(
        Random(42),
        order_ids=ORDER_IDS,
        product_prices=PRODUCT_PRICES,
    )

    lines = list(generator.generate(1000))

    order_line_ids = [line.order_line_id for line in lines]

    assert len(order_line_ids) == len(set(order_line_ids))


def test_quantity_is_positive() -> None:
    generator = OrderLineGenerator(
        Random(42),
        order_ids=ORDER_IDS,
        product_prices=PRODUCT_PRICES,
    )

    lines = list(generator.generate(100))

    assert all(line.quantity > 0 for line in lines)