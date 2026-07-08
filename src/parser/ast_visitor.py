"""
AST Visitor

Walks the SQLGlot AST and extracts metadata.
"""

from sqlglot import exp


class ASTVisitor:

    def __init__(self):

        self.tables = []
        self.columns = []

    # --------------------------------------------------

    def visit(self, statements):

        """
        Visit every parsed statement.
        """

        for statement in statements:

            self._extract_tables(statement)

            self._extract_columns(statement)

        return {
            "tables": sorted(set(self.tables)),
            "columns": sorted(set(self.columns))
        }

    # --------------------------------------------------

    def _extract_tables(self, statement):

        """
        Extract table names.
        """

        for table in statement.find_all(exp.Table):

            self.tables.append(table.sql())

    # --------------------------------------------------

    def _extract_columns(self, statement):

        """
        Extract referenced columns.
        """

        for column in statement.find_all(exp.Column):

            self.columns.append(column.name)
