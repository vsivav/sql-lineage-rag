from sqlglot import parse_one

from src.lineage.alias_resolver import AliasResolver


def test_alias_resolution():

    sql = """

    SELECT

        c.CustomerID,

        o.Amount

    FROM dbo.Customers c

    JOIN dbo.Orders o

        ON c.CustomerID=o.CustomerID

    """

    statement = parse_one(sql, read="tsql")

    resolver = AliasResolver()

    aliases = resolver.resolve(statement)

    assert aliases["c"] == "dbo.Customers AS c"

    assert aliases["o"] == "dbo.Orders AS o"
