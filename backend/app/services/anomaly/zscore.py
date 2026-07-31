import os

import numpy as np
import pandas as pd

# ==========================
# Configuration
# ==========================
DATASET = "data/processed/clean_sales_data.csv"
OUTPUT = "data/processed/zscore_anomalies.csv"

FEATURE = None
THRESHOLD = 3

# ==========================
# Load Dataset
# ==========================
if not os.path.exists(DATASET):
    raise FileNotFoundError(f"Dataset not found: {DATASET}")

df = pd.read_csv(DATASET)

if df.empty:
    raise ValueError("Dataset is empty.")

# ==========================
# Select Feature
# ==========================
numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()

if not numeric_columns:
    raise ValueError("No numeric columns found.")

if FEATURE is None:
    ignore = ["order_id", "customer_id", "product_id", "supplier_id", "id"]
    candidates = [c for c in numeric_columns if c.lower() not in ignore]
    feature = candidates[0] if candidates else numeric_columns[0]
else:
    if FEATURE not in df.columns:
        raise ValueError(f"Column '{FEATURE}' not found.")
    feature = FEATURE

# ==========================
# Prepare Data
# ==========================
data = df[feature].fillna(df[feature].median()).astype(float)

mean = float(data.mean())
std = float(data.std(ddof=0))

if std == 0:
    raise ValueError(f"Column '{feature}' has zero standard deviation.")

# ==========================
# Calculate Z-Score
# ==========================
z_scores = (data - mean) / std

df["z_score"] = pd.Series(z_scores, index=df.index, dtype=float)

# ==========================
# Detect Anomalies
# ==========================
df["anomaly"] = (df["z_score"].abs() > THRESHOLD).astype(int)

anomalies = df[df["anomaly"] == 1]

# ==========================
# Save Results
# ==========================
os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
anomalies.to_csv(OUTPUT, index=False)

# ==========================
# Print Summary
# ==========================
print("=" * 45)
print("Z-Score Anomaly Detection")
print("=" * 45)
print(f"Dataset        : {DATASET}")
print(f"Feature        : {feature}")
print(f"Threshold      : ±{THRESHOLD}")
print(f"Total Records  : {len(df)}")
print(f"Anomalies      : {len(anomalies)}")
print(f"Output File    : {OUTPUT}")
print("=" * 45)
