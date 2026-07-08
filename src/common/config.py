from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

SRC_DIR = PROJECT_ROOT / "src"

DATA_DIR = PROJECT_ROOT / "data"

SQL_DIR = DATA_DIR / "sql"

OUTPUT_DIR = DATA_DIR / "metadata"

VECTOR_DIR = DATA_DIR / "faiss"

LOG_DIR = PROJECT_ROOT / "logs"

SUPPORTED_DIALECT = "tsql"

DEFAULT_ENCODING = "utf-8"
