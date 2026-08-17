"""Tests for demand forecasting evaluation metrics."""

import math

import numpy as np
import pytest

from src.forecasting.metrics import (
    calculate_safe_mape,
    evaluate_forecast,
)


def test_evaluate_forecast_returns_required_metrics() -> None:
    """The evaluation result should contain all project metrics."""
    result = evaluate_forecast(
        actual=[100, 200, 300],
        predicted=[110, 190, 310],
    )

    assert set(result) == {
        "mae",
        "mape",
        "mse",
        "rmse",
        "r2",
    }


def test_evaluate_forecast_calculates_expected_errors() -> None:
    """MAE, MSE and RMSE should match known values."""
    result = evaluate_forecast(
        actual=[100, 200, 300],
        predicted=[110, 190, 310],
    )

    assert result["mae"] == pytest.approx(10.0)
    assert result["mse"] == pytest.approx(100.0)
    assert result["rmse"] == pytest.approx(10.0)
    assert result["mape"] == pytest.approx(6.111111, rel=1e-5)


def test_mape_excludes_zero_actual_values() -> None:
    """Zero actual demand should not cause division by zero."""
    result = calculate_safe_mape(
        actual=[0, 100, 200],
        predicted=[20, 90, 220],
    )

    assert result == pytest.approx(10.0)


def test_mape_is_none_when_every_actual_value_is_zero() -> None:
    """MAPE is undefined when all actual demand values are zero."""
    result = calculate_safe_mape(
        actual=[0, 0, 0],
        predicted=[5, 10, 15],
    )

    assert result is None


def test_constant_actual_values_return_no_r2() -> None:
    """R-squared should be omitted for a constant target."""
    result = evaluate_forecast(
        actual=[10, 10, 10],
        predicted=[9, 10, 11],
    )

    assert result["r2"] is None


def test_perfect_prediction_has_zero_error() -> None:
    """Perfect forecasts should produce zero error."""
    result = evaluate_forecast(
        actual=[10, 20, 30],
        predicted=[10, 20, 30],
    )

    assert result["mae"] == 0
    assert result["mse"] == 0
    assert result["rmse"] == 0
    assert result["mape"] == 0
    assert result["r2"] == pytest.approx(1.0)


def test_mismatched_shapes_are_rejected() -> None:
    """Actual and predicted arrays must have equal lengths."""
    with pytest.raises(
        ValueError,
        match="matching shapes",
    ):
        evaluate_forecast(
            actual=[10, 20, 30],
            predicted=[10, 20],
        )


def test_empty_metric_input_is_rejected() -> None:
    """Metric arrays cannot be empty."""
    with pytest.raises(
        ValueError,
        match="cannot be empty",
    ):
        evaluate_forecast(
            actual=[],
            predicted=[],
        )


@pytest.mark.parametrize(
    "invalid_value",
    [np.nan, np.inf, -np.inf],
)
def test_nonfinite_metric_input_is_rejected(
    invalid_value: float,
) -> None:
    """NaN and infinite metric values should fail validation."""
    with pytest.raises(
        ValueError,
        match="must be finite",
    ):
        evaluate_forecast(
            actual=[10, 20, invalid_value],
            predicted=[10, 20, 30],
        )


def test_metric_results_are_not_nan() -> None:
    """Ordinary evaluation results should contain valid numbers."""
    result = evaluate_forecast(
        actual=[10, 20, 30],
        predicted=[11, 19, 31],
    )

    for value in result.values():
        if value is not None:
            assert not math.isnan(value)
