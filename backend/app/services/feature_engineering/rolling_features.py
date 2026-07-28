from typing import Dict, List

import pandas as pd


class RollingFeatureGenerator:
    """
    Service class for generating rolling statistics features for time-series
    forecasting.
    """

    def __init__(self, rolling_config: Dict[str, List[int]]):
        """
        Initialize the RollingFeatureGenerator.

        Args:
            rolling_config (Dict[str, List[int]]): A dictionary mapping column names
                to a list of rolling window sizes (integers).
                Example: {"sales": [3, 7, 14, 30]}
        """
        self.available_metrics = ["mean", "sum", "std", "min", "max", "median"]
        self._validate_config(rolling_config)
        self.rolling_config = rolling_config

    def _validate_config(self, rolling_config: Dict[str, List[int]]):
        if not isinstance(rolling_config, dict) or not rolling_config:
            raise ValueError("rolling_config must be a non-empty dictionary.")
        for col, windows in rolling_config.items():
            if not isinstance(windows, list):
                raise TypeError(
                    f"Windows for column '{col}' must be a list of integers."
                )
            for window in windows:
                if not isinstance(window, int) or window <= 0:
                    raise ValueError(
                        f"Invalid window value '{window}' for column '{col}'. "
                        "Windows must be positive integers."
                    )

    def _validate_input(self, df: pd.DataFrame) -> pd.DataFrame:
        if not isinstance(df, pd.DataFrame):
            raise TypeError("Input must be a pandas DataFrame.")
        if df.empty:
            raise ValueError("Input DataFrame is empty.")

        missing_cols = [
            col for col in self.rolling_config.keys() if col not in df.columns
        ]
        if missing_cols:
            raise ValueError(
                f"Missing required columns for rolling feature generation: "
                f"{missing_cols}"
            )

        return df.copy()

    def generate(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Generate rolling features and append them to the DataFrame.
        """
        df_out = self._validate_input(df)

        for col, windows in self.rolling_config.items():
            for window in windows:
                # pandas rolling object
                # Note: We can specify min_periods if desired,
                # default is the window size
                rolling_obj = df_out[col].rolling(window=window)

                df_out[f"{col}_rolling_mean_{window}"] = rolling_obj.mean()
                df_out[f"{col}_rolling_sum_{window}"] = rolling_obj.sum()
                df_out[f"{col}_rolling_std_{window}"] = rolling_obj.std()
                df_out[f"{col}_rolling_min_{window}"] = rolling_obj.min()
                df_out[f"{col}_rolling_max_{window}"] = rolling_obj.max()
                df_out[f"{col}_rolling_median_{window}"] = rolling_obj.median()

        return df_out
