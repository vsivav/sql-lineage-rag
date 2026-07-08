class SQLLineageException(Exception):
    """Base exception for the project."""


class SQLParseException(SQLLineageException):
    """Raised when SQL parsing fails."""


class UnsupportedDialectException(SQLLineageException):
    """Raised when an unsupported SQL dialect is encountered."""


class MetadataGenerationException(SQLLineageException):
    """Raised when metadata generation fails."""
