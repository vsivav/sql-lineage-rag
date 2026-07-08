"""
src/parser/parser.py

Basic SQL Parser using SQLGlot.

Step 1 Goals
------------
- Read SQL text
- Parse SQL Server SQL
- Return SQLGlot AST
- Provide simple validation

Author:
SQL Lineage RAG
"""

from __future__ import annotations

from pathlib import Path
from typing import List, Union

import sqlglot
from sqlglot import exp
from sqlglot.errors import ParseError

from src.common.logger import logger
from src.common.exceptions import SQLParseException
from src.parser.constants import SQL_DIALECT
from src.parser.sql_reader import SQLReader
from src.parser.ast_visitor import ASTVisitor


class SQLParser:
    """
    Wrapper around sqlglot.

    Example
    -------
    parser = SQLParser()

    ast = parser.parse_file("sample.sql")
    """

    def __init__(self, dialect: str = SQL_DIALECT):
        self.dialect = dialect

    # --------------------------------------------------
    # Public API
    # --------------------------------------------------

    def parse_file(self, file_path: Union[str, Path]) -> List[exp.Expression]:
        """
        Read and parse a SQL file.

        Returns
        -------
        list[Expression]
        """

        logger.info(f"Reading SQL file: {file_path}")

        sql = SQLReader.read(str(file_path))

        return self.parse_sql(sql)

    def parse_sql(self, sql: str) -> List[exp.Expression]:
        """
        Parse SQL text into SQLGlot AST.

        Parameters
        ----------
        sql : str

        Returns
        -------
        list[Expression]
        """

        sql = self._normalize(sql)

        try:

            ast = sqlglot.parse(
                sql,
                read=self.dialect
            )

        except ParseError as ex:

            logger.exception(ex)

            raise SQLParseException(str(ex))

        logger.info(f"Successfully parsed {len(ast)} SQL statement(s).")

        return ast

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    @staticmethod
    def _normalize(sql: str) -> str:
        """
        Basic SQL normalization.
        """

        sql = sql.replace("\r\n", "\n")
        sql = sql.replace("\t", " ")

        return sql.strip()
