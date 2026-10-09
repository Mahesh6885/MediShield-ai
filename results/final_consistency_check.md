# MediShield AI: Final Experimental Results Consistency Audit
**Date:** October 6, 2026
**Status:** AUTHORITATIVE AUDIT & VERIFICATION

---

## 1. Dataset Consistency Check
- [PASS] Dataset records: 5,000 observations (CSV == Metadata == 5000).
- [PASS] Class distribution: No Shortage = 1,996 (39.92%), Shortage = 3,004 (60.08%).
- [PASS] Ground truth label verification: Recalculated labels match CSV labels with 0 mismatches (100.0% formula fidelity).
- [PASS] Domain protective safety stock coefficient is exactly -2.0; threshold is -20.0.

## 2. Model Comparison Consistency Check
- [PASS] Logistic Regression: Accuracy = 0.9974 ± 0.0015 (perfect linear boundary tracking).
- [PASS] Decision Tree: Accuracy = 0.8758 ± 0.0061.
- [PASS] Random Forest: Accuracy = 0.9338 ± 0.0063.
- [PASS] XGBoost Default Raw: Accuracy = 0.9668 ± 0.0040.
- [PASS] XGBoost Engineered + Tuned: Accuracy = 0.9750 ± 0.0044, ROC-AUC = 0.9980 ± 0.0004, PR-AUC = 0.9987 ± 0.0002.
- [PASS] model_comparison.csv matches model_comparison.json within 1e-6.

## 3. Ablation Study Consistency Check
- [PASS] Config A (Raw + Default): Accuracy = 0.9668 ± 0.0040.
- [PASS] Config B (+ Engineered): Accuracy = 0.9708 ± 0.0045.
- [PASS] Config C (+ Tuned): Accuracy = 0.9750 ± 0.0044.
- [PASS] Config D (+ Imbalance Handling): Accuracy = 0.9736 ± 0.0024.
- [PASS] Trade-off verified: Imbalance handling does NOT claim accuracy gain (0.9736 < 0.9750); precision rises to 0.9787 while recall shifts to 0.9774.
- [PASS] ablation_results.csv matches ablation_results.json within 1e-6.

## 4. Confusion Matrix (Seed 42) Consistency Check
- [PASS] Confusion matrix counts: TN=388, FP=11, FN=9, TP=592, N=1,000.
- [PASS] Accuracy = 0.9800 (98.00%).
- [PASS] Precision = 0.9818 (98.18%).
- [PASS] Recall (Sensitivity) = 0.9850 (98.50%).
- [PASS] Specificity = 0.9724 (97.24%).
- [PASS] F1-Score = 0.9834, Balanced Accuracy = 0.9787.
- [PASS] ROC-AUC = 0.9987, PR-AUC = 0.9992.
- [PASS] confusion_matrix.csv matches confusion_matrix.json within 1e-6.

## 5. Inventory Simulation Consistency Check
- [PASS] Baseline: Cost = $1699.64 ± $22.63, Service Level = 100.0%, Stockout Days = 0.0.
- [PASS] Proposed: Cost = $1676.58 ± $16.62, Service Level = 99.9% ± 0.22%, Stockout Days = 0.2 ± 0.45.
- [PASS] Cost reduction programmatically calculated: exactly 1.36%.
- [PASS] Honest trade-off verified: Dynamic ROP slightly trades 0.2 stockout days for $23.06 holding cost reduction.

## 6. Supplier Ranking & Sensitivity Consistency Check
- [PASS] Nominal top supplier: Sun Pharma (Score = 80.00).
- [PASS] 200 Monte Carlo perturbation trials present in results/supplier_sensitivity_trials.csv.
- [PASS] Mean Kendall Tau = 1.000, Spearman Rho = 1.000.
- [PASS] Sun Pharma top-supplier stability = 100.0% across all 200 trials.
- [PASS] 9 deterministic scenario bounds accurately distinguished from 200 random trials.

## 7. RAG Benchmark Consistency Check
- [PASS] Retrieval Hit Rate = 90.00% (Top-3 relevance).
- [PASS] MRR = 0.8333.
- [PASS] Groundedness Ratio = 68.66%.
- [PASS] Citation Validity = 100.00%.
- [PASS] Latency = 15.05 ms.
- [PASS] 4 indexed documents physically verified in repository (WHO, FDA, ASHP, SOP).
- [PASS] Documents explicitly marked as project-authored technical synthesis.
- [PASS] Human evaluation status: Pending Clinical Review (unverified ratings avoided).

## 8. LaTeX Publication Tables Verification
- [PASS] dataset_summary.tex present and generated programmatically.
- [PASS] model_comparison.tex present and generated programmatically.
- [PASS] ablation.tex present and generated programmatically.
- [PASS] confusion_matrix.tex present and generated programmatically.
- [PASS] shap_features.tex present and generated programmatically.
- [PASS] supplier_ranking.tex present and generated programmatically.
- [PASS] inventory_comparison.tex present and generated programmatically.
- [PASS] rag_evaluation.tex present and generated programmatically.

## 9. Publication Figures Verification
- [PASS] confusion_matrix.pdf present (Vector PDF).
- [PASS] roc_curve.pdf present (Vector PDF).
- [PASS] pr_curve.pdf present (Vector PDF).
- [PASS] shap_global.pdf present (Vector PDF).
- [PASS] shap_local_high_risk.pdf present (Vector PDF).
- [PASS] shap_local_false_negative.pdf present (Vector PDF).
- [PASS] supplier_ranking.pdf present (Vector PDF).
- [PASS] inventory_stockout_comparison.pdf present (Vector PDF).
- [PASS] inventory_cost_comparison.pdf present (Vector PDF).
- [PASS] rag_retrieval_evaluation.pdf present (Vector PDF).
- [PASS] Stale figures cleanly removed / archived in figures/archive_stale/ (zero root clutter).

## 10. Comprehensive Workspace Stale Number Audit
- [PASS] Zero stale numbers found across all active results, tables, CSV, JSON, and Python files outside historical documentation.
- [PASS] Historical numbers safely quarantined in results/project_audit_before_changes.md and results/CHANGES_FROM_ORIGINAL_MODEL.md.

---
## 11. Final Verification Conclusion
**OVERALL RESULT: PERFECT CONSISTENCY (PASS)**
- 100% of numerical results reconcile directly with authoritative outputs.
- Zero discrepancies detected across CSV, JSON, Markdown, LaTeX, and Figures.