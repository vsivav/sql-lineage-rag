"""
AST Visitor.

Traverses SQLGlot AST and extracts metadata.
"""

from sqlglot import exp

from src.lineage.models import (
    LineageMetadata,
    TableMetadata,
    ColumnMetadata,
    JoinMetadata,
)


class ASTVisitor:

    def visit(self, statements) -> LineageMetadata:

        metadata = LineageMetadata()

        for statement in statements:

            self._extract_tables(statement, metadata)

            self._extract_columns(statement, metadata)

            self._extract_joins(statement, metadata)

        return metadata

    # --------------------------------------------------

    def _extract_tables(self, statement, metadata):

        seen = set()

        for table in statement.find_all(exp.Table):

            key = (
                table.catalog or "",
                table.db or "",
                table.name
            )

            if key in seen:
                continue

            seen.add(key)

            metadata.tables.append(

                TableMetadata(
                    database=table.catalog or "",
                    schema=table.db or "",
                    name=table.name,
                    alias=table.alias or ""
                )

            )

    # --------------------------------------------------

    def _extract_columns(self, statement, metadata):

        seen = set()

        for column in statement.find_all(exp.Column):

            key = (
                column.table or "",
                column.name
            )

            if key in seen:
                continue

            seen.add(key)

            metadata.columns.append(

                ColumnMetadata(
                    table=column.table or "",
                    name=column.name,
                    alias=""
                )

            )

    # --------------------------------------------------

    def _extract_joins(self, statement, metadata):

        for join in statement.find_all(exp.Join):

            metadata.joins.append(

                JoinMetadata(

                    join_type=str(join.args.get("kind") or "JOIN"),

                    right_table=join.this.sql(),

                    condition=(
                        join.args["on"].sql()
                        if join.args.get("on")
                        else ""
                    )

                )

            )
