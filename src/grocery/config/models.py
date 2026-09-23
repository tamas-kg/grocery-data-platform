from typing import Literal

from pydantic import BaseModel, Field, model_validator


class SourceConfig(BaseModel):
    source_name: str
    source_type: Literal["file", "jdbc", "api", "kafka"]
    source_format: Literal["parquet", "json", "csv"]
    path_or_table: str
    key_columns: list[str] = Field(min_length=1)
    partition_columns: list[str] | None = None
    schema_ref: str
    watermark_column: str | None = None
    load_type: Literal["full", "incremental", "cdc"]

    @model_validator(mode="after")
    def validate_load_config(self) -> "SourceConfig":
        if self.load_type == "incremental" and not self.watermark_column:
            raise ValueError(
                "watermark_column is required for incremental sources"
            )

        if self.load_type == "cdc" and not self.key_columns:
            raise ValueError(
                "key_columns are required for CDC sources"
            )

        return self