from pathlib import Path


class SQLReader:

    @staticmethod
    def read(file_path: str) -> str:

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(file_path)

        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    @staticmethod
    def read_directory(directory: str):

        directory = Path(directory)

        sql_files = []

        for file in directory.glob("*.sql"):
            sql_files.append(
                (
                    file.name,
                    file.read_text(encoding="utf-8")
                )
            )

        return sql_files
