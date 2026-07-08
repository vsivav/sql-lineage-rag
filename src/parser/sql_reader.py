from pathlib import Path

from src.common.logger import logger


class SQLReader:
    """
    Reads SQL files.
    """

    @staticmethod
    def read(path: str) -> str:
        file_path = Path(path)

        logger.info(f"Reading {file_path}")

        if not file_path.exists():
            raise FileNotFoundError(file_path)

        return file_path.read_text(encoding="utf-8")

    @staticmethod
    def list_sql(directory: str):
        root = Path(directory)

        return sorted(root.glob("*.sql"))
