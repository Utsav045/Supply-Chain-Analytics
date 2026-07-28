from typing import Dict, List

import pandas as pd


class LagFeatureGenerator:
    """
    Service class for generating lag features for time-series forecasting.
    """

    def __init__(self, lag_config: Dict[str, List[int]]):
        """
        Initialize the LagFeatureGenerator.

        Args:
            lag_config (Dict[str, List[int]]): A dictionary mapping column names
                to a list of lag periods (integers).
                Example: {"sales": [1, 7, 14, 30], "demand": [1]}
        """
        self._validate_config(lag_config)
        self.lag_config = lag_config

    def _validate_config(self, lag_config: Dict[str, List[int]]):
        if not isinstance(lag_config, dict) or not lag_config:
            raise ValueError("lag_config must be a non-empty dictionary.")
        for col, lags in lag_config.items():
            if not isinstance(lags, list):
                raise TypeError(f"Lags for column '{col}' must be a list of integers.")
            for lag in lags:
                if not isinstance(lag, int) or lag <= 0:
                    raise ValueError(
                        f"Invalid lag value '{lag}' for column '{col}'. "
                        "Lags must be positive integers."
                    )

    def _validate_input(self, df: pd.DataFrame) -> pd.DataFrame:
        if not isinstance(df, pd.DataFrame):
            raise TypeError("Input must be a pandas DataFrame.")
        if df.empty:
            raise ValueError("Input DataFrame is empty.")

        missing_cols = [col for col in self.lag_config.keys() if col not in df.columns]
        if missing_cols:
            raise ValueError(
                f"Missing required columns for lag generation: {missing_cols}"
            )

        return df.copy()

    def generate(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Generate lag features and append them to the DataFrame.
        """
        df_out = self._validate_input(df)

        for col, lags in self.lag_config.items():
            for lag in lags:
                feature_name = f"{col}_lag_{lag}"
                df_out[feature_name] = df_out[col].shift(lag)

        return df_out
