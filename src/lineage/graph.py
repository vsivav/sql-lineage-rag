from collections import defaultdict
from typing import Dict, List

from src.lineage.relationship import TableRelationship


class LineageGraph:

    def __init__(self):

        self._graph: Dict[str, List[TableRelationship]] = defaultdict(list)

    def add(self, relationship: TableRelationship):

        self._graph[relationship.source_table].append(
            relationship
        )

    def get_sources(self):

        return self._graph

    def relationships(self):

        result = []

        for values in self._graph.values():

            result.extend(values)

        return result
