"""
Alias Resolver

Responsible for resolving SQL table aliases.

Example

FROM dbo.Customer c

Returns

{
    "c": "dbo.Customer"
}
"""

from __future__ import annotations

from typing import Dict

from sqlglot import exp


class AliasResolver:
    """
    Builds alias → table mappings.

    Example

        Customer c

    becomes

        {
            "c":"dbo.Customer"
        }
    """

    def __init__(self):

        self.alias_map: Dict[str, str] = {}

    # -----------------------------------------------------

    def resolve(self, statement) -> Dict[str, str]:
        """
        Resolve aliases for a statement.
        """

        self.alias_map.clear()

        for table in statement.find_all(exp.Table):

            alias = table.alias

            table_name = table.sql()

            if alias:

                self.alias_map[alias] = table_name

            else:

                #
                # Self reference
                #
                self.alias_map[table.name] = table_name

        return dict(self.alias_map)

    # -----------------------------------------------------

    def table_for_alias(self, alias: str):

        return self.alias_map.get(alias)

    # -----------------------------------------------------

    def has_alias(self, alias: str):

        return alias in self.alias_map

    # -----------------------------------------------------

    def __len__(self):

        return len(self.alias_map)

    # -----------------------------------------------------

    def __repr__(self):

        return str(self.alias_map)
