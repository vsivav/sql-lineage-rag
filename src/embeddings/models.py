"""
Embedding Models
"""

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class EmbeddingRecord:
    """
    One vector stored in FAISS.
    """

    id: str

    text: str

    vector: List[float]

    metadata: Dict
