"""
MediShield AI: RAG Document Ingestion
Module: backend.app.ai.rag.ingestion

Loads and parses legitimate pharmaceutical and health system documentation.
Extracts structural sections and preserves document provenance metadata.
"""

import os
import glob
from typing import List, Dict, Any


DOCUMENTS_DIR = os.path.join(os.path.dirname(__file__), "documents")


def load_documents(docs_dir: str = DOCUMENTS_DIR) -> List[Dict[str, Any]]:
    """
    Scans the documents directory and parses all markdown and text files.
    Returns list of parsed documents with metadata.
    """
    if not os.path.exists(docs_dir):
        os.makedirs(docs_dir, exist_ok=True)
        return []

    doc_files = glob.glob(os.path.join(docs_dir, "*.md")) + glob.glob(os.path.join(docs_dir, "*.txt"))
    documents = []

    for file_path in doc_files:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        lines = content.strip().split("\n")
        title = lines[0].replace("#", "").strip() if lines else os.path.basename(file_path)
        
        # Extract Source and Document ID headers if present
        source = "Official Pharmaceutical Guidance"
        doc_id = os.path.splitext(os.path.basename(file_path))[0]

        body_lines = []
        for line in lines[1:]:
            if line.startswith("Source:"):
                source = line.replace("Source:", "").strip()
            elif line.startswith("Document ID:"):
                doc_id = line.replace("Document ID:", "").strip()
            else:
                body_lines.append(line)

        documents.append({
            "doc_id": doc_id,
            "title": title,
            "source": source,
            "file_path": file_path,
            "content": "\n".join(body_lines).strip(),
            "character_count": len(content),
        })

    return sorted(documents, key=lambda x: x["doc_id"])
