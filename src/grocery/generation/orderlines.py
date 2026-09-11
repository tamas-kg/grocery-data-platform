from collections.abc import Iterator, Sequence, Mapping
from decimal import Decimal
from random import Random
from uuid import UUID

from grocery.domain.orderline import OrderLine

class OrderLineGenerator:

    def __init__(
        self,
        rng: Random,
        order_ids: Sequence[UUID],
        product_prices: Mapping[UUID, Decimal],
    ) -> None:
        self._rng = rng
        self._order_ids = order_ids
        self._product_prices = product_prices


    def generate(self, count: int) -> Iterator[OrderLine]:
        if count < 0:
            raise ValueError("count must be non-negative")

        if not self._order_ids:
            raise ValueError("order_ids must not be empty")

        if not self._product_prices:
            raise ValueError("product_prices must not be empty")
        
        for _ in range(count):
            product_id = self._rng.choice(list(self._product_prices))

            yield OrderLine(
                order_line_id=self._generate_id(),
                order_id=self._rng.choice(self._order_ids),
                product_id=product_id,
                quantity=self._rng.randint(1, 10),
                unit_price=self._product_prices[product_id],
            )

    def _generate_id(self) -> UUID:
        return UUID(
            int=self._rng.getrandbits(128),
            version=4,
        )