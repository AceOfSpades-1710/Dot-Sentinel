# ml/supervised/detector.py

class SupervisedDetector:
    def __init__(self, binary_model, multiclass_model):
        self.binary_model = binary_model
        self.multiclass_model = multiclass_model

    def analyze(self, X):
        """
        X: scaled feature matrix (n_samples, n_features)
        Returns:
            attack_probs, attack_types
        """
        attack_probs = self.binary_model.predict_proba(X)[:, 1]
        attack_types = self.multiclass_model.predict(X)

        return attack_probs, attack_types
