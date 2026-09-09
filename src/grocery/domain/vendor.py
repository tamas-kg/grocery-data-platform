from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class Vendor:
    vendor_id: UUID
    name: str
    email: str
    phone: str
    city: str
    postcode: str
    address: str