from dataclasses import dataclass
from pathlib import Path
from datetime import datetime


@dataclass(frozen=True, slots=True)
class GenerationConfig:
    seed: int
    output_dir: Path

    vendor_count: int
    customer_count: int
    store_count: int
    product_count: int
    order_count: int
    order_line_count: int
    order_start_timestamp: datetime
    order_end_timestamp: datetime