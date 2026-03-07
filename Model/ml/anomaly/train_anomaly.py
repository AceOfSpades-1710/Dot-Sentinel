import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.insert(0, PROJECT_ROOT)

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_PATH = os.path.join(BASE_DIR, "data", "raw", "UNSW_NB15_training-set.csv")


import pandas as pd
import joblib
from ml.preprocessing import preprocess_data
from sklearn.ensemble import IsolationForest

# -------------- CONFIG ---------------- #

# DATA_PATH = "data/unsw_sample.csv"
#DATA_PATH = "D:/syllabus books VIT/Capstone/soc-intrusion-detection/data/raw/UNSW_NB15_training-set.csv"

MODEL_DIR = "ml/anomaly/models"
MODEL_PATH = os.path.join(MODEL_DIR, "anomaly_model.pkl")

os.makedirs(MODEL_DIR, exist_ok=True)

# -------------------------------------- #

print("[*] Loading data...")
df = pd.read_csv(DATA_PATH)

# Use only normal flows for training
if "label" in df.columns:
    df_normal = df[df["label"] == 0]
else:
    df_normal = df.copy()

print(f"[*] Normal samples: {len(df_normal)}")

print("[*] Preprocessing...")
X, _, _ = preprocess_data(df_normal, fit=False)

print("[*] Training Isolation Forest...")
model = IsolationForest(
    n_estimators=200,
    contamination=0.05,
    random_state=42,
    n_jobs=-1
)
model.fit(X)

joblib.dump(model, MODEL_PATH)
print(f"[+] Anomaly model saved: {MODEL_PATH}")
