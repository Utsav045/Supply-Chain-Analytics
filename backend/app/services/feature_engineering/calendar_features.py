from typing import List

import pandas as pd


class CalendarFeatureGenerator:
    """
    Service class for generating date-based calendar features from a time-series index.
    """

    def __init__(self, features_to_generate: List[str] = None):
        """
        Initialize the CalendarFeatureGenerator.

        Args:
            features_to_generate (List[str], optional): List of features to generate.
                If None, all available features will be generated.
        """
        self.available_features = [
            "year",
            "quarter",
            "month",
            "week_of_year",
            "day_of_month",
            "day_of_week",
            "is_weekend",
            "is_month_start",
            "is_month_end",
            "is_quarter_start",
            "is_quarter_end",
            "is_year_start",
            "is_year_end",
        ]
        if features_to_generate is None:
            self.features_to_generate = self.available_features
        else:
            invalid_features = [
                f for f in features_to_generate if f not in self.available_features
            ]
            if invalid_features:
                raise ValueError(f"Invalid features requested: {invalid_features}")
            self.features_to_generate = features_to_generate

    def _validate_input(self, df: pd.DataFrame) -> pd.DataFrame:
        if not isinstance(df, pd.DataFrame):
            raise TypeError("Input must be a pandas DataFrame.")
        if df.empty:
            raise ValueError("Input DataFrame is empty.")
        if not pd.api.types.is_datetime64_any_dtype(df.index):
            try:
                df = df.copy()
                df.index = pd.to_datetime(df.index)
            except Exception as e:
                raise ValueError(
                    "DataFrame index must be a DatetimeIndex or convertible to one."
                ) from e
        return df.copy()

    def generate(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Generate calendar features and append them to the DataFrame.
        """
        df_out = self._validate_input(df)

        if "year" in self.features_to_generate:
            df_out["year"] = df_out.index.year
        if "quarter" in self.features_to_generate:
            df_out["quarter"] = df_out.index.quarter
        if "month" in self.features_to_generate:
            df_out["month"] = df_out.index.month
        if "week_of_year" in self.features_to_generate:
            df_out["week_of_year"] = df_out.index.isocalendar().week.astype(int)
        if "day_of_month" in self.features_to_generate:
            df_out["day_of_month"] = df_out.index.day
        if "day_of_week" in self.features_to_generate:
            df_out["day_of_week"] = df_out.index.dayofweek
        if "is_weekend" in self.features_to_generate:
            df_out["is_weekend"] = (df_out.index.dayofweek >= 5).astype(int)
        if "is_month_start" in self.features_to_generate:
            df_out["is_month_start"] = df_out.index.is_month_start.astype(int)
        if "is_month_end" in self.features_to_generate:
            df_out["is_month_end"] = df_out.index.is_month_end.astype(int)
        if "is_quarter_start" in self.features_to_generate:
            df_out["is_quarter_start"] = df_out.index.is_quarter_start.astype(int)
        if "is_quarter_end" in self.features_to_generate:
            df_out["is_quarter_end"] = df_out.index.is_quarter_end.astype(int)
        if "is_year_start" in self.features_to_generate:
            df_out["is_year_start"] = df_out.index.is_year_start.astype(int)
        if "is_year_end" in self.features_to_generate:
            df_out["is_year_end"] = df_out.index.is_year_end.astype(int)

        return df_out
