from random import Random
from decimal import Decimal
import pytest
import re

from grocery.generation.vendors import VendorGenerator


def test_generation_is_deterministic() -> None:
    generator1 = VendorGenerator(Random(42))
    generator2 = VendorGenerator(Random(42))
    
    vendors_1 = list(generator1.generate(25))
    vendors_2 = list(generator2.generate(25))
    print(vendors_1)

    assert vendors_1 == vendors_2


def test_different_seeds_produce_different_vendors() -> None:
    generator1 = VendorGenerator(Random(42))
    generator2 = VendorGenerator(Random(43))

    vendors_1 = list(generator1.generate(25))
    vendors_2 = list(generator2.generate(25))

    assert vendors_1 != vendors_2


def test_generates_no_vendors_when_count_is_zero() -> None:
    generator = VendorGenerator(Random(42))

    vendors = list(generator.generate(0))

    assert vendors == []


def test_rejects_negative_count() -> None:
    generator = VendorGenerator(Random(42))

    with pytest.raises(ValueError):
        list(generator.generate(-1))


def test_vendor_emails_are_unique() -> None:
    generator = VendorGenerator(Random(42))

    vendors = list(generator.generate(1000))

    emails = [customer.email for customer in vendors]

    assert len(emails) == len(set(emails))


def test_phone_numbers_have_valid_format() -> None:
    generator = VendorGenerator(Random(42))

    vendors = list(generator.generate(100))

    pattern = r"^\+44 \d{9}$"

    assert all(
        re.match(pattern, customer.phone)
        for customer in vendors
    )


def test_emails_have_valid_format() -> None:
    generator = VendorGenerator(Random(42))

    vendors = list(generator.generate(100))

    assert all(
        "@" in customer.email
        and customer.email.endswith(".com")
        for customer in vendors
    )


def test_postcodes_have_six_digits() -> None:
    generator = VendorGenerator(Random(42))

    vendors = list(generator.generate(100))

    assert all(
        len(customer.postcode) == 6
        and customer.postcode.isdigit()
        for customer in vendors
    )