from typing import List, Optional

from pydantic import BaseModel, Field


class TableModel(BaseModel):
    name: str
    schema: Optional[str] = None
    database: Optional[str] = None
    alias: Optional[str] = None


class ColumnModel(BaseModel):
    name: str
    alias: Optional[str] = None
    table: Optional[str] = None
    expression: Optional[str] = None


class JoinModel(BaseModel):
    join_type: str
    left_table: str
    right_table: str
    condition: Optional[str] = None


class CTEModel(BaseModel):
    name: str
    sql: str


class ProcedureModel(BaseModel):
    procedure_name: str = ""

    tables: List[TableModel] = Field(default_factory=list)

    columns: List[ColumnModel] = Field(default_factory=list)

    joins: List[JoinModel] = Field(default_factory=list)

    ctes: List[CTEModel] = Field(default_factory=list)

    raw_sql: str = ""
