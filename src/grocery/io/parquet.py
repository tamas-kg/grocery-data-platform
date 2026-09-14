import logging
from collections.abc import Iterable
from typing import Callable
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from uuid import UUID

import pyarrow as pa
import pyarrow.parquet as pq


logger = logging.getLogger(__name__)


class ParquetWriter:

    def __init__(self, 
                 schema: pa.Schema,
                 chunk_size: int = 10_000,
                 clock: Callable[[], datetime] = datetime.now
                 ) -> None:
        if chunk_size <= 0:
            raise ValueError("chunk_size must be positive")

        self._schema = schema
        self._chunk_size = chunk_size
        self._clock = clock

    def write(
        self,
        records: Iterable[object],
        output_path: Path,
    ) -> None:
        output_path = self._add_timestamp(output_path)

        logger.info("Writing parquet file: %s", output_path)

        iterator = iter(records)

        try:
            first_record = next(iterator)
        except StopIteration:
            logger.warning(
                "No records to write: %s",
                output_path,
            )
            return

        writer: pq.ParquetWriter | None = None
        rows: list[dict[str, object]] = []
        records_written = 0

        try:
            rows.append(self._to_row(first_record))

            for record in iterator:
                rows.append(self._to_row(record))

                if len(rows) >= self._chunk_size:
                    writer = self._write_chunk(
                        rows,
                        output_path,
                        writer,
                    )

                    records_written += len(rows)
                    rows = []

            if rows:
                writer = self._write_chunk(
                    rows,
                    output_path,
                    writer,
                )

                records_written += len(rows)

        finally:
            if writer is not None:
                writer.close()

        logger.info(
            "Finished writing %d records to %s",
            records_written,
            output_path,
        )

    def _write_chunk(
        self,
        rows: list[dict[str, object]],
        output_path: Path,
        writer: pq.ParquetWriter | None,
    ) -> pq.ParquetWriter:
        table = pa.Table.from_pylist(rows, schema=self._schema)

        if writer is None:
            output_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            writer = pq.ParquetWriter(
                output_path,
                self._schema
            )

        writer.write_table(table)

        logger.debug(
            "Wrote parquet chunk containing %d records",
            len(rows),
        )

        return writer

    @staticmethod
    def _to_row(record: object) -> dict[str, object]:
        row = asdict(record)

        for key, value in row.items():
            if isinstance(value, UUID):
                row[key] = str(value)

        return row

    def _add_timestamp(self, output_path: Path) -> Path:
        timestamp = self._clock().strftime("%Y%m%dT%H%M%S")

        return output_path.with_name(
            f"{output_path.stem}_{timestamp}{output_path.suffix}"
        )