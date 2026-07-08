"""
Semantic Search Engine

Embeds a natural language query and searches
the FAISS index.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

import numpy as np

from src.embeddings.embedder import Embedder
from src.embeddings.models import EmbeddingRecord
from src.vectorstore.faiss_store import FAISSStore


@dataclass
class SearchResult:

    score: float

    record: EmbeddingRecord


class SearchEngine:

    def __init__(self, store: FAISSStore):

        self.store = store

        self.embedder = Embedder()

    # ----------------------------------------------------

    def search(
        self,
        question: str,
        top_k: int = 5
    ) -> List[SearchResult]:

        #
        # Embed the question
        #
        vector = self.embedder.model.encode(
            question,
            normalize_embeddings=True
        )

        query = np.asarray(
            [vector],
            dtype=np.float32
        )

        scores, indices = self.store.index.search(
            query,
            top_k
        )

        results: List[SearchResult] = []

        for score, idx in zip(scores[0], indices[0]):

            if idx == -1:
                continue

            results.append(

                SearchResult(

                    score=float(score),

                    record=self.store.records[idx]

                )

            )

        return results
