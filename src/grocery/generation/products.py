from collections.abc import Iterator
from decimal import Decimal
from random import Random
from uuid import UUID

from grocery.domain.product import Product
from grocery.reference_data.products import CATEGORIES, BRANDS

class ProductGenerator:

    def __init__(self, rng: Random) -> None:
        self._rng = rng

    def generate(self, count: int) -> Iterator[Product]:
        if count < 0:
            raise ValueError("count must be non-negative")
        
        for _ in range(count):
            category = self._rng.choice(list(CATEGORIES))
            name = self._rng.choice(CATEGORIES[category])
            brand = self._rng.choice(BRANDS)

            cost_cents = self._rng.randint(50, 1000)
            margin_cents = self._rng.randint(10, 500)

            yield Product(
                product_id=self._generate_id(),
                vendor_id="",
                category=category,
                name=name,
                brand=brand,
                unit_cost=Decimal(cost_cents) / Decimal(100),
                unit_price=Decimal(cost_cents + margin_cents) / Decimal(100),
            )

    def _generate_id(self) -> UUID:
        return UUID(
            int=self._rng.getrandbits(128),
            version=4,
        )