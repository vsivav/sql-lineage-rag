"""
Parser constants.
"""

SQL_DIALECT = "tsql"

SUPPORTED_FILE_TYPES = {
    ".sql",
    ".txt"
}

WRITE_OPERATIONS = {
    "INSERT",
    "UPDATE",
    "DELETE",
    "MERGE"
}

READ_OPERATIONS = {
    "SELECT"
}

JOIN_TYPES = {
    "JOIN",
    "INNER JOIN",
    "LEFT JOIN",
    "RIGHT JOIN",
    "FULL JOIN",
    "CROSS JOIN"
}

AGGREGATE_FUNCTIONS = {
    "SUM",
    "AVG",
    "COUNT",
    "MIN",
    "MAX"
}

WINDOW_FUNCTIONS = {
    "ROW_NUMBER",
    "RANK",
    "DENSE_RANK",
    "LAG",
    "LEAD",
    "FIRST_VALUE",
    "LAST_VALUE"
}
