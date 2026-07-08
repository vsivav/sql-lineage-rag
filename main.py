from src.parser.parser import SQLParser

parser = SQLParser()

result = parser.parse_file("tests/sample.sql")

print()

print("TABLES")

print(result["metadata"]["tables"])

print()

print("COLUMNS")

print(result["metadata"]["columns"])
