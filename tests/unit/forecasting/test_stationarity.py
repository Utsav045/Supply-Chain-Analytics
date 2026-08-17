"""Tests for time-series stationarity diagnostics."""

import numpy as np
import pandas as pd
import pytest

from src.forecasting.model_validation import ModelInputValidationError
from src.forecasting.stationarity import difference_series, run_adf_test


@pytest.fixture
def stationary_series() -> pd.Series:
    """Return a reproducible stationary autoregressive series."""
    random_generator = np.random.default_rng(seed=42)
    noise = random_generator.normal(
        loc=0.0,
        scale=1.0,
        size=120,
    )

    values = np.zeros(120, dtype=float)

    for position in range(1, len(values)):
        values[position] = 0.30 * values[position - 1] + noise[position]

    return pd.Series(
        data=values + 20.0,
        index=pd.date_range(
            start="2026-01-01",
            periods=120,
            freq="D",
        ),
        name="demand",
        dtype=float,
    )


def test_adf_returns_structured_result(
    stationary_series: pd.Series,
) -> None:
    """The ADF utility should expose all required outputs."""
    result = run_adf_test(stationary_series)

    assert isinstance(result.test_statistic, float)
    assert isinstance(result.p_value, float)
    assert isinstance(result.used_lags, int)
    assert isinstance(result.observations, int)
    assert isinstance(result.critical_values, dict)
    assert result.significance_level == pytest.approx(0.05)


def test_stationary_series_is_identified(
    stationary_series: pd.Series,
) -> None:
    """A stable autoregressive process should reject the unit root."""
    result = run_adf_test(stationary_series)

    assert result.p_value < 0.05
    assert result.is_stationary is True


def test_difference_series_reduces_length(
    stationary_series: pd.Series,
) -> None:
    """First differencing should remove one observation."""
    result = difference_series(
        stationary_series,
        periods=1,
    )

    assert len(result) == len(stationary_series) - 1
    assert result.name == "demand_diff_1"


def test_difference_values_are_correct() -> None:
    """Differencing should subtract the preceding observation."""
    series = pd.Series(
        data=[10.0, 13.0, 18.0, 20.0],
        index=pd.date_range(
            start="2026-01-01",
            periods=4,
            freq="D",
        ),
        name="demand",
    )

    result = difference_series(series)

    assert result.tolist() == [3.0, 5.0, 2.0]


def test_constant_series_is_rejected() -> None:
    """ADF testing requires variation in observed demand."""
    series = pd.Series(
        data=[10.0] * 20,
        index=pd.date_range(
            start="2026-01-01",
            periods=20,
            freq="D",
        ),
        name="demand",
    )

    with pytest.raises(
        ModelInputValidationError,
        match="non-constant",
    ):
        run_adf_test(series)


@pytest.mark.parametrize(
    "invalid_level",
    [0, 1, -0.1, 1.1, True],
)
def test_invalid_significance_level_is_rejected(
    stationary_series: pd.Series,
    invalid_level: object,
) -> None:
    """Significance level must be strictly between zero and one."""
    with pytest.raises(ModelInputValidationError):
        run_adf_test(
            stationary_series,
            significance_level=invalid_level,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize(
    "invalid_periods",
    [0, -1, 2.5, True],
)
def test_invalid_differencing_period_is_rejected(
    stationary_series: pd.Series,
    invalid_periods: object,
) -> None:
    """Differencing periods must be positive integers."""
    with pytest.raises(ModelInputValidationError):
        difference_series(
            stationary_series,
            periods=invalid_periods,  # type: ignore[arg-type]
        )
