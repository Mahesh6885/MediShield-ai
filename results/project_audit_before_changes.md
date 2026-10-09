# MediShield AI: Pre-Modification Project Audit Report
**Project:** MediShield AI – Medicine Shortage Prediction, Supplier Ranking, Inventory Optimization, and Clinical/Decision Support Assistant  
**Conference Context:** IEEE CEEE 2026 (Paper ID 3045, Accepted with Revisions)  
**Date:** October 6, 2026  
**Auditor Role:** Senior ML Engineer, Research Engineer, Backend Engineer, and Experimental Reproducibility Engineer  
**Workspace:** `d:\medishield-ai-v2`  
**Git Branch Created for Safety:** `backup-pre-revision` (from base commit `40bfc12`)  

---

## 1. Executive Summary

This audit assesses the current state of the MediShield AI repository prior to implementing camera-ready improvements. While an initial prototype exists with basic frontend pages, FastAPI endpoints, a SQLite database, and preliminary ML scripts, multiple core research and engineering components are either incomplete, heuristic, or contain scientific contradictions that must be resolved for IEEE camera-ready publication.

---

## 2. Current Module Status (Implemented vs. Not Implemented)

| Subsystem / Module | File Location(s) | Implementation Status | Functional Audit Findings |
| :--- | :--- | :---: | :--- |
| **Data Generation** | `backend/app/ai/train_model.py`, `run_experiments.py` | **Partial / Flawed** | Generates 5,000 synthetic samples. Contains a severe domain contradiction: $+2.0 \cdot \text{safety\_stock}$ artificially inflates shortage risk. No modular standalone generator with parameter metadata. |
| **Data Preprocessing** | `backend/app/ai/train_model.py` | **Not Implemented** | Raw synthetic values fed directly to XGBoost. No scikit-learn Pipeline or ColumnTransformer, no systematic check for missingness or categorical handling. |
| **Feature Engineering** | `backend/app/ai/train_model.py` | **Not Implemented in App** | App uses only 6 raw features (`inventory`, `demand`, `lead_time`, `supplier_reliability`, `expiry_days`, `safety_stock`). `run_experiments.py` had preliminary scripts for 5 engineered features, but not integrated into backend pipeline. |
| **Shortage Classifier** | `backend/app/ai/train_model.py`, `backend/app/ai/predict.py` | **Implemented (Baseline)** | XGBClassifier (`n_estimators=150, max_depth=4, lr=0.1, random_state=42`) trained on raw features without hyperparameter tuning or stratified cross-validation on train splits. |
| **Model Comparison** | `run_experiments.py` | **Partial** | Compares Logistic Regression, Decision Tree, Random Forest, Default XGBoost, and Tuned XGBoost. Logistic Regression performs near-perfectly because generative rule was linear. Needs rigorous multi-seed evaluation. |
| **Hyperparameter Tuning** | `train_model.py` | **Not Implemented** | Hardcoded arbitrary parameters. Needs systematic `GridSearchCV` or `RandomizedSearchCV` strictly on training folds. |
| **Ablation Study** | `run_experiments.py` | **Partial** | Evaluated in standalone script, but needs formal pipeline integration, multi-seed aggregation (mean $\pm$ std), and exportable tables. |
| **Class Imbalance** | `run_experiments.py` | **Partial** | Tested `scale_pos_weight` in script; needs systematic evaluation and scientific justification based on actual class distributions. |
| **Confusion Matrix / Curves**| `run_experiments.py` | **Partial** | Generated initial plots, but formatting needs IEEE publication standards (vector PDF, exact metrics, clean typography, strict alignment with final held-out test seed). |
| **SHAP Global Explanations** | `figures/fig_shap_global.pdf`, `run_experiments.py` | **Partial** | Beeswarm and bar plots exist, but mirror the $+2.0 \cdot \text{safety\_stock}$ contradiction. `shap_explain.py` is empty (0 bytes). |
| **SHAP Local Explanations** | `backend/app/ai/predict.py` | **Partial** | TreeExplainer generates per-instance impact for API, but representative cases (TP, TN, FP, FN) with vector figures are not fully exported. |
| **Supplier Recommendation** | `backend/app/routes/suppliers.py` | **Flawed Heuristic** | Uses arbitrary static offsets (`150 - cost`, `10 - delivery_days`). Lacks direction-aware min-max normalization and weight sensitivity analysis. |
| **Inventory Optimization** | `backend/app/routes/inventory.py` | **Static Heuristic** | Static ROP and deterministic EOQ. Lacks dynamic cycle service level calculation ($z \cdot \sigma_d \cdot \sqrt{L}$) and multi-period stochastic simulation across seeds. |
| **RAG Assistant** | `backend/app/ai/chatbot.py` | **NOT A RAG SYSTEM** | Implemented as a 112-line hardcoded string matching script with SQLite queries (`if "low stock" in text:`). No embeddings, no vector store, no chunking, no LLM, no citations. |
| **RAG Evaluation** | `results/rag_eval_for_human_rating.csv` | **Incomplete / Pending** | 33 evaluation questions exist, but ratings are unrated or pending. No quantitative retrieval recall/precision benchmark. |
| **Authentication & Security** | `backend/app/routes/auth.py` | **Insecure Prototype** | Hardcoded credentials (`admin/admin123`, `pharmacist/pharma123`), plaintext passwords in database, zero API endpoint route guards (`Depends`), no JWT/session tokens. |
| **Database Schema** | `backend/app/models.py`, `medishield.db` | **Implemented** | SQLite database with `medicines`, `suppliers`, `users`, `notifications`, `settings`, `prediction_history`. Functional but needs secure password columns and migrations. |
| **Frontend UI** | `src/` (React + Vite + TypeScript) | **Implemented Prototype** | Functional dashboards, assistant chat, prediction viewer, inventory table, and supplier list. Needs integration with enhanced API outputs and citations. |

---

## 3. Current Dependencies & Runtime Environment

### 3.1 Python Environment (`backend/venv`)
- **Python Version:** 3.14.3 (Windows amd64)
- **Key Installed Packages:**
  - `fastapi==0.141.1`, `uvicorn==0.52.4`, `starlette==1.6.0`, `pydantic==2.13.4`
  - `scikit-learn==1.9.0`, `xgboost==3.4.1`, `shap==0.52.0`, `numpy==2.5.2`, `scipy==1.18.1`, `pandas==3.0.5`
  - `SQLAlchemy==2.0.52`
  - `matplotlib==3.11.2`, `reportlab==5.0.1`, `pillow==12.3.0`
- **Missing Required Packages for Revision:**
  - RAG & Embeddings: `sentence-transformers`, `torch`, `transformers`, `pyyaml`
  - Security & Authentication: `bcrypt`, `pyjwt`

### 3.2 Frontend Environment
- **Node.js / Vite:** React 19, TypeScript, Tailwind CSS, Lucide icons, Axios.

---

## 4. Current Dataset Audit

- **Source:** Pure synthetic generator in `train_model.py` and `run_experiments.py`.
- **Observations:** 5,000 samples.
- **Features (6 raw):** `inventory` (5–200), `demand` (20–220), `lead_time` (1–8), `supplier_reliability` (60–99), `expiry_days` (15–365), `safety_stock` (5–25).
- **Label Generation Formula (ORIGINAL):**
  $$\text{score} = 0.45 \cdot \text{demand} - 0.35 \cdot \text{inventory} + 8.0 \cdot \text{lead\_time} - 0.30 \cdot \text{supplier\_reliability} - 0.05 \cdot \text{expiry\_days} + 2.0 \cdot \text{safety\_stock}$$
  $$\text{shortage} = \mathbb{I}(\text{score} > 40.0)$$
- **Observed Class Distribution:** 1,966 No Shortage (39.32%) vs. 3,034 Shortage (60.68%).
- **Integrity Rule:** Clearly labeled as:
  *"Synthetic medicine-shortage dataset generated using a domain-informed supply-chain risk formulation."*
  Never claimed as clinical hospital EHR or actual pharmaceutical company records.

---

## 5. Current Machine Learning Model Audit

- **Algorithm:** XGBoost (`XGBClassifier`)
- **Parameters:** `n_estimators=150`, `max_depth=4`, `learning_rate=0.1`, `random_state=42`.
- **Training Process:** Previously trained on 100% of the dataset with 0% validation/test split.
- **Saved Artifact:** `backend/app/ai/xgboost_model.pkl` (260 KB).
- **Inference Pipeline:** `backend/app/ai/predict.py` loads model and computes SHAP values on single instances via `shap.TreeExplainer`.
- **Deficiencies:**
  1. No proper train/test split in the core backend training script.
  2. Zero hyperparameter tuning recorded.
  3. Feature engineering absent from the live backend inference flow.
  4. Model learned an inverted relationship for safety stock due to flawed generative equation.

---

## 6. Current Backend APIs Audit

- `GET /medicines/`: Returns all medicine inventory records.
- `POST /prediction/{medicine_id}`: Runs XGBoost inference + per-sample SHAP values.
- `GET /prediction/history`: Fetches past prediction logs.
- `GET /inventory/`: Calculates static ROP and EOQ for inventory dashboard.
- `GET /suppliers/`: Calculates supplier ranking using static formula.
- `GET /suppliers/best`: Returns highest scoring supplier.
- `POST /assistant/chat`: Keyword string-matching responses from `chatbot.py`.
- `POST /auth/login`: Plaintext password check against hardcoded strings.
- `GET /dashboard/stats`: Aggregates inventory counts, high-risk items, alerts.

---

## 7. Current Security & Privacy Issues

1. **Hardcoded Credentials:** Cleartext strings `"admin123"` and `"pharma123"` in `auth.py`.
2. **Plaintext Passwords in Database:** SQLite `users` table stores raw passwords (`default="admin123"`).
3. **No Endpoint Authorization:** All CRUD, prediction, inventory, and supplier endpoints lack security dependencies (`Depends(get_current_user)`).
4. **No JWT / Token Revocation:** Successful login returns arbitrary JSON `{success: true, role: "Admin"}` without signed bearer tokens.
5. **Privacy Configuration:** No formal mechanism to prevent transmission of sensitive hospital inventory data to external LLMs.

---

## 8. Current Experimental Limitations

1. **Domain Contradiction in Ground Truth:** Positive coefficient on safety stock inverts supply-chain logic.
2. **Linear Dataset Separability:** Because the original generative formula is purely linear, Logistic Regression achieves near-perfect performance ($\approx 0.998$). A non-linear, realistic risk function with interaction terms is needed to reflect true supply chain non-linearities, or the linear fit must be explicitly reported.
3. **Missing Automated RAG Pipeline:** Lack of vector retrieval, embedding indices, and quantitative evaluation.
4. **Uncalibrated Supplier Scoring:** Linear offset heuristic rather than direction-aware normalized multi-criteria decision scoring.
5. **Static Inventory Evaluation:** No multi-period Monte Carlo simulation comparing stochastic stockout rates and inventory holding costs.

---

## 9. Files That Will Be Modified or Created

### 9.1 New Modules & Scripts
- `backend/app/ai/data_generation.py`: Reproducible synthetic data generation pipeline with corrected domain formulation and metadata export.
- `backend/app/ai/feature_engineering.py`: Reusable domain feature engineering module with epsilon protection.
- `backend/app/ai/preprocessing.py`: Scikit-learn Pipeline with train-only fitting and leakage prevention.
- `backend/app/ai/rag/`: Complete lightweight modular RAG pipeline:
  - `ingestion.py`
  - `chunking.py`
  - `embeddings.py`
  - `retriever.py`
  - `generator.py`
  - `pipeline.py`
  - `evaluation.py`
- `config/rag_config.yaml`: RAG pipeline configuration.
- `backend/app/security.py`: Password hashing (bcrypt) and JWT token validation.
- `run_all_experiments.py`: Master end-to-end automated experiment runner.
- `tests/`: Automated unit, integration, and reproducibility test suite.

### 9.2 Modified Existing Files
- `backend/app/ai/train_model.py`: Update to use modular generator, corrected ground-truth, pipeline preprocessing, and engineered features.
- `backend/app/ai/predict.py`: Support engineered features in live inference and consistent SHAP explanations.
- `backend/app/routes/auth.py`: Secure authentication with bcrypt and JWT tokens.
- `backend/app/routes/suppliers.py`: Direction-aware min-max normalization.
- `backend/app/routes/inventory.py`: Dynamic service-level safety stock calculation.
- `backend/app/routes/assistant.py`: Connect to the modular RAG pipeline.
- `backend/requirements.txt`: Add bcrypt, pyjwt, pyyaml, and RAG dependencies.
- `results/`: All required reports, matrices, tables, and manifest files.
- `figures/`: High-resolution IEEE-compliant figures in PDF and PNG formats.
