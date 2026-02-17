import pandas as pd
import joblib
import os

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

from preprocessing import preprocess_data

# ---------------- SAFETY ---------------- #
os.makedirs("models", exist_ok=True)

# ---------------- LOAD DATA ---------------- #

df_small = pd.read_csv(
    "C:/Users/Dell/Desktop/soc-intrusion detection/data/raw/UNSW_NB15_training-set.csv"
)

df_large = pd.read_csv(
    "C:/Users/Dell/Desktop/soc-intrusion detection/data/raw/UNSW_NB15_testing-set.csv"
)

# Decide train/test based on size
if df_large.shape[0] > df_small.shape[0]:
    train_df = df_large
    test_df  = df_small
else:
    train_df = df_small
    test_df  = df_large

print("Train shape:", train_df.shape)
print("Test shape:", test_df.shape)

# ---------------- FILTER ONLY ATTACKS ---------------- #

train_df = train_df[train_df["label"] == 1]
test_df  = test_df[test_df["label"] == 1]

print("Train ATTACK samples:", train_df.shape)
print("Test ATTACK samples:", test_df.shape)

# ---------------- PREPROCESS ---------------- #

X_train, _, y_train_mc = preprocess_data(train_df, fit=True)
X_test, _, y_test_mc   = preprocess_data(test_df, fit=False)

# ---------------- MODEL ---------------- #

multiclass_model = RandomForestClassifier(
    n_estimators=300,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1
)

multiclass_model.fit(X_train, y_train_mc)

# ---------------- EVALUATION ---------------- #

print("\nMulticlass Classification Report:")
print(classification_report(y_test_mc, multiclass_model.predict(X_test)))

# ---------------- SAVE MODEL ---------------- #

joblib.dump(multiclass_model, "models/multiclass_model.pkl")
print("\nMulticlass model saved successfully.")
