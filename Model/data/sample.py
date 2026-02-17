import pandas as pd

df = pd.read_csv("data/raw/UNSW_NB15_training-set.csv")

# Take 500 normal + 500 attack
normal = df[df["label"] == 0].sample(500, random_state=42)
attack = df[df["label"] == 1].sample(500, random_state=42)

sample_df = pd.concat([normal, attack]).sample(frac=1, random_state=42)

sample_df.to_csv("data/unsw_sample.csv", index=False)

print("Saved balanced sample with", len(sample_df), "rows")
