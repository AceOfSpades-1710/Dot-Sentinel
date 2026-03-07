import joblib
import numpy as np

class AnomalyDetector:
    """
    Unsupervised anomaly detector wrapper
    """

    def __init__(self, model_path):
        self.model = joblib.load(model_path)

    def predict(self, X):
        return self.model.decision_function(X)

# Large positive	Highly anomalous
# Small / negative	Normal

    def average_score(self, X):
        """
        Returns a single average anomaly score for a group of flows.
        """
        scores = self.score(X)
        return float(np.mean(scores))
