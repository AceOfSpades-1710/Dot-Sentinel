# ml/core/preprocessor.py

import os
import joblib

DROP_COLS = ["id", "srcip", "dstip", "stime", "ltime"]
CATEGORICAL_COLS = ["proto", "service", "state"]

class Preprocessor:
    def __init__(self, model_dir):
        self.encoder = joblib.load(os.path.join(model_dir, "encoder.pkl"))
        self.scaler = joblib.load(os.path.join(model_dir, "scaler.pkl"))

    def transform(self, df):
        df = df.copy()

        # Drop labels if present
        for col in ["label", "attack_cat"]:
            if col in df.columns:
                df.drop(col, axis=1, inplace=True)

        # Drop useless columns
        for col in DROP_COLS:
            if col in df.columns:
                df.drop(col, axis=1, inplace=True)

        # Encode categoricals
        df[CATEGORICAL_COLS] = self.encoder.transform(df[CATEGORICAL_COLS])

        # Scale
        X = self.scaler.transform(df)

        return X
