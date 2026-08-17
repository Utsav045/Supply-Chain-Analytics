"""Stationarity diagnostics for demand time series."""

from dataclasses import dataclass

import pandas as pd
from statsmodels.tsa.stattools import adfuller

from src.forecasting.model_validation import (
    ModelInputValidationError,
    validate_demand_series,
)


@dataclass(frozen=True, slots=True)
class StationarityResult:
    """Contain Augmented Dickey-Fuller test results."""

    test_statistic: float
    p_value: float
    used_lags: int
    observations: int
    critical_values: dict[str, float]
    information_criterion: float | None
    significance_level: float
    is_stationary: bool


def run_adf_test(
    series: pd.Series,
    significance_level: float = 0.05,
    max_lag: int | None = None,
) -> StationarityResult:
    """
    Run the Augmented Dickey-Fuller stationarity test.

    Args:
        series: Demand series to examine.
        significance_level: Threshold used to reject the unit-root null.
        max_lag: Optional maximum lag supplied to the test.

    Returns:
        Structured ADF test results.

    Raises:
        ModelInputValidationError: If the configuration or series is invalid.
    """
    if isinstance(significance_level, bool) or not isinstance(
        significance_level,
        int | float,
    ):
        raise ModelInputValidationError("significance_level must be numeric.")

    validated_significance = float(significance_level)

    if not 0 < validated_significance < 1:
        raise ModelInputValidationError(
            "significance_level must be between zero and one."
        )

    if max_lag is not None:
        if not isinstance(max_lag, int) or isinstance(
            max_lag,
            bool,
        ):
            raise ModelInputValidationError("max_lag must be an integer or None.")

        if max_lag < 0:
            raise ModelInputValidationError("max_lag cannot be negative.")

    validated_series = validate_demand_series(
        series,
        minimum_observations=10,
    )

    if validated_series.nunique() <= 1:
        raise ModelInputValidationError(
            "Stationarity testing requires a non-constant series."
        )

    try:
        result = adfuller(
            validated_series.to_numpy(dtype=float),
            maxlag=max_lag,
            regression="c",
            autolag="AIC",
        )
    except ValueError as exc:
        raise ModelInputValidationError(
            "Unable to complete the stationarity test."
        ) from exc

    test_statistic = float(result[0])
    p_value = float(result[1])
    used_lags = int(result[2])
    observations = int(result[3])

    critical_values = {str(level): float(value) for level, value in result[4].items()}

    information_criterion = float(result[5]) if len(result) > 5 else None

    return StationarityResult(
        test_statistic=test_statistic,
        p_value=p_value,
        used_lags=used_lags,
        observations=observations,
        critical_values=critical_values,
        information_criterion=information_criterion,
        significance_level=validated_significance,
        is_stationary=p_value < validated_significance,
    )


def difference_series(
    series: pd.Series,
    periods: int = 1,
) -> pd.Series:
    """
    Difference a demand series to reduce trend or non-stationarity.

    Args:
        series: Historical demand series.
        periods: Number of preceding periods used for differencing.

    Returns:
        Differenced demand series without missing values.
    """
    if not isinstance(periods, int) or isinstance(periods, bool):
        raise ModelInputValidationError("Differencing periods must be an integer.")

    if periods <= 0:
        raise ModelInputValidationError(
            "Differencing periods must be greater than zero."
        )

    validated_series = validate_demand_series(
        series,
        minimum_observations=periods + 2,
    )

    if periods >= len(validated_series):
        raise ModelInputValidationError(
            "Differencing periods must be smaller than the series."
        )

    differenced = validated_series.diff(periods=periods).dropna()
    differenced.name = f"{validated_series.name}_diff_{periods}"

    return differenced
