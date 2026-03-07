import pandas as pd
import joblib
import numpy as np

from preprocessing import preprocess_data

# ---------------- LOAD DATA ---------------- #

# Load the same UNSW files
df_small = pd.read_csv(
    "C:/Users/Dell/Desktop/soc-intrusion detection/data/raw/UNSW_NB15_training-set.csv"
)

df_large = pd.read_csv(
    "C:/Users/Dell/Desktop/soc-intrusion detection/data/raw/UNSW_NB15_testing-set.csv"
)

# Decide test set based on size (same logic as training)
if df_large.shape[0] > df_small.shape[0]:
    test_df = df_small
else:
    test_df = df_large

print("Test shape:", test_df.shape)

# ---------------- LOAD MODEL ---------------- #

binary_model = joblib.load("models/binary_model.pkl")

# ---------------- PREPROCESS TEST DATA ---------------- #

X_test, y_test, _ = preprocess_data(test_df, fit=False)

# ---------------- RANDOM SAMPLE TEST ---------------- #

print("\n🔍 Random prediction samples:\n")

idx = np.random.choice(len(X_test), 10, replace=False)

for i in idx:
    x = X_test[i].reshape(1, -1)

    pred = binary_model.predict(x)[0]
    prob = binary_model.predict_proba(x)[0][1]
    true = y_test.iloc[i]

    label_map = {0: "NORMAL", 1: "ATTACK"}

    print(
        f"True: {label_map[true]:7} | "
        f"Predicted: {label_map[pred]:7} | "
        f"Confidence: {prob:.3f}"
    )

# ---------------- EDGE CASE TESTS ---------------- #

print("\n🚨 Known ATTACK sample:")
attack_sample = test_df[test_df["label"] == 1].iloc[0]
X_attack, _, _ = preprocess_data(attack_sample.to_frame().T, fit=False)

print(
    "Prediction:",
    label_map[binary_model.predict(X_attack)[0]],
    "| Confidence:",
    binary_model.predict_proba(X_attack)[0][1]
)

print("\n🟢 Known NORMAL sample:")
normal_sample = test_df[test_df["label"] == 0].iloc[0]
X_normal, _, _ = preprocess_data(normal_sample.to_frame().T, fit=False)

print(
    "Prediction:",
    label_map[binary_model.predict(X_normal)[0]],
    "| Confidence:",
    binary_model.predict_proba(X_normal)[0][1]
)
