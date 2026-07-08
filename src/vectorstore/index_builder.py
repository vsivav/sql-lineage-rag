"""
Builds a FAISS index from metadata chunks.
"""

from src.embeddings.embedder import Embedder
from src.vectorstore.faiss_store import FAISSStore


class IndexBuilder:

    def __init__(self):

        self.embedder = Embedder()

    def build(self, chunks):

        records = self.embedder.embed_chunks(chunks)

        dimension = len(records[0].vector)

        store = FAISSStore(dimension)

        store.add_many(records)

        return store
