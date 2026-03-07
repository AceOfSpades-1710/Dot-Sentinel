# ml/core/model_loader.py

import os
import joblib

class ModelLoader:
    def __init__(self, model_dir):
        self.binary_model = joblib.load(os.path.join(model_dir, "binary_model.pkl"))
        self.multiclass_model = joblib.load(os.path.join(model_dir, "multiclass_model.pkl"))
