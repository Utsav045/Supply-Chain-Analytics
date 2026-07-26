"""Validation utilities for model-ready time-series inputs."""

from typing import cast

import numpy as np
import pandas as pd


class ModelInputValidationError(ValueError):
    """Raised when model-ready forecasting input is invalid."""


def infer_series_frequency(
    index: pd.DatetimeIndex,
) -> str:
    """
    Determine the regular frequency of a datetime index.

    Args:
        index: Chronological datetime index.

    Returns:
        A valid pandas frequency string.

    Raises:
        ModelInputValidationError: If frequency cannot be determined.
    """
    if not isinstance(index, pd.DatetimeIndex):
        raise ModelInputValidationError("Frequency inference requires a DatetimeIndex.")

    stored_frequency = index.freqstr

    if stored_frequency is not None:
        return stored_frequency

    if len(index) < 3:
        raise ModelInputValidationError(
            "At least three observations are required when the "
            "index has no stored frequency."
        )

    try:
        inferred_frequency = pd.infer_freq(index)
    except ValueError as exc:
        raise ModelInputValidationError(
            "Unable to infer the time-series frequency."
        ) from exc

    if inferred_frequency is None:
        raise ModelInputValidationError(
            "The demand series must have a regular time interval."
        )

    return inferred_frequency


def validate_demand_series(
    series: pd.Series,
    minimum_observations: int = 3,
) -> pd.Series:
    """
    Validate a univariate demand series before model training.

    Args:
        series: Historical demand indexed by date.
        minimum_observations: Minimum required number of observations.

    Returns:
        A sorted floating-point demand series.

    Raises:
        ModelInputValidationError: If the series is invalid.
    """
    if not isinstance(minimum_observations, int) or isinstance(
        minimum_observations,
        bool,
    ):
        raise ModelInputValidationError("minimum_observations must be an integer.")

    if minimum_observations <= 0:
        raise ModelInputValidationError(
            "minimum_observations must be greater than zero."
        )

    if not isinstance(series, pd.Series):
        raise ModelInputValidationError("Demand input must be a pandas Series.")

    if series.empty:
        raise ModelInputValidationError("Demand series cannot be empty.")

    if not isinstance(series.index, pd.DatetimeIndex):
        raise ModelInputValidationError("Demand series must use a DatetimeIndex.")

    datetime_index = pd.DatetimeIndex(series.index)

    if datetime_index.has_duplicates:
        raise ModelInputValidationError("Demand series contains duplicate timestamps.")

    validated = series.copy()
    validated.index = datetime_index
    validated = validated.sort_index()

    if len(validated) < minimum_observations:
        raise ModelInputValidationError(
            f"At least {minimum_observations} observations are required."
        )

    numeric_series = pd.to_numeric(
        validated,
        errors="coerce",
    )

    if not isinstance(numeric_series, pd.Series):
        raise ModelInputValidationError(
            "Demand input could not be converted to a pandas Series."
        )

    if numeric_series.isna().any():
        raise ModelInputValidationError(
            "Demand series contains missing or non-numeric values."
        )

    demand_values = numeric_series.to_numpy(dtype=float)

    if not np.isfinite(demand_values).all():
        raise ModelInputValidationError("Demand series contains infinite values.")

    if (demand_values < 0).any():
        raise ModelInputValidationError("Demand values cannot be negative.")

    validated_series = cast(
        pd.Series,
        numeric_series.astype(float),
    )

    validated_series.index = pd.DatetimeIndex(validated_series.index)

    infer_series_frequency(pd.DatetimeIndex(validated_series.index))

    validated_series.name = series.name or "demand"

    return validated_series


def validate_exogenous_features(
    dataframe: pd.DataFrame,
    expected_index: pd.DatetimeIndex,
) -> pd.DataFrame:
    """
    Validate numeric external forecasting variables.

    External variables may include price, inventory level, promotion,
    holiday indicators and other known regressors.

    Args:
        dataframe: External feature dataset.
        expected_index: Index that the features must match.

    Returns:
        Validated numeric external features.

    Raises:
        ModelInputValidationError: If the feature data is invalid.
    """
    if not isinstance(dataframe, pd.DataFrame):
        raise ModelInputValidationError("External features must be a pandas DataFrame.")

    if not isinstance(expected_index, pd.DatetimeIndex):
        raise ModelInputValidationError(
            "Expected feature dates must use a DatetimeIndex."
        )

    if dataframe.empty:
        raise ModelInputValidationError("External feature data cannot be empty.")

    if dataframe.columns.empty:
        raise ModelInputValidationError(
            "External feature data must contain at least one column."
        )

    if not isinstance(dataframe.index, pd.DatetimeIndex):
        raise ModelInputValidationError("External features must use a DatetimeIndex.")

    datetime_index = pd.DatetimeIndex(dataframe.index)

    if datetime_index.has_duplicates:
        raise ModelInputValidationError(
            "External features contain duplicate timestamps."
        )

    validated = dataframe.copy()
    validated.index = datetime_index
    validated = validated.sort_index()

    if not validated.index.equals(expected_index):
        raise ModelInputValidationError(
            "External feature dates must match the demand-series dates."
        )

    numeric_features = cast(
        pd.DataFrame,
        validated.apply(
            pd.to_numeric,
            errors="coerce",
        ),
    )

    if numeric_features.isna().any().any():
        raise ModelInputValidationError(
            "External features contain missing or non-numeric values."
        )

    feature_values = numeric_features.to_numpy(dtype=float)

    if not np.isfinite(feature_values).all():
        raise ModelInputValidationError("External features contain infinite values.")

    return cast(
        pd.DataFrame,
        numeric_features.astype(float),
    )


def validate_forecast_horizon(
    horizon: int,
    maximum_horizon: int = 365,
) -> int:
    """
    Validate the number of future periods to forecast.

    Args:
        horizon: Requested forecast horizon.
        maximum_horizon: Maximum supported forecast horizon.

    Returns:
        Validated forecast horizon.
    """
    if not isinstance(horizon, int) or isinstance(horizon, bool):
        raise ModelInputValidationError("Forecast horizon must be an integer.")

    if horizon <= 0:
        raise ModelInputValidationError("Forecast horizon must be greater than zero.")

    if horizon > maximum_horizon:
        raise ModelInputValidationError(
            f"Forecast horizon cannot exceed {maximum_horizon} periods."
        )

    return horizon


def validate_confidence_level(
    confidence_level: float,
) -> float:
    """
    Validate the forecast confidence level.

    Args:
        confidence_level: Requested confidence level.

    Returns:
        Validated confidence level.
    """
    if isinstance(confidence_level, bool) or not isinstance(
        confidence_level,
        int | float,
    ):
        raise ModelInputValidationError("Confidence level must be numeric.")

    validated = float(confidence_level)

    if not 0 < validated < 1:
        raise ModelInputValidationError(
            "Confidence level must be between zero and one."
        )

    return validated
