from src.parser.parser import SQLParser

if __name__ == "__main__":

    parser = SQLParser()

    ast = parser.parse_file("tests/sample.sql")

    print("=" * 80)

    print("Statements Parsed :", len(ast))

    print("=" * 80)

    for statement in ast:

        print(statement)

        print("-" * 80)
