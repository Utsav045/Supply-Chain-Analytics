"""Tests for walk-forward forecasting validation."""

from collections.abc import Callable
from typing import cast

import pandas as pd
import pytest
from src.forecasting.backtesting import walk_forward_backtest
from src.forecasting.base import BaseForecaster
from src.forecasting.model_validation import ModelInputValidationError
from src.forecasting.moving_average import MovingAverageForecaster


@pytest.fixture
def demand_series() -> pd.Series:
    """Return regular historical demand."""
    return pd.Series(
        data=[
            10.0,
            12.0,
            14.0,
            16.0,
            18.0,
            20.0,
            22.0,
            24.0,
            26.0,
            28.0,
        ],
        index=pd.date_range(
            start="2026-01-01",
            periods=10,
            freq="D",
        ),
        name="demand",
        dtype=float,
    )


def test_backtest_returns_expected_prediction_count(
    demand_series: pd.Series,
) -> None:
    """Every observation after the initial window should be evaluated."""
    result = walk_forward_backtest(
        series=demand_series,
        model_factory=lambda: MovingAverageForecaster(window=3),
        initial_train_size=5,
    )

    assert len(result.predictions) == 5
    assert result.model_name == "moving_average_3"


def test_first_backtest_forecast_uses_only_prior_data(
    demand_series: pd.Series,
) -> None:
    """The first prediction must exclude the actual evaluation value."""
    result = walk_forward_backtest(
        series=demand_series,
        model_factory=lambda: MovingAverageForecaster(window=3),
        initial_train_size=5,
    )

    expected_prediction = (14 + 16 + 18) / 3

    assert result.predictions.iloc[0]["predicted_demand"] == pytest.approx(
        expected_prediction
    )

    assert result.predictions.index[0] == pd.Timestamp("2026-01-06")


def test_backtest_returns_evaluation_metrics(
    demand_series: pd.Series,
) -> None:
    """Backtesting should calculate all project metrics."""
    result = walk_forward_backtest(
        series=demand_series,
        model_factory=lambda: MovingAverageForecaster(window=3),
        initial_train_size=5,
    )

    assert set(result.metrics) == {
        "mae",
        "mape",
        "mse",
        "rmse",
        "r2",
    }

    assert result.metrics["mae"] is not None
    assert result.metrics["rmse"] is not None


def test_backtest_accepts_aligned_exogenous_features(
    demand_series: pd.Series,
) -> None:
    """External variables should be supplied to each model window."""
    exogenous = pd.DataFrame(
        {
            "price": [50.0] * 10,
            "promotion": [0.0] * 8 + [1.0, 1.0],
        },
        index=demand_series.index,
    )

    result = walk_forward_backtest(
        series=demand_series,
        model_factory=lambda: MovingAverageForecaster(window=3),
        initial_train_size=5,
        exogenous=exogenous,
    )

    assert len(result.predictions) == 5


@pytest.mark.parametrize(
    "invalid_size",
    [0, 1, 2, 10, 11, 2.5, True],
)
def test_invalid_initial_train_size_is_rejected(
    demand_series: pd.Series,
    invalid_size: object,
) -> None:
    """The first training window must be valid."""
    with pytest.raises(ModelInputValidationError):
        walk_forward_backtest(
            series=demand_series,
            model_factory=lambda: MovingAverageForecaster(window=3),
            initial_train_size=invalid_size,  # type: ignore[arg-type]
        )


def test_invalid_model_factory_is_rejected(
    demand_series: pd.Series,
) -> None:
    """The factory must produce a compatible forecasting model."""
    invalid_factory = cast(
        Callable[[], BaseForecaster],
        lambda: object(),
    )

    with pytest.raises(
        ModelInputValidationError,
        match="BaseForecaster",
    ):
        walk_forward_backtest(
            series=demand_series,
            model_factory=invalid_factory,
            initial_train_size=5,
        )


def test_misaligned_exogenous_data_is_rejected(
    demand_series: pd.Series,
) -> None:
    """External variables must share the demand index."""
    exogenous = pd.DataFrame(
        {
            "price": [50.0] * 10,
        },
        index=pd.date_range(
            start="2026-02-01",
            periods=10,
            freq="D",
        ),
    )

    with pytest.raises(
        ModelInputValidationError,
        match="must match",
    ):
        walk_forward_backtest(
            series=demand_series,
            model_factory=lambda: MovingAverageForecaster(window=3),
            initial_train_size=5,
            exogenous=exogenous,
        )
