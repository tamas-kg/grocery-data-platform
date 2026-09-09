from collections.abc import Iterator
from random import Random
from uuid import UUID

from grocery.domain.customer import Customer
from grocery.reference_data.names import FIRST_NAMES, LAST_NAMES
from grocery.reference_data.addresses import CITIES, STREETS
from grocery.reference_data.contacts import EMAIL_PROVIDERS

class CustomerGenerator:

    def __init__(self, rng: Random) -> None:
        self._rng = rng
        
    def generate(self, count: int) -> Iterator[Customer]:
        if count < 0:
            raise ValueError("count must be non-negative")
        
        for _ in range(count):
            first_name = self._rng.choice(FIRST_NAMES)
            last_name = self._rng.choice(LAST_NAMES)
            email_provider = self._rng.choice(EMAIL_PROVIDERS)
            email_salt = self._rng.randint(1, 999)
            email = f"{first_name}.{last_name}{email_salt}@{email_provider}.com"
            phone = f"+44 {self._generate_digits(9)}"
            city = self._rng.choice(CITIES)
            street = self._rng.choice(STREETS)
            house_number = self._rng.randint(1, 250)
            address = f"{street} {house_number}"
            card_number = '-'.join(''.join(str(self._rng.randint(0, 9)) for _ in range(4)) for _ in range(4))


            yield Customer(
                customer_id=self._generate_id(),
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                city=city,
                postcode=self._generate_digits(6),
                address=address,
                payment_card=card_number
            )

    def _generate_id(self) -> UUID:
        return UUID(
            int=self._rng.getrandbits(128),
            version=4,
        )

    def _generate_digits(self, n:int) -> str:
        return ''.join(str(self._rng.randint(0, 9)) for _ in range(n))

