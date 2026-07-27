from typing import Any, Dict, Optional, Tuple

import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.tsa.seasonal import DecomposeResult, seasonal_decompose


class SeasonalDecomposer:
    """
    A service class for performing time-series decomposition into
    Trend, Seasonal, and Residual components.
    """

    def __init__(
        self, value_column: str, model: str = "additive", period: Optional[int] = None
    ):
        """
        Initialize the SeasonalDecomposer.

        Args:
            value_column (str): The name of the column containing the time series
                values.
            model (str): Type of seasonal component. 'additive' or 'multiplicative'.
            period (int, optional): Period of the series. Must be used if x is not a
                pandas object or if the index of x does not have a frequency.
        """
        self.value_column = value_column
        if model not in ["additive", "multiplicative"]:
            raise ValueError("Model must be either 'additive' or 'multiplicative'.")
        self.model = model
        self.period = period
        self.result: Optional[DecomposeResult] = None
        self.df: Optional[pd.DataFrame] = None

    def _validate_input(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Validate the input DataFrame.
        """
        if not isinstance(df, pd.DataFrame):
            raise TypeError("Input must be a pandas DataFrame.")
        if df.empty:
            raise ValueError("Input DataFrame is empty.")
        if self.value_column not in df.columns:
            raise ValueError(
                f"Value column '{self.value_column}' not found in DataFrame."
            )
        if not pd.api.types.is_datetime64_any_dtype(df.index):
            try:
                # Attempt to convert index to datetime if it's not already
                df = df.copy()
                df.index = pd.to_datetime(df.index)
            except Exception as e:
                raise ValueError(
                    "DataFrame index must be a DatetimeIndex or convertible to one."
                ) from e

        return df.copy()

    def _handle_missing_values(self, series: pd.Series) -> pd.Series:
        """
        Handle missing values in the series.
        """
        if series.isna().any():
            # Interpolate missing values
            series = series.interpolate(method="time")
            # If any NaNs remain at the beginning/end, forward/back fill
            series = series.bfill().ffill()
        return series

    def decompose_series(self, df: pd.DataFrame) -> Dict[str, pd.Series]:
        """
        Decompose the time series.

        Args:
            df (pd.DataFrame): The input DataFrame.

        Returns:
            Dict[str, pd.Series]: A dictionary containing observed, trend,
                seasonal, and residual components.
        """
        validated_df = self._validate_input(df)
        self.df = validated_df

        series = validated_df[self.value_column]
        series = self._handle_missing_values(series)

        # Determine period
        period = self.period
        if period is None:
            if (
                getattr(series.index, "inferred_freq", None) is not None
                or getattr(series.index, "freq", None) is not None
            ):
                pass  # statsmodels can figure it out
            else:
                period = 1  # fallback

        # Check sufficient observations. statsmodels requires at least 2 * period

        if period is not None and len(series) < 2 * period:
            raise ValueError(
                f"Insufficient observations. Need at least {2 * period} "
                f"for period {period}, got {len(series)}."
            )

        if self.model == "multiplicative" and (series <= 0).any():
            raise ValueError(
                "Multiplicative decomposition requires strictly positive values."
            )

        try:
            self.result = seasonal_decompose(
                series, model=self.model, period=period, extrapolate_trend="freq"
            )
        except ValueError as e:
            raise ValueError(f"Decomposition failed: {e}") from e

        return {
            "observed": self.result.observed,
            "trend": self.result.trend,
            "seasonal": self.result.seasonal,
            "resid": self.result.resid,
        }

    def get_trend(self) -> pd.Series:
        """Get the trend component."""
        if self.result is None:
            raise RuntimeError("Must call decompose_series first.")
        return self.result.trend

    def get_seasonality(self) -> pd.Series:
        """Get the seasonal component."""
        if self.result is None:
            raise RuntimeError("Must call decompose_series first.")
        return self.result.seasonal

    def get_residuals(self) -> pd.Series:
        """Get the residual component."""
        if self.result is None:
            raise RuntimeError("Must call decompose_series first.")
        return self.result.resid

    def reconstruct_series(self) -> pd.Series:
        """
        Reconstruct the series from its components.
        """
        if self.result is None:
            raise RuntimeError("Must call decompose_series first.")

        if self.model == "additive":
            reconstructed = self.result.trend + self.result.seasonal + self.result.resid
        else:
            reconstructed = self.result.trend * self.result.seasonal * self.result.resid

        return reconstructed

    def plot_components(self, figsize: Tuple[int, int] = (10, 8)) -> Any:
        """
        Plot the decomposition components.
        """
        if self.result is None:
            raise RuntimeError("Must call decompose_series first.")

        fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=figsize, sharex=True)

        self.result.observed.plot(ax=ax1)
        ax1.set_ylabel("Observed")

        self.result.trend.plot(ax=ax2)
        ax2.set_ylabel("Trend")

        self.result.seasonal.plot(ax=ax3)
        ax3.set_ylabel("Seasonal")

        self.result.resid.plot(ax=ax4)
        ax4.set_ylabel("Residual")

        plt.tight_layout()
        return fig
