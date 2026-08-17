import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest


def detect_anomalies(
    df: pd.DataFrame,
    contamination: float = 0.05,
    random_state: int = 42,
) -> pd.DataFrame:
    """
    Detect anomalies using the Isolation Forest algorithm.

    Args:
        df: Input DataFrame.
        contamination: Expected proportion of anomalies.
        random_state: Random seed for reproducibility.

    Returns:
        DataFrame with an 'anomaly' column.
    """

    result = df.copy()

    numeric_columns = result.select_dtypes(include=[np.number]).columns.tolist()

    if not numeric_columns:
        raise ValueError("No numeric columns found.")

    x = result[numeric_columns].copy()

    # Fill missing values with column median
    x = x.fillna(x.median())

    model = IsolationForest(
        contamination=contamination,
        random_state=random_state,
    )

    predictions = model.fit_predict(x)

    # IsolationForest returns:
    #  1  = normal
    # -1 = anomaly
    result["anomaly"] = (predictions == -1).astype(int)

    return result


if __name__ == "__main__":
    dataset = "data/processed/clean_sales_data.csv"

    dataframe = pd.read_csv(dataset)

    result = detect_anomalies(dataframe)

    print("=" * 45)
    print("Isolation Forest Anomaly Detection")
    print("=" * 45)
    print(f"Dataset   : {dataset}")
    print(f"Rows      : {len(result)}")
    print(f"Anomalies : {result['anomaly'].sum()}")
    print("=" * 45)
