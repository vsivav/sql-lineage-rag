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

        # Cosine similarity (vectors must be normalized)
        self.index = faiss.IndexFlatIP(dimension)

        self.records: List[EmbeddingRecord] = []

    # --------------------------------------------------

    def add(self, record: EmbeddingRecord):

        vector = np.asarray(
            [record.vector],
            dtype=np.float32
        )

        self.index.add(vector)

        self.records.append(record)

    # --------------------------------------------------

    def add_many(self, records: List[EmbeddingRecord]):

        for record in records:
            self.add(record)

    # --------------------------------------------------

    def search(
        self,
        query_vector,
        k: int = 5
    ) -> List[EmbeddingRecord]:

        query = np.asarray(
            [query_vector],
            dtype=np.float32
        )

        scores, indices = self.index.search(query, k)

        results = []

        for idx in indices[0]:

            if idx == -1:
                continue

            results.append(
                self.records[idx]
            )

        return results

    # --------------------------------------------------

    def save(
        self,
        index_file: str,
        metadata_file: str
    ):

        Path(index_file).parent.mkdir(
            parents=True,
            exist_ok=True
        )

        faiss.write_index(
            self.index,
            index_file
        )

        with open(
            metadata_file,
            "w",
            encoding="utf-8"
        ) as fp:

            json.dump(

                [

                    {
                        "id": r.id,
                        "text": r.text,
                        "metadata": r.metadata
                    }

                    for r in self.records

                ],

                fp,

                indent=4

            )

    # --------------------------------------------------

    @classmethod
    def load(
        cls,
        index_file: str,
        metadata_file: str,
        dimension: int
    ):

        store = cls(dimension)

        store.index = faiss.read_index(index_file)

        with open(
            metadata_file,
            encoding="utf-8"
        ) as fp:

            data = json.load(fp)

        for item in data:

            store.records.append(

                EmbeddingRecord(

                    id=item["id"],

                    text=item["text"],

                    vector=[],

                    metadata=item["metadata"]

                )

            )

        return store
