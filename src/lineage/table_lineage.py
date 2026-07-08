from sqlglot import exp

from src.lineage.graph import LineageGraph
from src.lineage.relationship import TableRelationship


class TableLineageBuilder:
    """
    Builds table-level lineage from SQLGlot AST.
    """

    def build(self, statements):

        graph = LineageGraph()

        for statement in statements:

            target_table = self._find_target_table(statement)

            if target_table is None:
                continue

            source_tables = []

            for table in statement.find_all(exp.Table):

                table_name = table.sql()

                if table_name != target_table:
                    source_tables.append(table_name)

            for source in sorted(set(source_tables)):

                graph.add(

                    TableRelationship(

                        source_table=source,

                        target_table=target_table,

                        operation=statement.key.upper()
                    )

                )

        return graph

    def _find_target_table(self, statement):

        if isinstance(statement, exp.Insert):
            return statement.this.sql()

        if isinstance(statement, exp.Update):
            return statement.this.sql()

        if isinstance(statement, exp.Delete):
            return statement.this.sql()

        if isinstance(statement, exp.Merge):
            return statement.this.sql()

        return None
