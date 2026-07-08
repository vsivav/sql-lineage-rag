from loguru import logger
import sys

logger.remove()

logger.add(
    sys.stdout,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    level="INFO"
)

logger.add(
    "logs/sql_lineage.log",
    rotation="20 MB",
    retention="30 days",
    level="DEBUG"
)

__all__ = ["logger"]
