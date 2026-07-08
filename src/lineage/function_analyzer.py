"""
Function Analyzer

Extracts SQL functions used in SQL Server procedures.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

from sqlglot import exp


@dataclass
class FunctionUsage:
    """
    Represents one SQL function usage.
    """

    name: str

    expression: str

    arguments: List[str]


class FunctionAnalyzer:

    """
    Finds SQL functions in an AST.
    """

    def analyze(self, statement) -> List[FunctionUsage]:

        functions: List[FunctionUsage] = []

        #
        # Built-in anonymous functions
        #
        for func in statement.find_all(exp.Anonymous):

            functions.append(

                FunctionUsage(

                    name=func.name.upper(),

                    expression=func.sql(),

                    arguments=[
                        arg.sql()
                        for arg in func.expressions
                    ]

                )

            )

        #
        # Aggregate functions
        #
        for aggregate in (

            exp.Sum,
            exp.Avg,
            exp.Min,
            exp.Max,
            exp.Count

        ):

            for func in statement.find_all(aggregate):

                functions.append(

                    FunctionUsage(

                        name=aggregate.__name__.upper(),

                        expression=func.sql(),

                        arguments=[
                            col.sql()
                            for col in func.find_all(exp.Column)
                        ]

                    )

                )

        return functions
