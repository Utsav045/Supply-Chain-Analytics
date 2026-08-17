"""Tests for forecasting model comparison."""

import pandas as pd
import pytest

from src.forecasting.backtesting import BacktestResult
from src.forecasting.model_comparison import (
    compare_backtest_results,
)
from src.forecasting.model_validation import (
    ModelInputValidationError,
)


def make_backtest_result(
    model_name: str,
    mae: float,
    mape: float,
    mse: float,
    rmse: float,
    r2: float,
) -> BacktestResult:
    """Build a minimal valid backtest result."""
    predictions = pd.DataFrame(
        {
            "actual_demand": [10.0, 12.0],
            "predicted_demand": [11.0, 11.5],
            "lower_bound": [9.0, 9.5],
            "upper_bound": [13.0, 13.5],
        },
        index=pd.date_range(
            start="2026-01-01",
            periods=2,
            freq="D",
        ),
    )

    return BacktestResult(
        model_name=model_name,
        predictions=predictions,
        metrics={
            "mae": mae,
            "mape": mape,
            "mse": mse,
            "rmse": rmse,
            "r2": r2,
        },
    )


def test_lowest_rmse_is_selected() -> None:
    """RMSE comparison should select the smallest value."""
    result = compare_backtest_results(
        [
            make_backtest_result(
                "moving_average_7",
                5.0,
                10.0,
                36.0,
                6.0,
                0.70,
            ),
            make_backtest_result(
                "arima_1_1_1",
                3.0,
                7.0,
                16.0,
                4.0,
                0.85,
            ),
        ],
        primary_metric="rmse",
    )

    assert result.best_model_name == "arima_1_1_1"
    assert result.ranking.iloc[0]["rank"] == 1
    assert result.ranking.iloc[0]["model_name"] == "arima_1_1_1"


def test_highest_r2_is_selected() -> None:
    """R-squared comparison should maximize the score."""
    result = compare_backtest_results(
        [
            make_backtest_result(
                "moving_average_7",
                4.0,
                9.0,
                25.0,
                5.0,
                0.60,
            ),
            make_backtest_result(
                "arima_1_0_0",
                4.5,
                10.0,
                30.0,
                5.5,
                0.90,
            ),
        ],
        primary_metric="r2",
    )

    assert result.best_model_name == "arima_1_0_0"


def test_primary_metric_is_normalized() -> None:
    """Metric names should be case-insensitive."""
    result = compare_backtest_results(
        [
            make_backtest_result(
                "moving_average_3",
                2.0,
                5.0,
                9.0,
                3.0,
                0.80,
            )
        ],
        primary_metric=" RMSE ",
    )

    assert result.primary_metric == "rmse"


def test_duplicate_model_results_are_rejected() -> None:
    """Every compared model must have a unique name."""
    duplicate = make_backtest_result(
        "arima_1_1_1",
        2.0,
        5.0,
        9.0,
        3.0,
        0.80,
    )

    with pytest.raises(
        ModelInputValidationError,
        match="Duplicate model",
    ):
        compare_backtest_results(
            [
                duplicate,
                duplicate,
            ]
        )


def test_empty_results_are_rejected() -> None:
    """Comparison requires at least one model result."""
    with pytest.raises(
        ModelInputValidationError,
        match="At least one",
    ):
        compare_backtest_results([])


def test_unsupported_metric_is_rejected() -> None:
    """Only recognized forecasting metrics can rank models."""
    result = make_backtest_result(
        "arima_1_1_1",
        2.0,
        5.0,
        9.0,
        3.0,
        0.80,
    )

    with pytest.raises(
        ModelInputValidationError,
        match="Unsupported comparison metric",
    ):
        compare_backtest_results(
            [result],
            primary_metric="accuracy",
        )


def test_unavailable_metric_is_rejected() -> None:
    """A missing primary metric cannot be used for selection."""
    result = make_backtest_result(
        "arima_1_1_1",
        2.0,
        5.0,
        9.0,
        3.0,
        0.80,
    )

    invalid_result = BacktestResult(
        model_name=result.model_name,
        predictions=result.predictions,
        metrics={
            **result.metrics,
            "mape": None,
        },
    )

    with pytest.raises(
        ModelInputValidationError,
        match="is unavailable",
    ):
        compare_backtest_results(
            [invalid_result],
            primary_metric="mape",
        )
