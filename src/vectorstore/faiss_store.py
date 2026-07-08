"""
FAISS Vector Store
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import List

import faiss
import numpy as np

from src.embeddings.models import EmbeddingRecord


class FAISSStore:

    def __init__(self, dimension: int):

        self.dimension = dimension

        self.index = faiss.IndexFlatIP(dimension)

        self.records: List[EmbeddingRecord] =
