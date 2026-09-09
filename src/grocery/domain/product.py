from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID


@dataclass(frozen=True, slots=True)
class Product:
    product_id: UUID
    vendor_id: UUID
    name: str
    category: str
    brand: str
    unit_cost: Decimal
    unit_price: Decimal
