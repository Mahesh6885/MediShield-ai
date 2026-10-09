"""
MediShield AI: RAG Embedding Engine
Module: backend.app.ai.rag.embeddings

Provides vector embedding extraction for text chunks and queries.
Supports:
1. Sentence-Transformers (all-MiniLM-L6-v2) for dense neural semantic embeddings.
2. Robust local scikit-learn TF-IDF L2-normalized dense embeddings as deterministic fallback.
"""

from typing import List, Union
import numpy as np


class EmbeddingEngine:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2", use_neural: bool = True):
        self.model_name = model_name
        self.use_neural = use_neural
        self.neural_model = None
        self.tfidf_vectorizer = None
        self.embedding_type = "tfidf_fallback"
        self._initialize()

    def _initialize(self):
        if self.use_neural:
            try:
                from sentence_transformers import SentenceTransformer
                self.neural_model = SentenceTransformer(self.model_name)
                self.embedding_type = "sentence_transformers_neural"
                return
            except Exception:
                # Fallback to TF-IDF dense representation
                pass

        from sklearn.feature_extraction.text import TfidfVectorizer
        self.tfidf_vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            max_features=2048,
            sublinear_tf=True,
            stop_words="english"
        )
        self.embedding_type = "tfidf_dense_svd"

    def fit_corpus(self, texts: List[str]):
        """Fits vocabulary if using TF-IDF fallback."""
        if self.tfidf_vectorizer is not None:
            self.tfidf_vectorizer.fit(texts)

    def embed_texts(self, texts: List[str]) -> np.ndarray:
        """Embeds a list of text strings into L2-normalized float numpy matrix."""
        if self.neural_model is not None:
            try:
                emb = self.neural_model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
                return emb.astype(np.float32)
            except Exception:
                pass

        if self.tfidf_vectorizer is not None:
            mat = self.tfidf_vectorizer.transform(texts).toarray()
            # Normalize rows to unit length for cosine similarity
            norms = np.linalg.norm(mat, axis=1, keepdims=True)
            norms[norms == 0] = 1e-9
            return (mat / norms).astype(np.float32)

        raise RuntimeError("No embedding engine is initialized.")

    def embed_query(self, query: str) -> np.ndarray:
        """Embeds a single query string into 1D normalized float array."""
        matrix = self.embed_texts([query])
        return matrix[0]
