from typing import List

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
import os


class AnomalyDetector:
    """Provides different anomaly detection methods."""

    @staticmethod
    def zscore(values: List[float], threshold: float = 3.0) -> List[bool]:

        if not values:
            return []

        data = np.array(values, dtype=float)

        mean = np.mean(data)
        std = np.std(data)

        if std == 0:
            return [False] * len(values)

        z_scores = np.abs((data - mean) / std)

        return [score > threshold for score in z_scores]


    @staticmethod
    def iqr(values: List[float], multiplier: float = 1.5) -> List[bool]:

        if not values:
            return []

        data = np.array(values, dtype=float)

        q1 = np.percentile(data, 25)
        q3 = np.percentile(data, 75)

        iqr = q3 - q1

        lower = q1 - multiplier * iqr
        upper = q3 + multiplier * iqr

        return [
            (x < lower) or (x > upper)
            for x in data
        ]


    @staticmethod
    def isolation_forest(
        values: List[float],
        contamination: float = 0.05
    ) -> List[bool]:

        if not values:
            return []

        data = np.array(values).reshape(-1,1)

        model = IsolationForest(
            contamination=contamination,
            random_state=42
        )

        prediction = model.fit_predict(data)

        return [
            True if x == -1 else False
            for x in prediction
        ]


    @staticmethod
    def detect(
        values: List[float],
        method: str = "z_score",
        threshold: float = 3.0,
        contamination: float = 0.05
    ) -> List[bool]:

        if method == "z_score":

            return AnomalyDetector.zscore(
                values,
                threshold
            )


        elif method == "iqr":

            return AnomalyDetector.iqr(
                values
            )


        elif method == "isolation_forest":

            return AnomalyDetector.isolation_forest(
                values,
                contamination
            )


        else:

            raise ValueError(
                f"Unsupported method: {method}"
            )



if __name__ == "__main__":


    # ==============================
    # SALES ANOMALY DETECTION
    # ==============================

    sales_df = pd.read_excel(
        "data/processed/clean_sales_data.xlsx"
    )


    print("Sales Columns:")
    print(sales_df.columns.tolist())


    # Revenue based anomaly detection

    sales_values = sales_df["revenue"].tolist()


    sales_df["is_anomaly"] = AnomalyDetector.detect(
        sales_values,
        method="z_score"
    )


    print("\nSales Data:")
    print(sales_df.head())



    # ==============================
    # INVENTORY ANOMALY DETECTION
    # ==============================

    inventory_df = pd.read_excel(
        "data/processed/clean_inventory_data.xlsx"
    )


    print("\nInventory Columns:")
    print(inventory_df.columns.tolist())


    # Using closing_stock as inventory value

    inventory_values = inventory_df[
        "closing_stock"
    ].tolist()


    inventory_df["is_anomaly"] = AnomalyDetector.detect(
        inventory_values,
        method="z_score"
    )


    print("\nInventory Data:")
    print(inventory_df.head())



    # ==============================
    # SAVE OUTPUT
    # ==============================

    os.makedirs(
        "artifacts",
        exist_ok=True
    )


    sales_df.to_excel(
        "artifacts/sales_anomaly_result.xlsx",
        index=False
    )


    inventory_df.to_excel(
        "artifacts/inventory_anomaly_result.xlsx",
        index=False
    )


    print(
        "\nAnomaly detection completed successfully."
    )