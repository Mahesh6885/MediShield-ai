"""
MediShield AI: RAG Text Chunking
Module: backend.app.ai.rag.chunking

Implements section-aware and sliding-window chunking.
Ensures every chunk retains full provenance metadata (doc_id, source, section, chunk_id).
"""

import re
from typing import List, Dict, Any


def chunk_document(
    doc: Dict[str, Any],
    chunk_size: int = 350,
    chunk_overlap: int = 50,
) -> List[Dict[str, Any]]:
    """
    Chunks a single document using markdown section boundaries and word sliding window.
    """
    content = doc["content"]
    doc_id = doc["doc_id"]
    source = doc["source"]

    # Split into sections by markdown header
    raw_sections = re.split(r"(##\s+[^\n]+)", content)
    
    sections = []
    current_title = "Introduction"
    current_text = ""

    for part in raw_sections:
        part = part.strip()
        if not part:
            continue
        if part.startswith("## "):
            if current_text:
                sections.append((current_title, current_text))
            current_title = part.replace("## ", "").strip()
            current_text = ""
        else:
            current_text += "\n" + part

    if current_text:
        sections.append((current_title, current_text))

    chunks = []
    chunk_counter = 1

    for section_title, sec_text in sections:
        words = sec_text.split()
        if not words:
            continue

        # If section is small enough, keep as single chunk
        if len(words) <= chunk_size:
            chunk_id = f"{doc_id}_C{chunk_counter:03d}"
            chunks.append({
                "chunk_id": chunk_id,
                "doc_id": doc_id,
                "source": source,
                "section": section_title,
                "text": " ".join(words),
                "word_count": len(words),
            })
            chunk_counter += 1
        else:
            # Sliding window chunking
            start = 0
            while start < len(words):
                end = min(start + chunk_size, len(words))
                chunk_words = words[start:end]
                chunk_id = f"{doc_id}_C{chunk_counter:03d}"
                chunks.append({
                    "chunk_id": chunk_id,
                    "doc_id": doc_id,
                    "source": source,
                    "section": section_title,
                    "text": " ".join(chunk_words),
                    "word_count": len(chunk_words),
                })
                chunk_counter += 1
                if end == len(words):
                    break
                start += max(1, chunk_size - chunk_overlap)

    return chunks


def chunk_all_documents(
    documents: List[Dict[str, Any]],
    chunk_size: int = 350,
    chunk_overlap: int = 50,
) -> List[Dict[str, Any]]:
    """Chunks all ingested documents and returns consolidated chunk catalog."""
    all_chunks = []
    for doc in documents:
        chunks = chunk_document(doc, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        all_chunks.extend(chunks)
    return all_chunks
