"""
Metadata schema used for JSON generation.
"""

from typing import List
from pydantic import BaseModel, Field


class ColumnMetadata(BaseModel):
    target_column: str
    source_columns: List[str] = Field(default_factory=list)
    transformation: str = ""


class ProcedureMetadata(BaseModel):
    procedure_name: str

    source_tables: List[str] = Field(default_factory=list)

    target_tables: List[str] = Field(default_factory=list)

    columns: List[ColumnMetadata] = Field(default_factory=list)

    functions: List[str] = Field(default_factory=list)
