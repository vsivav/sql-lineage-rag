"""
Subquery Resolver

Resolves derived tables and nested SELECT statements.

Version 1
---------
✓ Detect derived tables
✓ Capture alias
✓ Source tables
✓ Output columns

Future
------
- Nested subqueries
- Correlated subqueries
- APPLY operators
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from sqlglot import exp


@dataclass
class SubqueryInfo:

    alias: str

    source_tables: List[str] = field(default_factory=list)

    output_columns: List[str] = field(default_factory=list)


class SubqueryResolver:

    """
    Resolves derived tables.

    Example

        FROM
        (
            SELECT ...
        ) s
    """

    def resolve(self, statement) -> List[SubqueryInfo]:

        subqueries: List[SubqueryInfo] = []

        for subquery in statement.find_all(exp.Subquery):

            #
            # Ignore CTE bodies
            #
            if isinstance(subquery.parent, exp.CTE):
                continue

            info = SubqueryInfo(

                alias=subquery.alias_or_name or ""

            )

            #
            # Source tables
            #
            for table in subquery.find_all(exp.Table):

                table_name = table.sql()

                if table_name not in info.source_tables:

                    info.source_tables.append(table_name)

            #
            # Output columns
            #
            select = subquery.find(exp.Select)

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

            subqueries.append(info)

        return subqueries
