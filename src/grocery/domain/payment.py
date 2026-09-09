from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID


@dataclass(frozen=True)
class Payment:
    payment_id: UUID
    order_id: UUID
    amount: Decimal
    payment_method: str
    status: str
    payment_timestamp: datetime