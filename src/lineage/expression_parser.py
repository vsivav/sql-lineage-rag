"""
Expression Parser

Analyzes SQLGlot expressions and classifies
column transformations.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import List

from sqlglot import exp


# ----------------------------------------------------
# Expression Types
# ----------------------------------------------------

class ExpressionType(str, Enum):

    DIRECT = "DIRECT"

    AGGREGATE = "AGGREGATE"

    CONDITIONAL = "CONDITIONAL"

    NULL_HANDLING = "NULL_HANDLING"

    TYPE_CONVERSION = "TYPE_CONVERSION"

    WINDOW = "WINDOW"

    ARITHMETIC = "ARITHMETIC"

    FUNCTION = "FUNCTION"

    UNKNOWN = "UNKNOWN"


# ----------------------------------------------------

@dataclass
class ExpressionMetadata:

    expression: str

    expression_type: ExpressionType

    source_columns: List[str]


# ----------------------------------------------------

class ExpressionParser:

    """
    Classifies SQL expressions.
    """

    # ------------------------------------------------

    def parse(self, expression) -> ExpressionMetadata:

        expression_type = self._classify(expression)

        columns = [

            column.sql()

            for column in expression.find_all(exp.Column)

        ]

        return ExpressionMetadata(

            expression=expression.sql(),

            expression_type=expression_type,

            source_columns=columns

        )

    # ------------------------------------------------

    def _classify(self, expression) -> ExpressionType:

        #
        # CASE
        #
        if isinstance(expression, exp.Case):

            return ExpressionType.CONDITIONAL

        #
        # CAST
        #
        if isinstance(expression, exp.Cast):

            return ExpressionType.TYPE_CONVERSION

        #
        # Window functions
        #
        if isinstance(expression, exp.Window):

            return ExpressionType.WINDOW

        #
        # Arithmetic
        #
        if isinstance(
            expression,
            (
                exp.Add,
                exp.Sub,
                exp.Mul,
                exp.Div
            )
        ):

            return ExpressionType.ARITHMETIC

        #
        # Function
        #
        if isinstance(expression, exp.Anonymous):

            name = expression.name.upper()

            if name in ("ISNULL", "COALESCE"):

                return ExpressionType.NULL_HANDLING

            if name in (

                "SUM",

                "AVG",

                "COUNT",

                "MIN",

                "MAX"

            ):

                return ExpressionType.AGGREGATE

            return ExpressionType.FUNCTION

        #
        # Direct column
        #
        if isinstance(expression, exp.Column):

            return ExpressionType.DIRECT

        return ExpressionType.UNKNOWN
