"""
Lineage Metadata Models
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class TableMetadata:
    name: str
    alias: str = ""
    database: str = ""
    schema: str = ""


@dataclass
class ColumnMetadata:
    name: str
    table: str = ""
    alias: str = ""
    expression: str = ""


@dataclass
class JoinMetadata:
    join_type: str
    left_table: str
    right_table: str
    condition: str


@dataclass
class CTEMetadata:
    name: str


@dataclass
class FunctionMetadata:
    name: str
    expression: str


@dataclass
class OutputColumn:
    name: str
    expression: str


@dataclass
class LineageMetadata:

    tables: List[TableMetadata] = field(default_factory=list)

    columns: List[ColumnMetadata] = field(default_factory=list)

    joins: List[JoinMetadata] = field(default_factory=list)

    ctes: List[CTEMetadata] = field(default_factory=list)

    functions: List[FunctionMetadata] = field(default_factory=list)

    output_columns: List[OutputColumn] = field(default_factory=list)
