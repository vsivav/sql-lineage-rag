from src.lineage.table_lineage import TableLineageBuilder
from src.lineage.column_lineage import ColumnLineageBuilder
from src.lineage.function_analyzer import FunctionAnalyzer
from src.lineage.cte_resolver import CTEResolver
from src.lineage.subquery_resolver import SubqueryResolver

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

resolver = CTEResolver()

statement = ast[0]

ctes = resolver.resolve(statement)

print("\nCTEs\n")

for cte in ctes:

    print(cte)

resolver = SubqueryResolver()

statement = ast[0]

subqueries = resolver.resolve(statement)

print("\nSUBQUERIES\n")

for subquery in subqueries:

    print(subquery)

