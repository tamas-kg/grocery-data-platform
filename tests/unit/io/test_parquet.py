from datetime import datetime
from decimal import Decimal
from pathlib import Path
from uuid import UUID

import pyarrow.parquet as pq
import pytest

from grocery.domain.product import Product
from grocery.io.parquet import ParquetWriter
from grocery.io.schemas import PRODUCT_SCHEMA


FIXED_TIMESTAMP = datetime(2026, 9, 14, 12, 30, 45)


def fixed_clock() -> datetime:
    return FIXED_TIMESTAMP


def make_product(product_number: int = 1) -> Product:
    return Product(
        product_id=UUID(
            f"550e8400-e29b-41d4-a716-4466554400{product_number:02d}"
        ),
        vendor_id=UUID(
            "550e8400-e29b-41d4-a716-446655440000"
        ),
        category="Dairy",
        name="Milk",
        brand="FreshMart",
        unit_cost=Decimal("1.50"),
        unit_price=Decimal("2.00"),
    )


def get_output_file(tmp_path: Path) -> Path:
    files = list(tmp_path.glob("products_*.parquet"))

    assert len(files) == 1

    return files[0]


def test_writes_expected_number_of_records(tmp_path: Path) -> None:
    writer = ParquetWriter(
        schema=PRODUCT_SCHEMA,
        chunk_size=2,
        clock=fixed_clock,
    )

    records = [
        make_product(1),
        make_product(2),
        make_product(3),
    ]

    writer.write(
        records,
        tmp_path / "products.parquet",
    )

    table = pq.read_table(get_output_file(tmp_path))

    assert table.num_rows == 3


def test_writes_records_across_multiple_chunks(
    tmp_path: Path,
) -> None:
    writer = ParquetWriter(
        schema=PRODUCT_SCHEMA,
        chunk_size=2,
        clock=fixed_clock,
    )

    records = [
        make_product(1),
        make_product(2),
        make_product(3),
        make_product(4),
        make_product(5),
    ]

    writer.write(
        records,
        tmp_path / "products.parquet",
    )

    table = pq.read_table(get_output_file(tmp_path))

    assert table.num_rows == 5


def test_preserves_schema(tmp_path: Path) -> None:
    writer = ParquetWriter(
        schema=PRODUCT_SCHEMA,
        clock=fixed_clock,
    )

    writer.write(
        [make_product()],
        tmp_path / "products.parquet",
    )

    table = pq.read_table(get_output_file(tmp_path))

    assert table.schema == PRODUCT_SCHEMA


def test_serializes_uuid_as_string(
    tmp_path: Path,
) -> None:
    product = make_product()

    writer = ParquetWriter(
        schema=PRODUCT_SCHEMA,
        clock=fixed_clock,
    )

    writer.write(
        [product],
        tmp_path / "products.parquet",
    )

    table = pq.read_table(get_output_file(tmp_path))

    assert table["product_id"].to_pylist() == [
        str(product.product_id)
    ]


def test_preserves_decimal_values(
    tmp_path: Path,
) -> None:
    product = make_product()

    writer = ParquetWriter(
        schema=PRODUCT_SCHEMA,
        clock=fixed_clock,
    )

    writer.write(
        [product],
        tmp_path / "products.parquet",
    )

    table = pq.read_table(get_output_file(tmp_path))

    assert table["unit_cost"].to_pylist() == [
        Decimal("1.50")
    ]

    assert table["unit_price"].to_pylist() == [
        Decimal("2.00")
    ]


def test_creates_parent_directories(
    tmp_path: Path,
) -> None:
    output_path = (
        tmp_path
        / "nested"
        / "data"
        / "products.parquet"
    )

    writer = ParquetWriter(
        schema=PRODUCT_SCHEMA,
        clock=fixed_clock,
    )

    writer.write(
        [make_product()],
        output_path,
    )

    assert (
        tmp_path
        / "nested"
        / "data"
        / "products_20260914T123045.parquet"
    ).exists()


def test_filename_contains_generation_timestamp(
    tmp_path: Path,
) -> None:
    writer = ParquetWriter(
        schema=PRODUCT_SCHEMA,
        clock=fixed_clock,
    )

    writer.write(
        [make_product()],
        tmp_path / "products.parquet",
    )

    expected = (
        tmp_path
        / "products_20260914T123045.parquet"
    )

    assert expected.exists()


def test_empty_input_does_not_create_file(
    tmp_path: Path,
) -> None:
    writer = ParquetWriter(
        schema=PRODUCT_SCHEMA,
        clock=fixed_clock,
    )

    writer.write(
        [],
        tmp_path / "products.parquet",
    )

    assert list(tmp_path.glob("products_*.parquet")) == []


def test_consumes_iterator(
    tmp_path: Path,
) -> None:
    consumed = 0

    def records():
        nonlocal consumed

        for number in range(5):
            consumed += 1
            yield make_product(number + 1)

    writer = ParquetWriter(
        schema=PRODUCT_SCHEMA,
        chunk_size=2,
        clock=fixed_clock,
    )

    writer.write(
        records(),
        tmp_path / "products.parquet",
    )

    assert consumed == 5


def test_rejects_invalid_chunk_size() -> None:
    with pytest.raises(ValueError):
        ParquetWriter(
            schema=PRODUCT_SCHEMA,
            chunk_size=0,
        )

    with pytest.raises(ValueError):
        ParquetWriter(
            schema=PRODUCT_SCHEMA,
            chunk_size=-1,
        )