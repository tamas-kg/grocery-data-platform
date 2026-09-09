from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID


@dataclass(frozen=True)
class OrderItem:
    order_item_id: UUID
    order_id: UUID
    product_id: UUID
    quantity: int
    unit_price: Decimal