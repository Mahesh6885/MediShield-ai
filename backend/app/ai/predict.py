import joblib
import pandas as pd
import shap

model = joblib.load("app/ai/xgboost_model.pkl")
explainer = shap.TreeExplainer(model)

def predict_shortage(features: dict):

    df = pd.DataFrame([features])

    probability = float(model.predict_proba(df)[0][1])

    shap_values = explainer(df)

    explanation = []

    for name, value in zip(df.columns, shap_values.values[0]):
        explanation.append({
            "feature": name,
            "impact": round(float(value), 3)
        })

    explanation = sorted(
        explanation,
        key=lambda x: abs(x["impact"]),
        reverse=True
    )

    if probability >= 0.75:
        risk = "High"
    elif probability >= 0.45:
        risk = "Medium"
    else:
        risk = "Low"

    return {
        "probability": round(probability * 100, 2),
        "risk": risk,
        "explanation": explanation[:6]
    }