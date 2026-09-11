from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class Customer:
    customer_id: UUID
    first_name: str
    last_name: str
    email: str
    phone: str
    city: str
    postcode: str
    address: str
    payment_card: str