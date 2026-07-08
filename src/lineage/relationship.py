from dataclasses import dataclass


@dataclass(frozen=True)
class TableRelationship:
    """
    Represents a lineage relationship between two tables.
    """

    source_table: str
    target_table: str
    operation: str
