import sys
import os
import joblib
import pandas as pd
import numpy as np

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.insert(0, PROJECT_ROOT)

from ml.anomaly.anomaly_model import AnomalyDetector

# ---------------- CONFIG ---------------- #

# DATA_PATH = "data/unsw_sample.csv"
DATA_PATH = "D:/syllabus books VIT/Capstone/soc-intrusion-detection/data/raw/UNSW_NB15_training-set.csv"

MODEL_PATH = "ml/anomaly/models/anomaly_model.pkl"
ENCODER_PATH = "ml/anomaly/models/anomaly_encoder.pkl"
SCALER_PATH = "ml/anomaly/models/anomaly_scaler.pkl"

DROP_COLS = ["id", "srcip", "dstip", "stime", "ltime"]
CATEGORICAL_COLS = ["proto", "service", "state"]

# --------------------------------------- #

print("[*] Loading data...")
df = pd.read_csv(DATA_PATH)

# Remove labels if present
for col in ["label", "attack_cat"]:
    if col in df.columns:
        df.drop(col, axis=1, inplace=True)

# Drop unused cols
for col in DROP_COLS:
    if col in df.columns:
        df.drop(col, axis=1, inplace=True)

print("[*] Loading encoder & scaler...")
encoder = joblib.load(ENCODER_PATH)
scaler = joblib.load(SCALER_PATH)

df[CATEGORICAL_COLS] = encoder.transform(df[CATEGORICAL_COLS])
X = scaler.transform(df)

print("[*] Loading anomaly model...")
model = AnomalyDetector(MODEL_PATH)

print("[*] Computing anomaly scores...")
scores = model.score(X)

# print("\n--- ANOMALY SCORE STATS ---")
# print("Min:", np.min(scores))
# print("Max:", np.max(scores))
# print("Avg:", np.mean(scores))

print("\nSample scores:")
for i in range(5):
    print(f"Flow {i} → score: {scores[i]:.4f}")
