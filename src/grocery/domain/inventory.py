from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class Inventory:
    inventory_id: UUID
    store_id: UUID
    product_id: UUID
    quantity_on_hand: int
    updated_at: datetime