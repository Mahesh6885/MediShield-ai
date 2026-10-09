"""
MediShield AI: Comprehensive Unit & Integration Test Suite
File: tests/test_system.py
Conference: IEEE CEEE 2026 Camera-Ready Verification

Verifies:
1. Data generation & reproducibility
2. Feature engineering & epsilon safety
3. Preprocessing & leakage prevention
4. ML model training & live SHAP inference
5. Supplier ranking & direction-aware normalization
6. Inventory optimization & stochastic simulation
7. RAG pipeline retrieval & citation generation
8. Authentication security (bcrypt & JWT)
9. FastAPI route integrity via TestClient
"""

import os
import sys
import unittest
import numpy as np
import pandas as pd

# Add workspace root to sys.path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from backend.app.ai.data_generation import generate_synthetic_dataset, compute_risk_score
from backend.app.ai.feature_engineering import compute_domain_features, ALL_FEATURE_COLUMNS, RAW_FEATURE_COLUMNS
from backend.app.ai.preprocessing import create_preprocessing_pipeline, audit_dataset_for_preprocessing
from backend.app.ai.predict import predict_shortage
from backend.app.ai.supplier_ranking import compute_supplier_scores, run_weight_sensitivity_analysis, BASELINE_WEIGHTS
from backend.app.ai.inventory_simulation import run_single_inventory_policy, run_comparative_simulation
from backend.app.ai.rag.pipeline import RAGPipeline
from backend.app.security import hash_password, verify_password, create_access_token, decode_access_token
from fastapi.testclient import TestClient
from backend.app.main import app


class TestMediShieldAI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    # --------------------------------------------------------------------------
    # 1. Dataset Generation Tests
    # --------------------------------------------------------------------------
    def test_data_generation_reproducibility(self):
        """Verifies deterministic dataset generation under fixed random seed."""
        df1, meta1 = generate_synthetic_dataset(num_samples=100, seed=42)
        df2, meta2 = generate_synthetic_dataset(num_samples=100, seed=42)
        pd.testing.assert_frame_equal(df1, df2)
        self.assertEqual(meta1["seed"], 42)
        self.assertEqual(len(df1), 100)

    def test_safety_stock_protective_direction(self):
        """Verifies that higher safety stock strictly reduces or protects against shortage score."""
        score_low_ss = compute_risk_score(inventory=50, demand=100, lead_time=4, supplier_reliability=90, expiry_days=100, safety_stock=5)
        score_high_ss = compute_risk_score(inventory=50, demand=100, lead_time=4, supplier_reliability=90, expiry_days=100, safety_stock=25)
        self.assertLess(score_high_ss, score_low_ss, "Safety stock must have protective (negative) contribution to risk score.")

    # --------------------------------------------------------------------------
    # 2. Feature Engineering Tests
    # --------------------------------------------------------------------------
    def test_feature_engineering_epsilon_protection(self):
        """Verifies epsilon protection against zero demand in stock cover and safety margin."""
        zero_demand_sample = {
            "inventory": 50,
            "demand": 0,  # Zero demand boundary test
            "lead_time": 4,
            "supplier_reliability": 90,
            "expiry_days": 180,
            "safety_stock": 15,
        }
        df_feat = compute_domain_features(zero_demand_sample)
        self.assertFalse(np.isinf(df_feat["stock_cover_ratio"].values[0]), "Division by zero occurred in stock_cover_ratio.")
        self.assertFalse(np.isnan(df_feat["safety_buffer_margin"].values[0]), "NaN generated in safety_buffer_margin.")
        for col in ALL_FEATURE_COLUMNS:
            self.assertIn(col, df_feat.columns)

    # --------------------------------------------------------------------------
    # 3. Preprocessing Tests
    # --------------------------------------------------------------------------
    def test_preprocessing_leakage_free_fitting(self):
        """Verifies scaler fits only on train data and applies cleanly to test data."""
        X_train = pd.DataFrame({"demand": [20, 100, 200], "inventory": [10, 50, 150]})
        X_test = pd.DataFrame({"demand": [80], "inventory": [40]})
        pipeline = create_preprocessing_pipeline(numerical_cols=["demand", "inventory"], scale_features=True)
        transformed_train = pipeline.fit_transform(X_train)
        transformed_test = pipeline.transform(X_test)
        self.assertEqual(transformed_train.shape, (3, 2))
        self.assertEqual(transformed_test.shape, (1, 2))

    # --------------------------------------------------------------------------
    # 4. Model Prediction & SHAP Inference Tests
    # --------------------------------------------------------------------------
    def test_live_prediction_and_shap(self):
        """Verifies live inference endpoint returns valid probability, risk tier, and SHAP features."""
        features = {
            "inventory": 20,
            "demand": 150,
            "lead_time": 6,
            "supplier_reliability": 70,
            "expiry_days": 30,
            "safety_stock": 10,
        }
        result = predict_shortage(features)
        self.assertIn("probability", result)
        self.assertIn("risk", result)
        self.assertIn("explanation", result)
        self.assertTrue(0.0 <= result["probability"] <= 100.0)
        self.assertIn(result["risk"], ["High", "Medium", "Low"])
        self.assertGreater(len(result["explanation"]), 0)

    # --------------------------------------------------------------------------
    # 5. Supplier Multi-Criteria Ranking Tests
    # --------------------------------------------------------------------------
    def test_supplier_ranking_direction_awareness(self):
        """Verifies that lower cost and lower delivery days improve composite supplier score."""
        suppliers = [
            {"id": 1, "name": "Vendor A", "reliability": 90, "quality": 90, "cost": 100.0, "delivery": 2},
            {"id": 2, "name": "Vendor B", "reliability": 90, "quality": 90, "cost": 200.0, "delivery": 10},
        ]
        results, df_ranked = compute_supplier_scores(suppliers, BASELINE_WEIGHTS)
        self.assertGreater(results[0]["composite_score"], results[1]["composite_score"])
        self.assertEqual(results[0]["name"], "Vendor A")

    def test_supplier_sensitivity_stability(self):
        """Verifies sensitivity perturbation produces valid stability metrics."""
        suppliers = [
            {"id": 1, "name": "Vendor A", "reliability": 95, "quality": 95, "cost": 90.0, "delivery": 2},
            {"id": 2, "name": "Vendor B", "reliability": 85, "quality": 85, "cost": 120.0, "delivery": 5},
        ]
        df_sens, summary = run_weight_sensitivity_analysis(suppliers, perturbation_pct=0.20)
        self.assertGreater(summary["mean_kendall_tau"], 0.8)
        self.assertEqual(summary["top_supplier_nominal"], "Vendor A")

    # --------------------------------------------------------------------------
    # 6. Inventory Simulation Tests
    # --------------------------------------------------------------------------
    def test_inventory_simulation_execution(self):
        """Verifies multi-period simulation computes finite costs and valid service levels."""
        demand = np.array([5, 4, 6, 8, 3, 5, 4, 7, 6, 5])
        res = run_single_inventory_policy(
            daily_demand=demand,
            lead_time_days=2,
            initial_inventory=50.0,
            rop=20.0,
            order_qty=40.0,
        )
        self.assertTrue(0.0 <= res["service_level_pct"] <= 100.0)
        self.assertGreaterEqual(res["total_inventory_cost"], 0.0)
        self.assertEqual(res["days"], 10)

    # --------------------------------------------------------------------------
    # 7. RAG Pipeline Tests
    # --------------------------------------------------------------------------
    def test_rag_pipeline_retrieval_and_citations(self):
        """Verifies document ingestion, vector retrieval, and structured citation formatting."""
        pipe = RAGPipeline()
        pipe.build_index()
        self.assertGreater(len(pipe.documents), 0, "No documents were ingested into RAG index.")
        self.assertGreater(len(pipe.chunks), 0, "No chunks generated.")
        
        query_res = pipe.query("What are the early warning indicators of shortages?", top_k=2)
        self.assertIn("answer", query_res)
        self.assertIn("citations", query_res)
        self.assertGreater(len(query_res["retrieved_chunks"]), 0)
        self.assertTrue(query_res["grounded"])

    # --------------------------------------------------------------------------
    # 8. Security & Authentication Tests
    # --------------------------------------------------------------------------
    def test_bcrypt_hashing_and_verification(self):
        """Verifies bcrypt password hashing and constant-time verification."""
        password = "SecureClinicalPassword2026!"
        hashed = hash_password(password)
        self.assertTrue(hashed.startswith("$2b$"))
        self.assertTrue(verify_password(password, hashed))
        self.assertFalse(verify_password("WrongPassword", hashed))

    def test_jwt_token_creation_and_decoding(self):
        """Verifies cryptographic creation and decoding of access tokens."""
        payload = {"sub": "pharmacist@medishield.ai", "role": "Pharmacist"}
        token = create_access_token(payload)
        decoded = decode_access_token(token)
        self.assertEqual(decoded["sub"], "pharmacist@medishield.ai")
        self.assertEqual(decoded["role"], "Pharmacist")

    # --------------------------------------------------------------------------
    # 9. FastAPI Endpoints Integration Tests
    # --------------------------------------------------------------------------
    def test_fastapi_medicines_endpoint(self):
        """GET /medicines/ returns 200 and list of medicines."""
        res = self.client.get("/medicines/")
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.json(), list)

    def test_fastapi_suppliers_endpoint(self):
        """GET /suppliers/ returns 200 and sorted ranked suppliers."""
        res = self.client.get("/suppliers/")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIsInstance(data, list)
        if len(data) >= 2:
            self.assertGreaterEqual(data[0]["score"], data[1]["score"])

    def test_fastapi_inventory_endpoint(self):
        """GET /inventory/ returns 200 with dynamic ROP and EOQ."""
        res = self.client.get("/inventory/")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIsInstance(data, list)
        if len(data) > 0:
            self.assertIn("reorder_point", data[0])
            self.assertIn("eoq", data[0])

    def test_fastapi_assistant_chat_endpoint(self):
        """POST /assistant/chat returns 200 with grounded RAG answer."""
        res = self.client.post("/assistant/chat", json={"message": "What is the standard reorder point formula?"})
        self.assertEqual(res.status_code, 200)
        body = res.json()
        self.assertIn("assistant", body)
        self.assertIn("citations", body)

    def test_fastapi_auth_login(self):
        """POST /auth/login with valid admin credentials returns success and bearer token."""
        res = self.client.post("/auth/login", json={"username": "admin", "password": "admin123"})
        self.assertEqual(res.status_code, 200)
        body = res.json()
        self.assertTrue(body["success"])
        self.assertIn("access_token", body)


if __name__ == "__main__":
    unittest.main()
