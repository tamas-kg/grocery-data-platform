from collections.abc import Iterator, Sequence
from datetime import datetime, timedelta
from random import Random
from uuid import UUID

from grocery.domain.order import Order
from grocery.reference_data.orders import ORDER_STATUSES

class OrderGenerator:

    def __init__(
        self,
        rng: Random,
        customer_ids: Sequence[UUID],
        store_ids: Sequence[UUID],
        start_timestamp: datetime,
        end_timestamp: datetime
    ) -> None:
        self._rng = rng
        self._customer_ids = customer_ids
        self._store_ids = store_ids
        self._start_timestamp = start_timestamp
        self._end_timestamp = end_timestamp



    def generate(self, count: int) -> Iterator[Order]:
        if count < 0:
            raise ValueError("count must be non-negative")

        if not self._customer_ids:
            raise ValueError("customer_ids must not be empty")

        if not self._store_ids:
            raise ValueError("store_ids must not be empty")

        if self._start_timestamp >= self._end_timestamp:
            raise ValueError(
                "start_timestamp must be before end_timestamp"
            )

        time_range_seconds = int(
            (self._end_timestamp - self._start_timestamp).total_seconds()
        )
        
        for _ in range(count):

            random_timestamp = self._start_timestamp + timedelta(
                seconds=self._rng.randint(0, time_range_seconds)
            )


            yield Order(
                order_id=self._generate_id(),
                customer_id=self._rng.choice(self._customer_ids),
                store_id=self._rng.choice(self._store_ids),
                order_timestamp=random_timestamp,
                status=self._rng.choice(ORDER_STATUSES),
            )

    def _generate_id(self) -> UUID:
        return UUID(
            int=self._rng.getrandbits(128),
            version=4,
        )