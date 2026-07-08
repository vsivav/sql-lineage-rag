"""
CTE Resolver

Extracts Common Table Expressions (CTEs)
from SQLGlot AST.

Current Version
---------------
✓ Detect CTE names
✓ Detect source tables
✓ Detect output columns

Future
------
- Nested CTEs
- Recursive CTEs
- CTE dependency graph
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from sqlglot import exp


@dataclass
class CTEInfo:
    """
    Represents one CTE.
    """

    name: str

    source_tables: List[str] = field(default_factory=list)

    output_columns: List[str] = field(default_factory=list)


class CTEResolver:

    """
    Resolves SQL Server CTEs.
    """

    def resolve(self, statement) -> List[CTEInfo]:

        ctes: List[CTEInfo] = []

        #
        # Find every CTE
        #
        for cte in statement.find_all(exp.CTE):

            info = CTEInfo(

                name=cte.alias_or_name

            )

            #
            # Source tables
            #
            for table in cte.find_all(exp.Table):

                table_name = table.sql()

                if table_name not in info.source_tables:

                    info.source_tables.append(table_name)

            #
            # Output columns
            #
            select = cte.find(exp.Select)

            if select:

                for projection in select.expressions:

                    if projection.alias:

                        info.output_columns.append(

                            projection.alias

                        )

                    elif isinstance(projection, exp.Column):

                        info.output_columns.append(

                            projection.name

                        )

                    else:

                        info.output_columns.append(

                            projection.sql()

                        )

            ctes.append(info)

        return ctes
