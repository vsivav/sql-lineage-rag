"""
Column Lineage Builder

Builds source-to-target column mappings from SQLGlot AST.

Current scope (v1)
------------------
✔ SELECT
✔ INSERT ... SELECT
✔ Aliases
✔ Basic expressions

Future versions
---------------
- MERGE
- UPDATE ... FROM
- DELETE
- CTE chains
- Window functions
- CASE
- Dynamic SQL
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from sqlglot import exp

from src.lineage.alias_resolver import AliasResolver
from src.lineage.expression_parser import ExpressionParser

# ----------------------------------------------------------
# Models
# ----------------------------------------------------------

@dataclass
class ColumnLineage:

    source_table: str

    source_column: str

    target_table: str = ""

    target_column: str = ""

    expression: str = ""


# ----------------------------------------------------------
# Builder
# ----------------------------------------------------------

class ColumnLineageBuilder:

    def __init__(self):

        self.alias_resolver = AliasResolver()

    # ------------------------------------------------------

    def build(self, statement) -> List[ColumnLineage]:

        """
        Build lineage for a SQLGlot statement.
        """

        aliases = self.alias_resolver.resolve(statement)

        lineage: List[ColumnLineage] = []

        #
        # Find SELECT projection
        #
        select = statement.find(exp.Select)

        if select is None:
            return lineage

        for projection in select.expressions:

            lineage.extend(
                self._projection_lineage(
                    projection,
                    aliases
                )
            )

        return lineage

    # ------------------------------------------------------

    def _projection_lineage(
        self,
        projection,
        aliases
    ) -> List[ColumnLineage]:

        rows = []

        #
        # Find every referenced column
        #
        columns = list(
            projection.find_all(exp.Column)
        )

        #
        # Output column name
        #
        if projection.alias:

            target_name = projection.alias

        elif isinstance(projection, exp.Column):

            target_name = projection.name

        else:

            target_name = projection.sql()

        #
        # Expression text
        #
        self.expression_parser = ExpressionParser()
        metadata = self.expression_parser.parse(projection)
        expression = metadata.expression

        #
        # Create lineage
        #
        for column in columns:

            alias = column.table

            table = aliases.get(alias, alias)

            rows.append(

                ColumnLineage(

                    source_table=table,

                    source_column=column.name,

                    target_column=target_name,

                    expression=expression

                )

            )

        return rows
