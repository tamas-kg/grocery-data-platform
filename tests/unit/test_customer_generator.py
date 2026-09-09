from random import Random
from decimal import Decimal
import pytest
import re

from grocery.generation.customers import CustomerGenerator

def test_generation_is_deterministic() -> None:
    generator1 = CustomerGenerator(Random(42))
    generator2 = CustomerGenerator(Random(42))
    
    customers_1 = list(generator1.generate(25))
    customers_2 = list(generator2.generate(25))
    print(customers_1)

    assert customers_1 == customers_2

def test_different_seeds_produce_different_customers() -> None:
    generator1 = CustomerGenerator(Random(42))
    generator2 = CustomerGenerator(Random(43))

    customers_1 = list(generator1.generate(25))
    customers_2 = list(generator2.generate(25))

    assert customers_1 != customers_2

def test_generates_no_customers_when_count_is_zero() -> None:
    generator = CustomerGenerator(Random(42))

    customers = list(generator.generate(0))

    assert customers == []

def test_rejects_negative_count() -> None:
    generator = CustomerGenerator(Random(42))

    with pytest.raises(ValueError):
        list(generator.generate(-1))

def test_customer_emails_are_unique() -> None:
    generator = CustomerGenerator(Random(42))

    customers = list(generator.generate(1000))

    emails = [customer.email for customer in customers]

    assert len(emails) == len(set(emails))

def test_payment_cards_are_unique() -> None:
    generator = CustomerGenerator(Random(42))

    customers = list(generator.generate(1000))

    cards = [customer.payment_card for customer in customers]

    assert len(cards) == len(set(cards))

def test_phone_numbers_have_valid_format() -> None:
    generator = CustomerGenerator(Random(42))

    customers = list(generator.generate(100))

    pattern = r"^\+44 \d{9}$"

    assert all(
        re.match(pattern, customer.phone)
        for customer in customers
    )

def test_emails_have_valid_format() -> None:
    generator = CustomerGenerator(Random(42))

    customers = list(generator.generate(100))

    assert all(
        "@" in customer.email
        and customer.email.endswith(".com")
        for customer in customers
    )

def test_payment_cards_have_valid_format() -> None:
    generator = CustomerGenerator(Random(42))

    customers = list(generator.generate(100))

    pattern = r"^\d{4}-\d{4}-\d{4}-\d{4}$"

    assert all(
        re.match(pattern, customer.payment_card)
        for customer in customers
    )

def test_postcodes_have_six_digits() -> None:
    generator = CustomerGenerator(Random(42))

    customers = list(generator.generate(100))

    assert all(
        len(customer.postcode) == 6
        and customer.postcode.isdigit()
        for customer in customers
    )