import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder, StandardScaler

# ---------------- CONFIG ---------------- #

DROP_COLS = ["id", "srcip", "dstip", "stime", "ltime"]
CATEGORICAL_COLS = ["proto", "service", "state"]

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "model")
os.makedirs(MODEL_DIR, exist_ok=True)

ENCODER_PATH = os.path.join(MODEL_DIR, "encoder.pkl")
SCALER_PATH  = os.path.join(MODEL_DIR, "scaler.pkl")


# ---------------------------------------- #


def preprocess_data(df, fit=True):
    """
    Preprocess UNSW-NB15 data for ML models.

    Parameters:
    df   : pandas DataFrame
    fit  : True -> training data
           False -> test/inference data

    Returns:
    X             : processed features
    y_binary      : binary labels (0/1)
    y_multiclass  : attack category labels
    """

    df = df.copy()

    # ----------- LABELS ----------- #
    y_binary = df["label"]
    y_multiclass = df["attack_cat"]

    # Remove labels from feature set
    df.drop(["label", "attack_cat"], axis=1, inplace=True)

    # ----------- DROP USELESS COLS ----------- #
    for col in DROP_COLS:
        if col in df.columns:
            df.drop(col, axis=1, inplace=True)

    # ----------- ENCODE CATEGORICAL FEATURES ----------- #
    from sklearn.preprocessing import OrdinalEncoder


    if fit:
        encoder = OrdinalEncoder(
            handle_unknown="use_encoded_value",
            unknown_value=-1
    )
        df[CATEGORICAL_COLS] = encoder.fit_transform(df[CATEGORICAL_COLS])
        joblib.dump(encoder, ENCODER_PATH)
    else:
        encoder = joblib.load(ENCODER_PATH)
        df[CATEGORICAL_COLS] = encoder.transform(df[CATEGORICAL_COLS])


    # ----------- SCALE FEATURES ----------- #
    if fit:
        scaler = StandardScaler()
        X = scaler.fit_transform(df)
        joblib.dump(scaler, SCALER_PATH)
    else:
        scaler = joblib.load(SCALER_PATH)
        X = scaler.transform(df)

    return X, y_binary, y_multiclass
