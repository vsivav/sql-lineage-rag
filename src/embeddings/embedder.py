"""
Sentence Transformer Embedder
"""

from sentence_transformers import SentenceTransformer

from src.embeddings.models import EmbeddingRecord


class Embedder:

    def __init__(
        self,
        model_name="all-MiniLM-L6-v2"
    ):

        self.model = SentenceTransformer(model_name)

    # ----------------------------------------------

    def embed_chunk(
        self,
        chunk
    ) -> EmbeddingRecord:

        vector = self.model.encode(
            chunk.text,
            normalize_embeddings=True
        )

        return EmbeddingRecord(

            id=chunk.chunk_id,

            text=chunk.text,

            vector=vector.tolist(),

            metadata=chunk.metadata

        )

    # ----------------------------------------------

    def embed_chunks(
        self,
        chunks
    ):

        return [

            self.embed_chunk(chunk)

            for chunk in chunks

        ]
