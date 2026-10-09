"""
MediShield AI: End-to-End RAG Pipeline
Module: backend.app.ai.rag.pipeline

Orchestrates Document Ingestion -> Chunking -> Vector Indexing -> Retrieval -> Generation.
Provides unified interface for both CLI experiments and the FastAPI assistant endpoint.
"""

import os
import time
import yaml
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session

from .ingestion import load_documents
from .chunking import chunk_all_documents
from .embeddings import EmbeddingEngine
from .retriever import VectorRetriever
from .generator import ResponseGenerator


CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "config", "rag_config.yaml")


class RAGPipeline:
    def __init__(self, config_path: str = CONFIG_PATH):
        self.config_path = os.path.abspath(config_path)
        self.config = self._load_config()
        
        # Unpack configuration
        rag_cfg = self.config.get("rag", {})
        llm_cfg = self.config.get("llm", {})
        priv_cfg = self.config.get("privacy", {})

        self.chunk_size = rag_cfg.get("chunk_size", 350)
        self.chunk_overlap = rag_cfg.get("chunk_overlap", 50)
        self.top_k = rag_cfg.get("top_k", 3)
        self.similarity_threshold = rag_cfg.get("similarity_threshold", 0.15)
        self.model_name = rag_cfg.get("embedding_model", "sentence-transformers/all-MiniLM-L6-v2")

        # Initialize components
        self.embedding_engine = EmbeddingEngine(model_name=self.model_name, use_neural=True)
        self.retriever = VectorRetriever(
            embedding_engine=self.embedding_engine,
            top_k=self.top_k,
            similarity_threshold=self.similarity_threshold,
        )
        self.generator = ResponseGenerator(
            provider=llm_cfg.get("provider", "local_extractive_grounded"),
            disable_external=priv_cfg.get("disable_external_llm", True),
        )

        self.documents: List[Dict[str, Any]] = []
        self.chunks: List[Dict[str, Any]] = []
        self._is_indexed = False

    def _load_config(self) -> Dict[str, Any]:
        if os.path.exists(self.config_path):
            with open(self.config_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        return {
            "rag": {"chunk_size": 350, "chunk_overlap": 50, "top_k": 3, "similarity_threshold": 0.15},
            "llm": {"provider": "local_extractive_grounded"},
            "privacy": {"disable_external_llm": True},
        }

    def build_index(self):
        """Loads documents, chunks text, and builds in-memory vector index."""
        self.documents = load_documents()
        self.chunks = chunk_all_documents(
            self.documents,
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
        )
        self.retriever.index_chunks(self.chunks)
        self._is_indexed = True

    def query(
        self,
        question: str,
        top_k: Optional[int] = None,
        db: Optional[Session] = None,
    ) -> Dict[str, Any]:
        """
        Executes query against RAG pipeline.
        Optionally augments with local SQLite inventory context if relevant.
        """
        if not self._is_indexed:
            self.build_index()

        start_time = time.time()
        retrieved_chunks = self.retriever.retrieve(question, top_k=top_k)

        # Optional database augmentation for hybrid clinical decision support
        db_context = None
        if db is not None:
            db_context = self._query_database_context(question, db)

        # Generate grounded response
        res = self.generator.generate_response(question, retrieved_chunks)
        elapsed_ms = round((time.time() - start_time) * 1000.0, 2)

        # If DB context found, prepend or append to response
        if db_context:
            res["answer"] = f"Local Inventory Status:\n{db_context}\n\nClinical Guidance:\n{res['answer']}"

        return {
            "query": question,
            "answer": res["answer"],
            "citations": res["citations"],
            "retrieved_chunks": retrieved_chunks,
            "db_context": db_context,
            "latency_ms": elapsed_ms,
            "embedding_type": self.embedding_engine.embedding_type,
            "grounded": res["grounded"],
        }

    def _query_database_context(self, question: str, db: Session) -> Optional[str]:
        """Checks for relevant operational medicine or supplier database matches."""
        try:
            from datetime import datetime
            from ...models import Medicine, Supplier
            q_lower = question.lower()

            # 1. Expiry Queries
            if any(w in q_lower for w in ["expir", "expiry", "expired", "shelf life"]):
                meds = db.query(Medicine).all()
                expiring = []
                for m in meds:
                    try:
                        days = (datetime.strptime(m.expiry_date, "%Y-%m-%d") - datetime.today()).days
                        if days <= 60:
                            expiring.append((m.name, days, m.inventory))
                    except Exception:
                        pass
                expiring.sort(key=lambda x: x[1])
                if expiring:
                    sample = expiring[:6]
                    lines = [f"• {name} (Stock: {stock} units) — Expires in {days} days" for name, days, stock in sample]
                    return f"Found {len(expiring)} medicines expiring within 60 days:\n" + "\n".join(lines)
                return "All medicines currently have more than 60 days of shelf life remaining."

            # 2. Low Stock / Stockout Queries
            if any(w in q_lower for w in ["low stock", "safety stock", "stockout", "out of stock"]):
                meds = db.query(Medicine).filter(Medicine.inventory <= Medicine.safety_stock).all()
                if meds:
                    sample = meds[:6]
                    lines = [f"• {m.name}: Current stock {m.inventory} (Safety buffer: {m.safety_stock})" for m in sample]
                    return f"Found {len(meds)} medicines at or below safety stock threshold:\n" + "\n".join(lines)
                return "All medicines currently have inventory above designated safety buffers."

            # 3. High Risk / Critical Shortage Queries
            if any(w in q_lower for w in ["high risk", "critical", "shortage warning", "risk level"]):
                meds = db.query(Medicine).filter(Medicine.risk_level == "High").all()
                if meds:
                    sample = meds[:6]
                    lines = [f"• {m.name} (Shortage Prob: {m.shortage_probability}%, Stock: {m.inventory})" for m in sample]
                    return f"High-Risk Medicines Detected ({len(meds)} total items):\n" + "\n".join(lines)
                return "No medicines are currently classified as High Risk."

            # 4. Inventory Health Queries
            if "health" in q_lower or "inventory health" in q_lower:
                meds = db.query(Medicine).all()
                healthy = sum(1 for m in meds if m.inventory > (m.safety_stock or 0))
                score = round((healthy / max(1, len(meds))) * 100.0, 2)
                return f"Hospital Inventory Health Index: {score}% ({healthy}/{len(meds)} items above safety stock)."

            # 5. Best / Top Supplier Queries
            if any(w in q_lower for w in ["best supplier", "top supplier", "recommended supplier", "vendor"]):
                suppliers = db.query(Supplier).order_by(Supplier.score.desc()).all()
                if suppliers:
                    best = suppliers[0]
                    return (
                        f"Recommended Supplier: {best.name}\n"
                        f"• Overall Score: {best.score}/100\n"
                        f"• Reliability: {best.reliability}%\n"
                        f"• Quality Score: {best.quality_score}%\n"
                        f"• Delivery Lead Time: {best.delivery_days} days\n"
                        f"• Procurement Cost: ${best.cost}"
                    )

            # 6. Specific Medicine Search
            meds = db.query(Medicine).all()
            for m in meds:
                if m.name.lower() in q_lower:
                    return (
                        f"Medicine Record: {m.name} ({m.category})\n"
                        f"• Physical Stock: {m.inventory} units\n"
                        f"• Monthly Consumption: {m.demand} units\n"
                        f"• Safety Stock Buffer: {m.safety_stock} units\n"
                        f"• Lead Time: {m.lead_time} days\n"
                        f"• Risk Classification: {m.risk_level} (Prob: {m.shortage_probability}%)\n"
                        f"• Primary Supplier: {m.supplier} (Reliability: {m.supplier_reliability}%)"
                    )
        except Exception:
            pass
        return None


# Global singleton instance for app-wide sharing
_pipeline_instance = None

def get_rag_pipeline() -> RAGPipeline:
    global _pipeline_instance
    if _pipeline_instance is None:
        _pipeline_instance = RAGPipeline()
        _pipeline_instance.build_index()
    return _pipeline_instance
