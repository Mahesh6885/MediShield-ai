import pandas as pd
import random
import joblib
from xgboost import XGBClassifier

rows = []

for _ in range(5000):

    inventory = random.randint(5, 200)
    demand = random.randint(20, 220)
    lead_time = random.randint(1, 8)
    supplier_reliability = random.randint(60, 99)
    expiry_days = random.randint(15, 365)
    safety_stock = random.randint(5, 25)

    score = (
        demand * 0.45
        - inventory * 0.35
        + lead_time * 8
        - supplier_reliability * 0.3
        - expiry_days * 0.05
        + safety_stock * 2
    )

    shortage = 1 if score > 40 else 0

    rows.append([
        inventory,
        demand,
        lead_time,
        supplier_reliability,
        expiry_days,
        safety_stock,
        shortage
    ])

df = pd.DataFrame(rows, columns=[
    "inventory",
    "demand",
    "lead_time",
    "supplier_reliability",
    "expiry_days",
    "safety_stock",
    "shortage"
])

X = df.drop("shortage", axis=1)
y = df["shortage"]

model = XGBClassifier(
    n_estimators=150,
    max_depth=4,
    learning_rate=0.1,
    random_state=42
)

model.fit(X, y)

joblib.dump(model, "app/ai/xgboost_model.pkl")

print("XGBoost Model Trained Successfully!")