from src.parser.parser import SQLParser

parser = SQLParser()

metadata = parser.parse_file("tests/sample.sql")

print("\nTables")
for table in metadata.tables:
    print(table)

print("\nColumns")
for column in metadata.columns:
    print(column)

print("\nJoins")
for join in metadata.joins:
    print(join)
