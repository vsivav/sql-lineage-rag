from pathlib import Path

BASE_DIR = Path(__file__).parent

DATA_DIR = BASE_DIR / "data"

SQL_DIR = DATA_DIR / "sql"

OUTPUT_DIR = DATA_DIR / "metadata"

LOG_LEVEL = "INFO"

SUPPORTED_DIALECT = "tsql"
