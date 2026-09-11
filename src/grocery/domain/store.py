from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class Store:
    store_id: UUID
    name: str
    size: str
    city: str
    postcode: str
    address: str
    