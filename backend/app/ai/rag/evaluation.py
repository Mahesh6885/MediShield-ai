"""
MediShield AI: Quantitative RAG Benchmark Evaluation
Module: backend.app.ai.rag.evaluation

Implements reproducible quantitative evaluation:
1. Retrieval Hit Rate (% queries where top-k retrieved chunks contain target keywords/concepts)
2. Mean Reciprocal Rank (MRR) of first relevant chunk
3. Groundedness Overlap (% key answer tokens present in retrieved evidence chunks)
4. Citation Validity Rate (% citations referencing valid existing chunk IDs)
5. Distinguishes machine-generated empirical metrics from human ratings (labeled 'Pending Clinical Expert Review')
"""

import os
import json
import pandas as pd
import numpy as np
from typing import Dict, Any, List

from .pipeline import RAGPipeline


# Benchmark evaluation queries covering clinical guidelines, WHO/FDA standards, and inventory SOP
BENCHMARK_QUERIES = [
    {
        "query": "What are the primary early warning indicators of medicine shortages according to WHO?",
        "expected_keywords": ["supplier concentration", "lead time", "inventory cover", "api"],
        "category": "Clinical Guidelines (WHO)",
    },
    {
        "query": "Under FDA guidelines, what are the mandatory advance notification requirements for discontinuances?",
        "expected_keywords": ["506c", "six months", "manufacturing", "interruption"],
        "category": "Regulatory Policy (FDA)",
    },
    {
        "query": "What are the root causes of drug shortages identified by FDA empirical analysis?",
        "expected_keywords": ["manufacturing quality", "sterility", "particulate", "delays"],
        "category": "Regulatory Policy (FDA)",
    },
    {
        "query": "How should health-system pharmacies assess patient acuity when facing an acute shortage?",
        "expected_keywords": ["acuity", "tier 1", "tier 2", "substitute"],
        "category": "Clinical Practice (ASHP)",
    },
    {
        "query": "What dose conservation strategies does ASHP recommend during medicine shortages?",
        "expected_keywords": ["dose rounding", "route conversion", "iv", "oral"],
        "category": "Clinical Practice (ASHP)",
    },
    {
        "query": "How is the standard Reorder Point calculated under the hospital inventory SOP?",
        "expected_keywords": ["reorder point", "rop", "demand", "lead_time", "safety_stock"],
        "category": "Inventory SOP",
    },
    {
        "query": "What are the four direction-aware criteria used to rank pharmaceutical suppliers?",
        "expected_keywords": ["reliability", "quality", "cost", "delivery"],
        "category": "Supplier SOP",
    },
    {
        "query": "What protocol is required when medicine inventory is within 60 days of expiry?",
        "expected_keywords": ["60 days", "expiration", "priority dispensing", "return"],
        "category": "Inventory SOP",
    },
    {
        "query": "What action is required when a medicine is classified as High Shortage Risk?",
        "expected_keywords": ["expedited procurement", "secondary supplier", "24 hours"],
        "category": "Clinical Decision Support",
    },
    {
        "query": "What mitigation actions should hospital administrators take to avoid speculative hoarding?",
        "expected_keywords": ["hoarding", "panic-buying", "imbalances", "pre-qualified"],
        "category": "Clinical Guidelines (WHO)",
    },
]


def run_rag_evaluation(
    pipeline: RAGPipeline,
    results_dir: str = "results",
) -> Dict[str, Any]:
    """
    Executes automated RAG evaluation benchmark and writes results to CSV and JSON.
    """
    os.makedirs(results_dir, exist_ok=True)
    if not pipeline._is_indexed:
        pipeline.build_index()

    eval_rows = []
    hit_count = 0
    reciprocal_ranks = []
    groundedness_scores = []
    citation_validities = []

    for item in BENCHMARK_QUERIES:
        query = item["query"]
        expected_keywords = item["expected_keywords"]
        category = item["category"]

        res = pipeline.query(query, top_k=3)
        retrieved_chunks = res["retrieved_chunks"]
        answer = res["answer"]
        citations = res["citations"]

        # 1. Retrieval Hit Rate & Rank
        found_rank = 0
        all_retrieved_text = " ".join([c["text"].lower() for c in retrieved_chunks])
        
        for r, chunk in enumerate(retrieved_chunks, 1):
            chunk_text = chunk["text"].lower()
            if any(kw in chunk_text for kw in expected_keywords):
                found_rank = r
                break

        if found_rank > 0:
            hit_count += 1
            reciprocal_ranks.append(1.0 / found_rank)
        else:
            reciprocal_ranks.append(0.0)

        # 2. Groundedness (Keyword overlap between answer and retrieved text)
        answer_words = set(answer.lower().split())
        retrieved_words = set(all_retrieved_text.split())
        overlap = len(answer_words.intersection(retrieved_words)) / max(1, len(answer_words))
        groundedness_scores.append(overlap)

        # 3. Citation Validity
        valid_chunks_in_index = {c["chunk_id"] for c in pipeline.chunks}
        if citations:
            valid_cit = sum(1 for c in citations if c["chunk_id"] in valid_chunks_in_index)
            cit_rate = valid_cit / len(citations)
        else:
            cit_rate = 0.0
        citation_validities.append(cit_rate)

        # Record evaluation row
        eval_rows.append({
            "query_id": f"Q{len(eval_rows)+1:02d}",
            "category": category,
            "query": query,
            "retrieval_hit": 1 if found_rank > 0 else 0,
            "reciprocal_rank": round(1.0 / found_rank, 3) if found_rank > 0 else 0.0,
            "groundedness_ratio": round(overlap, 3),
            "citation_validity": round(cit_rate, 3),
            "latency_ms": res["latency_ms"],
            "top_retrieved_source": retrieved_chunks[0]["source"] if retrieved_chunks else "None",
            "top_retrieved_chunk": retrieved_chunks[0]["chunk_id"] if retrieved_chunks else "None",
            "top_similarity_score": retrieved_chunks[0]["score"] if retrieved_chunks else 0.0,
            "human_rating_1_to_5": "Pending Clinical Expert Review",
            "human_expert_notes": "Awaiting camera-ready review panel evaluation",
        })

    df_eval = pd.DataFrame(eval_rows)

    # Save benchmark evaluation CSV
    csv_path = os.path.join(results_dir, "rag_evaluation.csv")
    df_eval.to_csv(csv_path, index=False)

    total_q = len(BENCHMARK_QUERIES)
    summary = {
        "benchmark_name": "MediShield AI RAG Clinical Supply Chain Benchmark v1.0",
        "total_queries_evaluated": total_q,
        "retrieval_hit_rate_pct": round((hit_count / total_q) * 100.0, 2),
        "mean_reciprocal_rank_mrr": round(float(np.mean(reciprocal_ranks)), 4),
        "mean_groundedness_ratio": round(float(np.mean(groundedness_scores)), 4),
        "mean_citation_validity_pct": round(float(np.mean(citation_validities)) * 100.0, 2),
        "mean_latency_ms": round(float(df_eval["latency_ms"].mean()), 2),
        "embedding_model": pipeline.model_name,
        "embedding_type": pipeline.embedding_engine.embedding_type,
        "top_k": pipeline.top_k,
        "total_indexed_documents": len(pipeline.documents),
        "total_indexed_chunks": len(pipeline.chunks),
        "human_evaluation_status": "Pending Clinical Expert Review (Unverified placeholder ratings strictly avoided)",
    }

    # Save summary JSON
    summary_path = os.path.join(results_dir, "rag_evaluation_summary.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    # Save RAG Configuration JSON
    cfg_json_path = os.path.join(results_dir, "rag_configuration.json")
    with open(cfg_json_path, "w", encoding="utf-8") as f:
        json.dump(pipeline.config, f, indent=2)

    # Save RAG Documents JSON
    docs_summary = [{
        "doc_id": d["doc_id"],
        "title": d["title"],
        "source": d["source"],
        "character_count": d["character_count"],
    } for d in pipeline.documents]
    docs_json_path = os.path.join(results_dir, "rag_documents.json")
    with open(docs_json_path, "w", encoding="utf-8") as f:
        json.dump(docs_summary, f, indent=2)

    return summary
