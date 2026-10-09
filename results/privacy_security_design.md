# MediShield AI: Data Privacy & Security Architecture
**Document:** `results/privacy_security_design.md`  
**Classification:** Application Security & Operational Data Privacy Protocol  
**Compliance Context:** Healthcare Inventory Decision Support (IEEE CEEE 2026 Camera-Ready Revision)  
**Date:** October 6, 2026  

---

## 1. Executive Summary

Healthcare and pharmaceutical supply-chain records contain sensitive operational signals, including inventory levels, purchase contracts, supplier pricing, and clinical prescribing velocity. Inadvertent transmission of this data to external commercial Large Language Model (LLM) APIs poses severe confidentiality, regulatory, and competitive risks. MediShield AI adopts a **privacy-by-design, local-first architecture** ensuring that operational inventory datasets never leave the healthcare facility's controlled boundary.

---

## 2. Privacy-Preserving Architecture & Local Processing

### 2.1 Zero-Transmission Default (Local-First Operation)
- **Local Embeddings:** Text embedding generation is executed in-process on the local host machine using `sentence-transformers` (`all-MiniLM-L6-v2`) or local dense vector representations. No query text or document chunk is transmitted to external embedding APIs.
- **Local Vector Indexing:** All guideline chunks are indexed in-memory and queried via local cosine vector search.
- **Grounded Local Synthesis:** Responses are synthesized locally using an extractive grounded evidence engine.
- **Explicit Kill-Switch:** Configured via `config/rag_config.yaml`:
  ```yaml
  privacy:
    disable_external_llm: true
    allow_external_transmission: false
    anonymize_phi: true
    store_chat_locally: true
  ```
  When `disable_external_llm: true`, any accidental external HTTP request is blocked at the software boundary.

### 2.2 Operational Inventory Data Isolation
- Synthetic and hospital operational databases (`medishield.db`) reside exclusively in local SQLite storage.
- Drug stock quantities, supplier negotiation prices, and reorder alerts are never embedded into public vector stores or transmitted across public networks.
- Queries referencing specific inventory items (e.g., "Paracetamol stock") are resolved strictly against the internal relational database using local SQL parameterized statements.

---

## 3. Application-Level Security Improvements

Prior to this camera-ready revision, the prototype utilized plaintext passwords and hardcoded credentials (`admin/admin123`). We have implemented basic application-level security controls:

### 3.1 Password Hashing via bcrypt
- Replaced all plaintext password comparisons with salted, adaptive key-derivation hashing via `bcrypt` (12 rounds):
  $$\text{hash} = \text{bcrypt.hashpw}(\text{password}, \text{salt})$$
- Database schema stores bcrypt hashes exclusively; plaintext passwords are never persisted.

### 3.2 Cryptographic Session Management (JWT Bearer Tokens)
- Implemented RFC 7519 compliant JSON Web Tokens (JWT) signed with HMAC-SHA256 (`HS256`).
- Tokens include explicit expiration (`exp`), subject claims (`sub`), and issuance timestamps (`iat`).
- Configurable token lifetimes via environment variable `ACCESS_TOKEN_EXPIRE_MINUTES` (default 480 minutes).

### 3.3 Endpoint Authorization & Role Guards
- FastAPI dependency injection (`Depends(get_current_user)`) inspects HTTP `Authorization: Bearer <token>` headers.
- Distinct application roles: `Admin` (full system configuration, supplier edits) and `Pharmacist` (clinical inquiries, inventory views, prediction execution).
- Non-breaking backward compatibility is preserved for automated testing suites and frontend demonstration modes.

### 3.4 Elimination of Hardcoded Secrets
- Authentication secrets and default administrator credentials are moved to environment variables (`MEDISHIELD_SECRET_KEY`, `ADMIN_PASSWORD`).
- Created standardized template file `.env.example` to instruct system operators on production key generation.

---

## 4. Realistic Scope Disclaimer

> **Scientific Integrity & Operational Notice:**  
> MediShield AI does **not** claim compliance with enterprise-grade HIPAA, HITRUST, or ISO 27001 healthcare standards. Rather, these implementations represent rigorous application-level engineering safeguards suitable for academic research prototypes, clinical simulation environments, and local edge-device hospital deployments.
