from random import Random
from decimal import Decimal
import pytest

from grocery.generation.products import ProductGenerator


def test_generates_requested_number_of_products() -> None:
    generator = ProductGenerator(Random(42))

    products = list(generator.generate(10))

    assert len(products) == 10

def test_product_ids_are_unique() -> None:
    generator = ProductGenerator(Random(42))

    products = list(generator.generate(100))

    product_ids = [product.product_id for product in products]

    assert len(product_ids) == len(set(product_ids))

def test_products_have_valid_categories() -> None:
    generator = ProductGenerator(Random(42))

    products = list(generator.generate(100))

    valid_categories = {
        "Dairy",
        "Bakery",
        "Produce",
        "Beverages",
        "Snacks",
    }

    assert all(
        product.category in valid_categories
        for product in products
    )

def test_product_price_is_greater_than_cost() -> None:
    generator = ProductGenerator(Random(42))

    products = list(generator.generate(100))

    assert all(
        product.unit_price > product.unit_cost
        for product in products
    )

def test_product_name_belongs_to_category() -> None:
    generator = ProductGenerator(Random(42))

    products = list(generator.generate(100))

    valid_products = {
        "Dairy": {"Milk", "Cheese", "Yogurt", "Butter"},
        "Bakery": {"Bread", "Croissant", "Bagel", "Roll"},
        "Produce": {"Apple", "Banana", "Orange", "Tomato"},
        "Beverages": {"Coffee", "Tea", "Juice", "Water"},
        "Snacks": {"Chips", "Chocolate", "Cookies", "Nuts"},
    }

    assert all(
        product.name in valid_products[product.category]
        for product in products
    )


def test_generation_is_deterministic() -> None:
    generator1 = ProductGenerator(Random(42))
    generator2 = ProductGenerator(Random(42))
    
    products_1 = list(generator1.generate(25))
    products_2 = list(generator2.generate(25))
    print(products_1)

    assert products_1 == products_2

def test_different_seeds_produce_different_products() -> None:
    generator1 = ProductGenerator(Random(42))
    generator2 = ProductGenerator(Random(43))

    products_1 = list(generator1.generate(25))
    products_2 = list(generator2.generate(25))

    assert products_1 != products_2

def test_generates_no_products_when_count_is_zero() -> None:
    generator = ProductGenerator(Random(42))

    products = list(generator.generate(0))

    assert products == []

def test_rejects_negative_count() -> None:
    generator = ProductGenerator(Random(42))

    with pytest.raises(ValueError):
        list(generator.generate(-1))

def test_products_have_valid_brands() -> None:
    generator = ProductGenerator(Random(42))

    products = list(generator.generate(100))

    valid_brands = {
        "Generic",
        "FreshMart",
        "DailyChoice",
        "Premium Foods",
    }

    assert all(
        product.brand in valid_brands
        for product in products
    )

def test_product_cost_is_within_expected_range() -> None:
    generator = ProductGenerator(Random(42))

    products = list(generator.generate(1000))

    assert all(
        Decimal("0.50") <= product.unit_cost <= Decimal("10.00")
        for product in products
    )

def test_product_margin_is_within_expected_range() -> None:
    generator = ProductGenerator(Random(42))

    products = list(generator.generate(1000))

    assert all(
        Decimal("0.10")
        <= product.unit_price - product.unit_cost
        <= Decimal("5.00")
        for product in products
    )