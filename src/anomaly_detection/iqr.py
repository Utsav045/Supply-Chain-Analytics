import os

import numpy as np
import pandas as pd


DATASET = "data/processed/clean_sales_data.csv"
OUTPUT = "data/processed/iqr_anomalies.csv"

FEATURE = None
MULTIPLIER = 1.5


def detect_anomalies(
    df: pd.DataFrame,
    multiplier: float = MULTIPLIER,
) -> pd.DataFrame:
    """
    Detect anomalies using the IQR method.

    Args:
        df: Input DataFrame.
        multiplier: IQR multiplier.

    Returns:
        DataFrame with an 'anomaly' column.
    """

    if df.empty:
        raise ValueError("Dataset is empty.")

    result = df.copy()

    numeric_columns = result.select_dtypes(
        include=[np.number]
    ).columns.tolist()

    if not numeric_columns:
        raise ValueError("No numeric columns found.")

    if FEATURE is None:
        ignore = [
            "order_id",
            "customer_id",
            "product_id",
            "supplier_id",
            "id",
        ]

        candidates = [
            column
            for column in numeric_columns
            if column.lower() not in ignore
        ]

        feature = (
            candidates[0]
            if candidates
            else numeric_columns[0]
        )
    else:
        if FEATURE not in result.columns:
            raise ValueError(
                f"Column '{FEATURE}' not found."
            )

        feature = FEATURE

    data = result[feature].fillna(
        result[feature].median()
    ).astype(float)

    q1 = data.quantile(0.25)
    q3 = data.quantile(0.75)

    iqr = q3 - q1

    lower_bound = q1 - (multiplier * iqr)
    upper_bound = q3 + (multiplier * iqr)

    result["anomaly"] = (
        (data < lower_bound)
        | (data > upper_bound)
    ).astype(int)

    return result


if __name__ == "__main__":
    if not os.path.exists(DATASET):
        raise FileNotFoundError(
            f"Dataset not found: {DATASET}"
        )

    dataframe = pd.read_csv(DATASET)

    result = detect_anomalies(dataframe)

    anomalies = result[result["anomaly"] == 1]

    os.makedirs(
        os.path.dirname(OUTPUT),
        exist_ok=True,
    )

    anomalies.to_csv(
        OUTPUT,
        index=False,
    )

    print("=" * 45)
    print("IQR Anomaly Detection")
    print("=" * 45)
    print(f"Dataset        : {DATASET}")
    print(f"Total Records  : {len(result)}")
    print(f"Anomalies      : {len(anomalies)}")
    print(f"Output File    : {OUTPUT}")
    print("=" * 45)