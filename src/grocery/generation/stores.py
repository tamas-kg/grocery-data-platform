from collections.abc import Iterator
from random import Random
from uuid import UUID

from grocery.domain.store import Store
from grocery.reference_data.stores import STORE_NAMES, STORE_SIZES
from grocery.reference_data.addresses import CITIES, STREETS

class StoreGenerator:

    def __init__(self, rng: Random) -> None:
        self._rng = rng
        
    def generate(self, count: int) -> Iterator[Store]:
        if count < 0:
            raise ValueError("count must be non-negative")
        
        for _ in range(count):
            store_name = self._rng.choice(STORE_NAMES)
            store_size = self._rng.choice(STORE_SIZES)
            city = self._rng.choice(CITIES)
            street = self._rng.choice(STREETS)
            house_number = self._rng.randint(1, 250)
            address = f"{street} {house_number}"


            yield Store(
                store_id=self._generate_id(),
                name=store_name,
                size=store_size,
                city=city,
                postcode=self._generate_digits(6),
                address=address,
            )

    def _generate_id(self) -> UUID:
        return UUID(
            int=self._rng.getrandbits(128),
            version=4,
        )

    def _generate_digits(self, n:int) -> str:
        return ''.join(str(self._rng.randint(0, 9)) for _ in range(n))