"""
Enterprise SQL Lineage Engine

Coordinates all lineage analyzers.

Pipeline

SQL
 │
 ▼
SQLParser
 │
 ▼
AST
 │
 ├── AliasResolver
 ├── CTEResolver
 ├── SubqueryResolver
 ├── FunctionAnalyzer
 ├── ColumnLineageBuilder
 └── TableLineageBuilder
 │
 ▼
LineageResult
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from sqlglot import exp

from src.lineage.alias_resolver import AliasResolver
from src.lineage.column_lineage import (
    ColumnLineage,
    ColumnLineageBuilder,
)
from src.lineage.cte_resolver import (
    CTEInfo,
    CTEResolver,
)
from src.lineage.function_analyzer import (
    FunctionAnalyzer,
    FunctionUsage,
)
from src.lineage.subquery_resolver import (
    SubqueryInfo,
    SubqueryResolver,
)
from src.lineage.relationship import TableRelationship
from src.lineage.table_lineage import TableLineageBuilder


@dataclass
class LineageResult:

    aliases: dict = field(default_factory=dict)

    table_relationships: List[TableRelationship] = field(default_factory=list)

    column_lineage: List[ColumnLineage] = field(default_factory=list)

    ctes: List[CTEInfo] = field(default_factory=list)

    subqueries: List[SubqueryInfo] = field(default_factory=list)

    functions: List[FunctionUsage] = field(default_factory=list)


class LineageEngine:

    """
    Main orchestration class.
    """

    def __init__(self):

        self.alias_resolver = AliasResolver()

        self.table_builder = TableLineageBuilder()

        self.column_builder = ColumnLineageBuilder()

        self.cte_resolver = CTEResolver()

        self.subquery_resolver = SubqueryResolver()

        self.function_analyzer = FunctionAnalyzer()

    # ---------------------------------------------------

    def analyze(self, statements) -> LineageResult:

        result = LineageResult()

        graph = self.table_builder.build(statements)

        result.table_relationships = graph.relationships()

        for statement in statements:

            result.aliases.update(

                self.alias_resolver.resolve(statement)

            )

            result.column_lineage.extend(

                self.column_builder.build(statement)

            )

            result.ctes.extend(

                self.cte_resolver.resolve(statement)

            )

            result.subqueries.extend(

                self.subquery_resolver.resolve(statement)

            )

            result.functions.extend(

                self.function_analyzer.analyze(statement)

            )

        return result
