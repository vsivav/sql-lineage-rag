import hashlib


def generate_hash(text: str) -> str:
    """
    Generates a stable SHA-256 hash for SQL text.
    """
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def normalize_sql(sql: str) -> str:
    """
    Basic SQL normalization.

    Full formatting will be added in a later module.
    """
    return " ".join(sql.split())
