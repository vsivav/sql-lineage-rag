from src.lineage.table_lineage import TableLineageBuilder

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
