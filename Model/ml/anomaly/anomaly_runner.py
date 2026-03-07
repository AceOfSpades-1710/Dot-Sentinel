import pandas as pd
from anomaly.anomaly_model import AnomalyDetector
from preprocessing import preprocess_data

def run_anomaly(csv_path, model_path):
    df = pd.read_csv(csv_path)

    X, _, _ = preprocess_data(df, fit=False)

    detector = AnomalyDetector(model_path)
    scores = detector.score(X)

    return scores
