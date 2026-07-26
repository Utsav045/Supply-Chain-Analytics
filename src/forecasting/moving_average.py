"""Moving Average baseline demand forecasting model."""

from dataclasses import dataclass, field
from statistics import NormalDist

import numpy as np
import pandas as pd
from pandas.tseries.frequencies import to_offset

from src.forecasting.base import BaseForecaster
from src.forecasting.model_validation import (
    infer_series_frequency,
    validate_confidence_level,
    validate_demand_series,
    validate_exogenous_features,
    validate_forecast_horizon,
)


@dataclass(slots=True)
class MovingAverageForecaster(BaseForecaster):
    """
    Forecast demand using the mean of recent observations.

    The model serves as the baseline against which ARIMA and Prophet
    performance will be compared.
    """

    window: int = 7
    _history: pd.Series | None = field(
        default=None,
        init=False,
        repr=False,
    )
    _frequency: str | None = field(
        default=None,
        init=False,
        repr=False,
    )
    _forecast_value: float | None = field(
        default=None,
        init=False,
        repr=False,
    )
    _window_standard_deviation: float | None = field(
        default=None,
        init=False,
        repr=False,
    )

    def __post_init__(self) -> None:
        """Validate Moving Average configuration."""
        if not isinstance(self.window, int) or isinstance(
            self.window,
            bool,
        ):
            raise TypeError("Moving Average window must be an integer.")

        if self.window <= 0:
            raise ValueError("Moving Average window must be greater than zero.")

    @property
    def model_name(self) -> str:
        """Return the configured baseline-model name."""
        return f"moving_average_{self.window}"

    @property
    def is_fitted(self) -> bool:
        """Return whether the model has been trained."""
        return (
            self._history is not None
            and self._frequency is not None
            and self._forecast_value is not None
        )

    def fit(
        self,
        series: pd.Series,
        exogenous: pd.DataFrame | None = None,
    ) -> "MovingAverageForecaster":
        """
        Fit the baseline using the most recent demand window.

        External features are validated for interface consistency but
        are not used by the Moving Average calculation.
        """
        validated = validate_demand_series(
            series,
            minimum_observations=self.window,
        )

        validated_index = pd.DatetimeIndex(validated.index)

        if exogenous is not None:
            validate_exogenous_features(
                exogenous,
                expected_index=validated_index,
            )

        recent_window = validated.iloc[-self.window :]

        self._history = validated
        self._frequency = infer_series_frequency(validated_index)
        self._forecast_value = max(
            float(recent_window.mean()),
            0.0,
        )

        if len(recent_window) > 1:
            self._window_standard_deviation = float(recent_window.std(ddof=1))
        else:
            self._window_standard_deviation = 0.0

        return self

    def predict(
        self,
        horizon: int,
        future_exogenous: pd.DataFrame | None = None,
        confidence_level: float = 0.95,
    ) -> pd.DataFrame:
        """
        Generate future Moving Average demand forecasts.

        Args:
            horizon: Number of future periods.
            future_exogenous: Optional future external variables.
            confidence_level: Confidence level for forecast bounds.

        Returns:
            Forecast with predicted demand and confidence bounds.
        """
        if not self.is_fitted:
            raise RuntimeError(
                "The Moving Average model must be fitted before prediction."
            )

        validated_horizon = validate_forecast_horizon(horizon)
        validated_confidence = validate_confidence_level(confidence_level)

        if (
            self._history is None
            or self._frequency is None
            or self._forecast_value is None
            or self._window_standard_deviation is None
        ):
            raise RuntimeError("The fitted Moving Average model state is incomplete.")

        offset = to_offset(self._frequency)

        future_index = pd.date_range(
            start=self._history.index[-1] + offset,
            periods=validated_horizon,
            freq=offset,
        )

        if future_exogenous is not None:
            validate_exogenous_features(
                future_exogenous,
                expected_index=future_index,
            )

        predicted_values = np.repeat(
            self._forecast_value,
            validated_horizon,
        )

        z_score = NormalDist().inv_cdf((1 + validated_confidence) / 2)

        margin = z_score * self._window_standard_deviation

        lower_bound = np.maximum(
            predicted_values - margin,
            0.0,
        )

        upper_bound = predicted_values + margin

        return pd.DataFrame(
            {
                "predicted_demand": predicted_values,
                "lower_bound": lower_bound,
                "upper_bound": upper_bound,
            },
            index=future_index,
        ).rename_axis("forecast_date")
