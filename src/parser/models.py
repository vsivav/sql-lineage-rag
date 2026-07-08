from dataclasses import dataclass, field
from typing import List


@dataclass
class TableInfo:
    name: str
    alias: str = ""


@dataclass
class JoinInfo:
    left_table: str
    right_table: str
    join_type: str
    condition: str


@dataclass
class ColumnInfo:
    name: str
    alias: str = ""
    expression: str = ""


@dataclass
class CTEInfo:
    name: str
    sql: str


@dataclass
class ProcedureInfo:
    name: str

    tables: List[TableInfo] = field(default_factory=list)

    joins: List[JoinInfo] = field(default_factory=list)

    columns: List[ColumnInfo] = field(default_factory=list)

    ctes: List[CTEInfo] = field(default_factory=list)
