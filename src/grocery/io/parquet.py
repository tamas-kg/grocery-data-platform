from collections.abc import Iterable
from dataclasses import asdict
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq


class ParquetWriter:

    def write(
        self,
        records: Iterable[object],
        output_path: Path,
    ) -> None:
        rows = []

        for record in records:
            row = asdict(record)

            for key, value in row.items():
                if hasattr(value, "hex"):
                    row[key] = str(value)

            rows.append(row)

        table = pa.Table.from_pylist(rows)

        output_path.parent.mkdir(parents=True, exist_ok=True)

        pq.write_table(
            table,
            output_path,
        )