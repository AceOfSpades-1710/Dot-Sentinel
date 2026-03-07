import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin

class DummyModel(BaseEstimator, ClassifierMixin):
    def predict(self, X):
        return np.zeros(X.shape[0])
    def predict_proba(self, X):
        # Return probability for class 0 and 1
        probs = np.random.rand(X.shape[0], 2)
        return probs / probs.sum(axis=1, keepdims=True)

class DummyAnomalyModel(BaseEstimator):
    def predict(self, X):
        return np.random.uniform(-1, 1, X.shape[0])
        
    def decision_function(self, X):
        return self.predict(X)
