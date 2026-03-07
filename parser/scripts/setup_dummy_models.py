import os
import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, OrdinalEncoder
import sys

# Add project root to path to import parser.dummy_definitions
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from parser.dummy_definitions import DummyModel, DummyAnomalyModel

def create_dummies():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # Go up from parser/scripts to Dot-Sentinel/Model
    MODEL_ROOT = os.path.join(os.path.dirname(os.path.dirname(BASE_DIR)), "Model")
    MODEL_DIR = os.path.join(MODEL_ROOT, "ml", "model")
    ANOMALY_DIR = os.path.join(MODEL_ROOT, "ml", "anomaly", "models")

    os.makedirs(MODEL_DIR, exist_ok=True)
    os.makedirs(ANOMALY_DIR, exist_ok=True)
    
    print(f"[*] Creating dummy models in {MODEL_DIR}")

    # 1. Create Scaler
    # Assume some features
    n_features = 42 # Approximation of UNSW-NB15 features (48 total - 6 dropped)
    scaler = StandardScaler()
    scaler.mean_ = np.zeros(n_features)
    scaler.scale_ = np.ones(n_features)
    scaler.var_ = np.ones(n_features)
    scaler.n_samples_seen_ = 100
    joblib.dump(scaler, os.path.join(MODEL_DIR, "scaler.pkl"))
    
    # 2. Create Encoder
    encoder = OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1)
    # Fit on some dummy categories
    df_cat = pd.DataFrame({
        "proto": ["tcp", "udp"],
        "service": ["http", "dns"],
        "state": ["FIN", "INT"]
    })
    encoder.fit(df_cat)
    joblib.dump(encoder, os.path.join(MODEL_DIR, "encoder.pkl"))

    # 3. Create Classifiers
    binary_model = DummyModel()
    joblib.dump(binary_model, os.path.join(MODEL_DIR, "binary_model.pkl"))

    multiclass_model = DummyModel()
    joblib.dump(multiclass_model, os.path.join(MODEL_DIR, "multiclass_model.pkl"))

    # 4. Create Anomaly Model
    anomaly_model = DummyAnomalyModel()
    joblib.dump(anomaly_model, os.path.join(ANOMALY_DIR, "anomaly_model.pkl"))
    
    print("[*] Dummy models created successfully.")

if __name__ == "__main__":
    create_dummies()
