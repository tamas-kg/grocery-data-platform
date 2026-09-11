from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID


@dataclass(frozen=True, slots=True)
class Order:
    order_id: UUID
    customer_id: UUID
    store_id: UUID
    order_timestamp: datetime
    status: str