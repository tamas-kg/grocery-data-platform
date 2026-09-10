from random import Random
import pytest

from grocery.generation.stores import StoreGenerator

def test_generation_is_deterministic() -> None:
    generator1 = StoreGenerator(Random(42))
    generator2 = StoreGenerator(Random(42))
    
    stores_1 = list(generator1.generate(25))
    stores_2 = list(generator2.generate(25))
    print(stores_1)

    assert stores_1 == stores_2

def test_different_seeds_produce_different_stores() -> None:
    generator1 = StoreGenerator(Random(42))
    generator2 = StoreGenerator(Random(43))

    stores_1 = list(generator1.generate(25))
    stores_2 = list(generator2.generate(25))

    assert stores_1 != stores_2

def test_generates_no_stores_when_count_is_zero() -> None:
    generator = StoreGenerator(Random(42))

    stores = list(generator.generate(0))

    assert stores == []

def test_rejects_negative_count() -> None:
    generator = StoreGenerator(Random(42))

    with pytest.raises(ValueError):
        list(generator.generate(-1))

def test_postcodes_have_six_digits() -> None:
    generator = StoreGenerator(Random(42))

    stores = list(generator.generate(100))

    assert all(
        len(customer.postcode) == 6
        and customer.postcode.isdigit()
        for customer in stores
    )