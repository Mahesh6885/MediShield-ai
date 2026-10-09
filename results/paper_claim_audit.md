# MediShield AI: Paper Claims Consistency Audit & Truth-in-Science Review
**Document:** `results/paper_claim_audit.md`  
**Conference:** IEEE CEEE 2026 (Paper ID 3045)  
**Classification:** Scientific Claim Verification & Camera-Ready Text Guidance  
**Authoritative Date:** October 6, 2026  

---

## 1. Audit Methodology & Standards

Every substantive claim regarding system capabilities, validation datasets, hospital deployment, and clinical impact was systematically audited against the executable codebase, empirical artifacts, and authoritative experimental outputs. Claims are strictly classified into three categories:

- **SUPPORTED:** Empirically verified through executed code and saved reproducible outputs in `results/`.
- **PARTIALLY SUPPORTED:** Valid within a simulated, benchmark, or prototype scope, but requiring precise qualifying language in the camera-ready manuscript to prevent overgeneralization.
- **NOT SUPPORTED:** Unsubstantiated by empirical code or empirical hospital data; must be revised, toned down, or explicitly reframed in the camera-ready paper.

---

## 2. Comprehensive Claim Classification Matrix

| Key Domain Area | Specific Target Claim | Audit Status | Codebase & Empirical Ground Truth | Required Camera-Ready Revision Text |
| :--- | :--- | :---: | :--- | :--- |
| **Real-World Data** | *"Validated using real-world hospital medicine shortage records"* | **NOT SUPPORTED** | The ML dataset consists of 5,000 synthetic observations generated via uniform feature distributions and a domain-informed composite risk formula (`backend/app/ai/data_generation.py`). No real-world EHR, ERP, or supplier database was queried. | *"Evaluated on a 5,000-sample synthetic benchmark dataset generated using a domain-informed supply-chain risk formulation."* |
| **Hospital Data** | *"Trained on clinical EHR records from tertiary care hospitals"* | **NOT SUPPORTED** | Zero clinical EHR records or patient health identifiers exist in the repository. Database is an isolated synthetic SQLite instance. | *"Designed for hospital pharmacy supply-chain decision support and evaluated using simulated healthcare operational parameters."* |
| **Clinical Validation** | *"Clinically validated by healthcare practitioners in hospital settings"* | **NOT SUPPORTED** | No institutional review board (IRB) protocol, prospective clinical trial, or blinded clinician workflow evaluation was conducted. | *"System represents a decision-support prototype evaluated on computational benchmarks; prospective clinical workflow validation is planned as future work."* |
| **Expert Validation** | *"Multi-criteria supplier weights (0.35, 0.30, 0.20, 0.15) were calibrated and validated by clinical pharmacy experts"* | **NOT SUPPORTED** | No formal expert elicitation (Delphi study, AHP survey) was conducted; weights were predefined heuristic research baselines. | *"Evaluated under predefined baseline multi-criteria weights, subjected to systematic $\pm 20\%$ sensitivity perturbation analysis across 200 Monte Carlo trials."* |
| **RAG Assistant** | *"Interactive RAG assistant retrieving clinical guidelines and operational protocols"* | **SUPPORTED** | Implemented modular RAG pipeline (`backend/app/ai/rag/`) with document ingestion (WHO, FDA, ASHP, SOP), `sentence-transformers/all-MiniLM-L6-v2` neural embeddings, cosine vector retriever, and citation grounding. Quantitative benchmark confirms 90.0% Hit Rate, 0.8333 MRR, 68.66% Groundedness, and 100.0% citation validity. | *Retain claim; cite empirical benchmark metrics from Table 8.* |
| **LLM Integration** | *"Powered by advanced Large Language Models"* | **PARTIALLY SUPPORTED** | Default pipeline utilizes a local extractive grounded evidence synthesis engine (extracts verified sentences from retrieved chunks matching query tokens) to guarantee privacy and eliminate API dependencies. Optional external LLM hooks exist. | *"Employs a local privacy-preserving grounded evidence synthesis engine over neural vector representations, with optional generative LLM integration."* |
| **Inventory Cost Reduction** | *"Dramatically cuts inventory expenditures by double-digit percentages across health networks"* | **PARTIALLY SUPPORTED** | 180-day stochastic inventory simulation across 5 seeds shows the proposed risk-aware policy achieved a 1.36% total cost reduction ($1,676.58 $\pm$ $16.62 vs $1,699.64 $\pm$ $22.63 baseline). | *"Stochastic multi-period inventory simulations demonstrate an empirical 1.36% total cost reduction ($1,676.58 vs $1,699.64) via dynamic reorder-point calibration."* |
| **Stockout Reduction** | *"MediShield AI completely eliminates hospital stockouts"* | **PARTIALLY SUPPORTED** | Simulation demonstrates a cost-service trade-off: proposed dynamic policy achieves 99.90% service level with 0.2 $\pm$ 0.45 stockout days (vs 0.0 days baseline). The proposed policy slightly trades absolute zero stockouts for reduced holding inventory. | *"Maintains a high 99.90% service level (0.2 stockout days over 180 days) while optimizing inventory holding costs."* |
| **Real-Time Prediction** | *"Provides real-time shortage prediction and explainability"* | **SUPPORTED** | Live FastAPI endpoint `/prediction/{medicine_id}` generates XGBoost probability and per-instance TreeSHAP explanations in under 35 ms. | *Supported. Retain claim.* |
| **Scalability** | *"Enterprise scalable cloud architecture handling millions of hospital transactions"* | **NOT SUPPORTED** | System executes on local SQLite with synchronous locks and local FastAPI processes. No load testing, Kubernetes clustering, or distributed message brokers exist. | *"Demonstrates a lightweight, locally deployable modular architecture suitable for departmental edge deployment."* |
| **Security & Privacy** | *"Enterprise HIPAA-compliant healthcare security infrastructure"* | **PARTIALLY SUPPORTED** | Implemented bcrypt password hashing with salt, cryptographically signed JWT bearer tokens, and `.env` isolation. However, full enterprise HIPAA requirements (BAA agreements, dedicated KMS encryption at rest, centralized SIEM) are not present. | *"Implements foundational application-level access controls including bcrypt password hashing and JWT token authorization for prototype research deployment."* |
| **Production Readiness** | *"Production-ready enterprise clinical platform"* | **NOT SUPPORTED** | Codebase is an academic research prototype and decision-support proof of concept, lacking clinical EHR integration, fault tolerance, and HA clustering. | *"A functional research prototype and decision-support proof-of-concept ready for pilot departmental testing."* |

---

## 3. Mandatory Camera-Ready Manuscript Action Items

1. **Abstract & Introduction Framing:** Replace all references to *"real-world hospital records"* or *"clinical validation"* with *"a 5,000-sample synthetic benchmark dataset generated using a domain-informed supply-chain risk formulation"*.
2. **Model Comparison Transparency:** State clearly in Section IV that standard Logistic Regression achieves 0.9974 accuracy because the underlying synthetic risk formulation is a linear composite score. Clarify that XGBoost (0.9750 accuracy) provides robust tree partitioning, non-linear feature interaction modeling, and feature importance explainability.
3. **Simulation Trade-Off Clarification:** Clarify that the 180-day inventory simulation reflects a 1.36% cost reduction and 99.90% service level, explicitly highlighting the cost-service trade-off rather than claiming simultaneous zero stockouts and massive cost cuts.
4. **RAG Architecture Specifics:** Describe the decision-support module as a dense neural retrieval and local grounded extractive evidence synthesis system rather than an unconstrained generative LLM.
