"""Tests for model-ready forecasting input validation."""

import numpy as np
import pandas as pd
import pytest

from src.forecasting.model_validation import (
    ModelInputValidationError,
    infer_series_frequency,
    validate_confidence_level,
    validate_demand_series,
    validate_exogenous_features,
    validate_forecast_horizon,
)


@pytest.fixture
def daily_demand() -> pd.Series:
    """Return a valid daily demand series."""
    return pd.Series(
        data=[10.0, 12.0, 15.0, 11.0, 18.0, 20.0, 16.0],
        index=pd.date_range(
            start="2026-01-01",
            periods=7,
            freq="D",
        ),
        name="demand",
        dtype=float,
    )


def test_valid_demand_series_is_standardized(
    daily_demand: pd.Series,
) -> None:
    """Valid demand should be returned as floating-point data."""
    result = validate_demand_series(daily_demand)

    assert result.dtype == float
    assert result.name == "demand"
    assert result.index.is_monotonic_increasing


def test_series_is_sorted_chronologically(
    daily_demand: pd.Series,
) -> None:
    """Unsorted demand should be sorted during validation."""
    unsorted = daily_demand.sort_index(ascending=False)

    result = validate_demand_series(unsorted)

    assert result.index.is_monotonic_increasing


def test_non_datetime_index_is_rejected() -> None:
    """Demand series must use dates as its index."""
    series = pd.Series([10, 20, 30])

    with pytest.raises(
        ModelInputValidationError,
        match="DatetimeIndex",
    ):
        validate_demand_series(series)


def test_duplicate_timestamps_are_rejected() -> None:
    """Duplicate demand dates should fail validation."""
    series = pd.Series(
        data=[10, 12, 15],
        index=pd.DatetimeIndex(
            [
                "2026-01-01",
                "2026-01-01",
                "2026-01-02",
            ]
        ),
    )

    with pytest.raises(
        ModelInputValidationError,
        match="duplicate timestamps",
    ):
        validate_demand_series(series)


def test_missing_demand_is_rejected(
    daily_demand: pd.Series,
) -> None:
    """Missing target values should fail validation."""
    daily_demand.iloc[2] = np.nan

    with pytest.raises(
        ModelInputValidationError,
        match="missing or non-numeric",
    ):
        validate_demand_series(daily_demand)


def test_infinite_demand_is_rejected(
    daily_demand: pd.Series,
) -> None:
    """Infinite demand values should fail validation."""
    daily_demand.iloc[2] = np.inf

    with pytest.raises(
        ModelInputValidationError,
        match="infinite",
    ):
        validate_demand_series(daily_demand)


def test_negative_demand_is_rejected(
    daily_demand: pd.Series,
) -> None:
    """Negative demand values should fail validation."""
    daily_demand.iloc[2] = -5

    with pytest.raises(
        ModelInputValidationError,
        match="cannot be negative",
    ):
        validate_demand_series(daily_demand)


def test_irregular_frequency_is_rejected() -> None:
    """Irregularly spaced observations should fail validation."""
    series = pd.Series(
        data=[10, 15, 12, 20],
        index=pd.DatetimeIndex(
            [
                "2026-01-01",
                "2026-01-02",
                "2026-01-05",
                "2026-01-09",
            ]
        ),
    )

    with pytest.raises(
        ModelInputValidationError,
        match="regular time interval",
    ):
        validate_demand_series(series)


def test_daily_frequency_is_detected(
    daily_demand: pd.Series,
) -> None:
    """Daily series should produce a daily frequency."""
    frequency = infer_series_frequency(daily_demand.index)

    assert frequency == "D"


def test_valid_exogenous_features_are_accepted(
    daily_demand: pd.Series,
) -> None:
    """Numeric regressors with matching dates should pass."""
    features = pd.DataFrame(
        {
            "price": [50, 50, 52, 52, 55, 55, 55],
            "promotion": [0, 0, 1, 1, 0, 0, 0],
            "holiday": [0, 0, 0, 0, 0, 1, 0],
        },
        index=daily_demand.index,
    )

    result = validate_exogenous_features(
        features,
        expected_index=daily_demand.index,
    )

    assert result.shape == (7, 3)
    assert all(dtype == float for dtype in result.dtypes)


def test_exogenous_index_must_match_demand(
    daily_demand: pd.Series,
) -> None:
    """Regressor dates must align with target dates."""
    features = pd.DataFrame(
        {
            "price": [50, 51, 52],
        },
        index=pd.date_range(
            "2026-02-01",
            periods=3,
            freq="D",
        ),
    )

    with pytest.raises(
        ModelInputValidationError,
        match="must match",
    ):
        validate_exogenous_features(
            features,
            expected_index=daily_demand.index,
        )


@pytest.mark.parametrize(
    "invalid_horizon",
    [0, -1, 366, 2.5, True],
)
def test_invalid_forecast_horizon_is_rejected(
    invalid_horizon: object,
) -> None:
    """Invalid horizons should fail before prediction."""
    with pytest.raises(ModelInputValidationError):
        validate_forecast_horizon(invalid_horizon)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "invalid_confidence_level",
    [0, 1, -0.5, 1.5, True],
)
def test_invalid_confidence_level_is_rejected(
    invalid_confidence_level: object,
) -> None:
    """Confidence level must be strictly between zero and one."""
    with pytest.raises(ModelInputValidationError):
        validate_confidence_level(invalid_confidence_level)  # type: ignore[arg-type]
