from collections.abc import Iterator
from random import Random
from uuid import UUID

from grocery.domain.vendor import Vendor
from grocery.reference_data.vendors import VENDOR_NAMES, VENDOR_MODIFIERS
from grocery.reference_data.addresses import CITIES, STREETS
from grocery.reference_data.contacts import EMAIL_PROVIDERS

class VendorGenerator:

    def __init__(self, rng: Random) -> None:
        self._rng = rng
        
    def generate(self, count: int) -> Iterator[Vendor]:
        if count < 0:
            raise ValueError("count must be non-negative")
        
        for _ in range(count):
            vendor_name = f"{self._rng.choice(VENDOR_NAMES)} {self._rng.choice(VENDOR_MODIFIERS)}"
            email_provider = self._rng.choice(EMAIL_PROVIDERS)
            email_salt = self._rng.randint(1, 999)
            email = f"{vendor_name.replace(' ' , '_')}{email_salt}@{email_provider}.com"
            phone = f"+44 {self._generate_digits(9)}"
            city = self._rng.choice(CITIES)
            street = self._rng.choice(STREETS)
            house_number = self._rng.randint(1, 250)
            address = f"{street} {house_number}"


            yield Vendor(
                vendor_id=self._generate_id(),
                name=vendor_name,
                email=email,
                phone=phone,
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

vendor = VendorGenerator(Random(42))
vendors = vendor.generate(250)
for v in vendors:
    print(v.email)