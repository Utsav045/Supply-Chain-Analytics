import numpy as np
import pandas as pd


def detect_anomalies(
    df: pd.DataFrame,
    threshold: float = 3.0,
) -> pd.DataFrame:
    """
    Detect anomalies using the Z-Score method.

    Args:
        df: Input DataFrame.
        threshold: Z-score threshold for anomaly detection.

    Returns:
        DataFrame with an 'anomaly' column.
    """

    result = df.copy()

    numeric_columns = result.select_dtypes(include=[np.number]).columns.tolist()

    if not numeric_columns:
        raise ValueError("No numeric columns found.")

    ignore = ["order_id", "customer_id", "product_id", "supplier_id", "id"]
    candidates = [c for c in numeric_columns if c.lower() not in ignore]
    feature = candidates[0] if candidates else numeric_columns[0]

    data = result[feature].fillna(result[feature].median()).astype(float)

    std = data.std()

    if std == 0:
        result["anomaly"] = 0
        return result

    z_scores = (data - data.mean()) / std

    result["anomaly"] = (np.abs(z_scores) > threshold).astype(int)

    return result


if __name__ == "__main__":
    dataset = "data/processed/clean_sales_data.csv"

    dataframe = pd.read_csv(dataset)

    result = detect_anomalies(dataframe)

    print("=" * 45)
    print("Z-Score Anomaly Detection")
    print("=" * 45)
    print(f"Dataset   : {dataset}")
    print(f"Rows      : {len(result)}")
    print(f"Anomalies : {result['anomaly'].sum()}")
    print("=" * 45)