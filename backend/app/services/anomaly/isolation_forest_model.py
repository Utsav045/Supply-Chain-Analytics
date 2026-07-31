import pickle
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest


class IsolationForestModel:
    """Isolation Forest model for anomaly detection."""

    def __init__(self, contamination: float = 0.05, random_state: int = 42):
        self.model = IsolationForest(
            contamination=contamination,
            random_state=random_state,
        )
        self.feature_name = None

    def fit(self, values: list[float], feature_name: str = "") -> None:
        """Train the Isolation Forest model."""

        data = np.asarray(values, dtype=float).reshape(-1, 1)
        self.model.fit(data)
        self.feature_name = feature_name

    def predict(self, values: list[float]) -> list[bool]:
        """Predict anomalies."""

        data = np.asarray(values, dtype=float).reshape(-1, 1)
        predictions = self.model.predict(data)

        # Isolation Forest returns:
        # 1  = Normal
        # -1 = Anomaly
        return [prediction == -1 for prediction in predictions]

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

    model = IsolationForestModel()
    model.fit(values, feature)

    model.save("models/anomaly/isolation_forest.pkl")

    loaded_model = IsolationForestModel.load("models/anomaly/isolation_forest.pkl")

    anomalies = loaded_model.predict(values)

    print(f"Dataset        : {csv_path}")
    print(f"Feature        : {feature}")
    print(f"Total Records  : {len(values)}")
    print(f"Anomalies      : {sum(anomalies)}")
    print("Model saved as : models/anomaly/isolation_forest.pkl")
