"""
Dependency Graph

Maintains table and column lineage relationships.

This graph will later support:

- Upstream lineage
- Downstream lineage
- Impact analysis
- RAG metadata generation
"""

from __future__ import annotations

from dataclasses import dataclass, field
from collections import defaultdict
from typing import Dict, List, Set


# --------------------------------------------------------
# Models
# --------------------------------------------------------

@dataclass(frozen=True)
class LineageNode:
    """
    Represents one table.column.
    """

    table: str
    column: str

    @property
    def id(self) -> str:
        return f"{self.table}.{self.column}"


@dataclass
class LineageEdge:
    """
    Source → Target relationship.
    """

    source: LineageNode
    target: LineageNode
    expression: str = ""


# --------------------------------------------------------
# Graph
# --------------------------------------------------------

class DependencyGraph:

    def __init__(self):

        self.forward: Dict[str, List[LineageEdge]] = defaultdict(list)

        self.reverse: Dict[str, List[LineageEdge]] = defaultdict(list)

        self.nodes: Dict[str, LineageNode] = {}

    # ----------------------------------------------------

    def add_edge(
        self,
        source_table: str,
        source_column: str,
        target_table: str,
        target_column: str,
        expression: str = ""
    ):

        source = LineageNode(
            source_table,
            source_column
        )

        target = LineageNode(
            target_table,
            target_column
        )

        self.nodes[source.id] = source
        self.nodes[target.id] = target

        edge = LineageEdge(
            source=source,
            target=target,
            expression=expression
        )

        self.forward[source.id].append(edge)

        self.reverse[target.id].append(edge)

    # ----------------------------------------------------

    def downstream(
        self,
        table: str,
        column: str
    ) -> List[LineageNode]:

        node_id = f"{table}.{column}"

        return [

            edge.target

            for edge in self.forward.get(node_id, [])

        ]

    # ----------------------------------------------------

    def upstream(
        self,
        table: str,
        column: str
    ) -> List[LineageNode]:

        node_id = f"{table}.{column}"

        return [

            edge.source

            for edge in self.reverse.get(node_id, [])

        ]

    # ----------------------------------------------------

    def all_nodes(self):

        return list(self.nodes.values())

    # ----------------------------------------------------

    def all_edges(self):

        edges = []

        for value in self.forward.values():

            edges.extend(value)

        return edges
