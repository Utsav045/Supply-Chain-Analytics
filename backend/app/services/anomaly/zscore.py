import os

import numpy as np
import pandas as pd
from scipy.stats import zscore

# ==========================
# Configuration
# ==========================
DATASET = "data/processed/clean_sales_data.csv"
OUTPUT = "data/processed/zscore_anomalies.csv"

# Set to None for automatic feature selection
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

    if candidates:
        feature = candidates[0]
    else:
        feature = numeric_columns[0]
else:
    if FEATURE not in df.columns:
        raise ValueError(f"Column '{FEATURE}' not found.")
    feature = FEATURE

# ==========================
# Handle Missing Values
# ==========================
data = df[feature].fillna(df[feature].median())

# ==========================
# Calculate Z-score
# ==========================
df["z_score"] = zscore(data)

# ==========================
# Detect Anomalies
# ==========================
df["anomaly"] = np.where(np.abs(df["z_score"]) > THRESHOLD, 1, 0)

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