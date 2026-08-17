import pickle
from pathlib import Path

import numpy as np
import pandas as pd

Number = int | float


class IQRModel:
    """IQR model for anomaly detection."""

    def __init__(self, multiplier: float = 1.5):
        self.multiplier = multiplier
        self.q1 = None
        self.q3 = None
        self.iqr = None
        self.lower_bound = None
        self.upper_bound = None
        self.feature_name = None

    def fit(self, values: list[Number], feature_name: str = "") -> None:
        """Train the IQR model."""

        data = np.asarray(values, dtype=float)

        self.q1 = np.percentile(data, 25)
        self.q3 = np.percentile(data, 75)
        self.iqr = self.q3 - self.q1

        self.lower_bound = self.q1 - (self.multiplier * self.iqr)
        self.upper_bound = self.q3 + (self.multiplier * self.iqr)

        self.feature_name = feature_name

    def predict(self, values: list[Number]) -> list[bool]:
        """Predict anomalies."""

        if self.lower_bound is None or self.upper_bound is None:
            raise ValueError("Model has not been trained.")

        return [
            bool(value < self.lower_bound or value > self.upper_bound)
            for value in values
        ]

    def save(self, path: str) -> None:
        """Save model."""

        with open(path, "wb") as file:
            pickle.dump(self, file)

    @staticmethod
    def load(path: str):
        """Load model."""

        with open(path, "rb") as file:
            return pickle.load(file)


if __name__ == "__main__":
    csv_path = Path("data/processed/clean_sales_data.csv")

    df = pd.read_csv(csv_path)

    numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()

    if not numeric_columns:
        raise ValueError("No numeric columns found in the dataset.")

    feature = numeric_columns[0]

    values = df[feature].dropna().tolist()

    model = IQRModel()
    model.fit(values, feature)

    model.save("models/anomaly/iqr_model.pkl")

    loaded_model = IQRModel.load("models/anomaly/iqr_model.pkl")

    anomalies = loaded_model.predict(values)

    print(f"Dataset        : {csv_path}")
    print(f"Feature        : {feature}")
    print(f"Total Records  : {len(values)}")
    print(f"Anomalies      : {sum(anomalies)}")
    print("Model saved as : models/anomaly/iqr_model.pkl")
