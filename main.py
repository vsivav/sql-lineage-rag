from src.lineage.table_lineage import TableLineageBuilder
from src.lineage.column_lineage import ColumnLineageBuilder
from src.lineage.function_analyzer import FunctionAnalyzer

parser = SQLParser()

ast = parser.parse_file("tests/sample.sql")

builder = TableLineageBuilder()

graph = builder.build(ast)

print("\nTABLE LINEAGE\n")

for relationship in graph.relationships():

    print(
        relationship.source_table,
        " ---> ",
        relationship.target_table,
        "(",
        relationship.operation,
        ")"
    )

builder = ColumnLineageBuilder()

statement = parser.parse_file("tests/sample.sql")[0]

lineage = builder.build(statement)

print()

print("COLUMN LINEAGE")

for row in lineage:

    print(row)

analyzer = FunctionAnalyzer()

statement = ast[0]

functions = analyzer.analyze(statement)

print("\nFUNCTIONS\n")

for func in functions:

    print(func)
