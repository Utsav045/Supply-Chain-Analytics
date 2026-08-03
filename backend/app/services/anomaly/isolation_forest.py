import os

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest

# ==========================
# Configuration
# ==========================

INPUT_FILE = "data/processed/clean_sales_data.csv"
OUTPUT_DIR = "data/processed"
OUTPUT_FILE = "isolation_forest_anomalies.csv"

CONTAMINATION = 0.05
RANDOM_STATE = 42


def detect_anomalies(df: pd.DataFrame) -> pd.DataFrame:
    """Detect anomalies using Isolation Forest."""

    numeric_columns = df.select_dtypes(include=[np.number]).columns

    if len(numeric_columns) == 0:
        raise ValueError("No numeric columns found.")

    feature = numeric_columns[0]

    model = IsolationForest(
        contamination=CONTAMINATION,
        random_state=RANDOM_STATE,
    )

    values = df[[feature]].fillna(df[feature].median())

    predictions = model.fit_predict(values)

    result = df.copy()
    result["is_anomaly"] = predictions == -1

    return result


def main():
    if not os.path.exists(INPUT_FILE):
        raise FileNotFoundError(f"{INPUT_FILE} not found.")

    df = pd.read_csv(INPUT_FILE)

    result = detect_anomalies(df)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILE)

    result.to_csv(output_path, index=False)

    print(f"Dataset loaded : {INPUT_FILE}")
    print(f"Rows           : {len(result)}")
    print(f"Anomalies      : {result['is_anomaly'].sum()}")
    print(f"Saved to       : {output_path}")


if __name__ == "__main__":
    main()
