import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score

from preprocessing import preprocess_data


# ---------------- LOAD DATA ---------------- #

df_small = pd.read_csv(
    "C:/Users/Dell/Desktop/soc-intrusion detection/data/raw/UNSW_NB15_training-set.csv"
)

df_large = pd.read_csv(
    "C:/Users/Dell/Desktop/soc-intrusion detection/data/raw/UNSW_NB15_testing-set.csv"
)

# Assign based on size
if df_large.shape[0] > df_small.shape[0]:
    train_df = df_large
    test_df  = df_small
else:
    train_df = df_small
    test_df  = df_large

print("Train shape:", train_df.shape)
print("Test shape:", test_df.shape)


# ---------------- PREPROCESS ---------------- #

X_train, y_train, _ = preprocess_data(train_df, fit=True)
X_test, y_test, _   = preprocess_data(test_df, fit=False)


# ---------------- MODEL ---------------- #

binary_model = RandomForestClassifier(
    n_estimators=200,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1
)

binary_model.fit(X_train, y_train)


# ---------------- EVALUATION ---------------- #

y_pred = binary_model.predict(X_test)
y_prob = binary_model.predict_proba(X_test)[:, 1]

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("ROC-AUC:", roc_auc_score(y_test, y_prob))


# ---------------- SAVE MODEL ---------------- #

joblib.dump(binary_model, "models/binary_model.pkl")
print("\nBinary model saved successfully.")
