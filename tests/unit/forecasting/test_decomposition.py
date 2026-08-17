"""Tests for demand time-series decomposition."""

import numpy as np
import pandas as pd
import pytest
from src.forecasting.decomposition import decompose_time_series
from src.forecasting.model_validation import ModelInputValidationError


@pytest.fixture
def seasonal_demand() -> pd.Series:
    """Return demand containing trend and weekly seasonality."""
    periods = 42
    positions = np.arange(periods)

    trend = 20.0 + (positions * 0.25)
    weekly_pattern = np.array([0.0, 2.0, 4.0, 3.0, 1.0, -1.0, -2.0])
    seasonality = np.tile(
        weekly_pattern,
        periods // len(weekly_pattern),
    )

    values = trend + seasonality

    return pd.Series(
        data=values,
        index=pd.date_range(
            start="2026-01-01",
            periods=periods,
            freq="D",
        ),
        name="demand",
        dtype=float,
    )


def test_decomposition_returns_required_components(
    seasonal_demand: pd.Series,
) -> None:
    """Observed, trend, seasonal and residual columns should exist."""
    result = decompose_time_series(
        seasonal_demand,
        period=7,
    )

    assert list(result.columns) == [
        "observed",
        "trend",
        "seasonal",
        "residual",
    ]

    assert len(result) == len(seasonal_demand)


def test_observed_component_matches_original_series(
    seasonal_demand: pd.Series,
) -> None:
    """The observed component should retain historical demand."""
    result = decompose_time_series(
        seasonal_demand,
        period=7,
    )

    assert np.allclose(
        result["observed"].to_numpy(),
        seasonal_demand.to_numpy(),
    )


def test_trend_is_extrapolated_at_series_boundaries(
    seasonal_demand: pd.Series,
) -> None:
    """Trend extrapolation should avoid missing edge values."""
    result = decompose_time_series(
        seasonal_demand,
        period=7,
    )

    assert result["trend"].isna().sum() == 0


def test_multiplicative_decomposition_accepts_positive_data(
    seasonal_demand: pd.Series,
) -> None:
    """Positive demand can use multiplicative decomposition."""
    result = decompose_time_series(
        seasonal_demand,
        period=7,
        model="multiplicative",
    )

    assert len(result) == len(seasonal_demand)


def test_multiplicative_decomposition_rejects_zero() -> None:
    """Multiplicative decomposition cannot contain zero demand."""
    series = pd.Series(
        data=[0.0] + [10.0] * 20,
        index=pd.date_range(
            start="2026-01-01",
            periods=21,
            freq="D",
        ),
        name="demand",
    )

    with pytest.raises(
        ModelInputValidationError,
        match="positive values",
    ):
        decompose_time_series(
            series,
            period=7,
            model="multiplicative",
        )


def test_series_requires_two_complete_cycles() -> None:
    """Decomposition needs enough data for two seasonal cycles."""
    series = pd.Series(
        data=[10.0] * 10,
        index=pd.date_range(
            start="2026-01-01",
            periods=10,
            freq="D",
        ),
        name="demand",
    )

    with pytest.raises(
        ModelInputValidationError,
        match="At least 14 observations",
    ):
        decompose_time_series(
            series,
            period=7,
        )


@pytest.mark.parametrize(
    "invalid_model",
    [
        "unknown",
        "linear",
        "",
    ],
)
def test_invalid_decomposition_model_is_rejected(
    seasonal_demand: pd.Series,
    invalid_model: str,
) -> None:
    """Only additive and multiplicative models are supported."""
    with pytest.raises(
        ModelInputValidationError,
        match="additive or multiplicative",
    ):
        decompose_time_series(
            seasonal_demand,
            period=7,
            model=invalid_model,
        )


@pytest.mark.parametrize(
    "invalid_period",
    [0, 1, -1, 2.5, True],
)
def test_invalid_decomposition_period_is_rejected(
    seasonal_demand: pd.Series,
    invalid_period: object,
) -> None:
    """The seasonal period must be an integer of at least two."""
    with pytest.raises(ModelInputValidationError):
        decompose_time_series(
            seasonal_demand,
            period=invalid_period,  # type: ignore[arg-type]
        )
