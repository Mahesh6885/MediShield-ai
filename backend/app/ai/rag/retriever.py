"""
MediShield AI: RAG Vector Retriever
Module: backend.app.ai.rag.retriever

Implements cosine similarity top-k retrieval over embedded document chunks.
Returns ranked chunks with similarity scores and full provenance metadata.
"""

from typing import List, Dict, Any, Optional
import numpy as np


class VectorRetriever:
    def __init__(self, embedding_engine, top_k: int = 3, similarity_threshold: float = 0.15):
        self.embedding_engine = embedding_engine
        self.top_k = top_k
        self.similarity_threshold = similarity_threshold
        self.chunks: List[Dict[str, Any]] = []
        self.index_embeddings: Optional[np.ndarray] = None

    def index_chunks(self, chunks: List[Dict[str, Any]]):
        """Indexes chunks by embedding their text contents."""
        self.chunks = chunks
        texts = [c["text"] for c in chunks]
        
        # Fit corpus vocabulary if using TF-IDF
        self.embedding_engine.fit_corpus(texts)
        self.index_embeddings = self.embedding_engine.embed_texts(texts)

    def retrieve(self, query: str, top_k: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Executes vector similarity search for query against index.
        Returns top-k matching chunks sorted by cosine similarity.
        """
        if self.index_embeddings is None or len(self.chunks) == 0:
            return []

        k = top_k if top_k is not None else self.top_k
        query_vec = self.embedding_engine.embed_query(query)

        # Dot product of L2-normalized vectors equals cosine similarity
        similarities = np.dot(self.index_embeddings, query_vec)

        # Sort indices in descending order
        ranked_indices = np.argsort(similarities)[::-1]

        results = []
        for idx in ranked_indices[:k]:
            score = float(similarities[idx])
            if score >= self.similarity_threshold:
                chunk_copy = self.chunks[idx].copy()
                chunk_copy["score"] = round(score, 4)
                results.append(chunk_copy)

        return results
