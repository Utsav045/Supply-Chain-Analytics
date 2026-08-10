import pandas as pd

from .iqr import detect_anomalies as detect_iqr
from .isolation_forest import detect_anomalies as detect_isolation_forest
from .zscore import detect_anomalies as detect_zscore


class AnomalyDetector:
    """Run different anomaly detection algorithms."""

    @staticmethod
    def run(
        df: pd.DataFrame,
        method: str = "iqr",
    ) -> pd.DataFrame:
        """
        Run the selected anomaly detection method.

        Args:
            df: Input DataFrame.
            method: "iqr", "zscore", or "isolation_forest".

        Returns:
            DataFrame containing the anomaly results.

        Raises:
            ValueError: If the selected method is unsupported.
        """

        method = method.lower().strip()

        if method == "iqr":
            return detect_iqr(df)

        if method == "zscore":
            return detect_zscore(df)

        if method in ("isolation_forest", "iforest"):
            return detect_isolation_forest(df)

        raise ValueError(
            f"Unsupported method: {method}. "
            "Choose from: iqr, zscore, isolation_forest."
        )


if __name__ == "__main__":
    dataset = "data/processed/clean_sales_data.csv"

    dataframe = pd.read_csv(dataset)

    methods = (
        "iqr",
        "zscore",
        "isolation_forest",
    )

    for method in methods:
        result = AnomalyDetector.run(
            dataframe,
            method=method,
        )

        print("=" * 45)
        print(f"Method    : {method}")
        print(f"Dataset   : {dataset}")
        print(f"Rows      : {len(result)}")

        if "anomaly" in result.columns:
            print(f"Anomalies : {result['anomaly'].sum()}")

        print("=" * 45)