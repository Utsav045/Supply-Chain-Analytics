"""Tests for automatic forecasting-model selection."""

import pandas as pd
import pytest
from src.forecasting.model_selector import AutomaticModelSelector
from src.forecasting.model_validation import ModelInputValidationError
from src.forecasting.moving_average import MovingAverageForecaster


@pytest.fixture
def increasing_demand() -> pd.Series:
    """Return steadily increasing daily demand."""
    return pd.Series(
        data=[float(value) for value in range(10, 50, 2)],
        index=pd.date_range(
            start="2026-01-01",
            periods=20,
            freq="D",
        ),
        name="demand",
        dtype=float,
    )


def test_selector_chooses_best_candidate(
    increasing_demand: pd.Series,
) -> None:
    """The smaller moving window should fit the trend better."""
    selector = AutomaticModelSelector(
        model_factories={
            "moving_average_2": (lambda: MovingAverageForecaster(window=2)),
            "moving_average_4": (lambda: MovingAverageForecaster(window=4)),
        },
        primary_metric="rmse",
    )

    result = selector.select(
        series=increasing_demand,
        initial_train_size=6,
    )

    assert result.selected_model_name == "moving_average_2"
    assert result.selected_model.is_fitted is True
    assert len(result.backtests) == 2
    assert result.failures == {}


def test_selected_model_can_generate_forecast(
    increasing_demand: pd.Series,
) -> None:
    """The final selected model should be fitted on all data."""
    selector = AutomaticModelSelector(
        model_factories={
            "moving_average_2": (lambda: MovingAverageForecaster(window=2)),
            "moving_average_5": (lambda: MovingAverageForecaster(window=5)),
        }
    )

    result = selector.select(
        series=increasing_demand,
        initial_train_size=7,
    )

    forecast = result.selected_model.predict(horizon=3)

    assert len(forecast) == 3
    assert forecast.index[0] == pd.Timestamp("2026-01-21")


def test_selector_records_failed_candidates(
    increasing_demand: pd.Series,
) -> None:
    """One failed candidate should not prevent selection."""
    selector = AutomaticModelSelector(
        model_factories={
            "moving_average_2": (lambda: MovingAverageForecaster(window=2)),
            "moving_average_50": (lambda: MovingAverageForecaster(window=50)),
        }
    )

    result = selector.select(
        series=increasing_demand,
        initial_train_size=6,
    )

    assert result.selected_model_name == "moving_average_2"
    assert "moving_average_50" in result.failures
    assert "moving_average_2" in result.backtests


def test_selector_rejects_empty_candidate_mapping() -> None:
    """Automatic selection requires at least one model."""
    with pytest.raises(
        ModelInputValidationError,
        match="At least one model factory",
    ):
        AutomaticModelSelector(model_factories={})


def test_selector_rejects_non_callable_factory() -> None:
    """Each registered candidate must have a callable factory."""
    with pytest.raises(
        ModelInputValidationError,
        match="must be callable",
    ):
        AutomaticModelSelector(
            model_factories={
                "invalid": object(),  # type: ignore[dict-item]
            }
        )


def test_selector_rejects_factory_name_mismatch(
    increasing_demand: pd.Series,
) -> None:
    """Registered names must match model-reported names."""
    selector = AutomaticModelSelector(
        model_factories={
            "incorrect_name": (lambda: MovingAverageForecaster(window=2)),
        }
    )

    with pytest.raises(
        ModelInputValidationError,
        match="Every forecasting candidate failed",
    ):
        selector.select(
            series=increasing_demand,
            initial_train_size=6,
        )


def test_selector_rejects_when_all_models_fail(
    increasing_demand: pd.Series,
) -> None:
    """Selection cannot succeed without one valid candidate."""
    selector = AutomaticModelSelector(
        model_factories={
            "moving_average_40": (lambda: MovingAverageForecaster(window=40)),
            "moving_average_50": (lambda: MovingAverageForecaster(window=50)),
        }
    )

    with pytest.raises(
        ModelInputValidationError,
        match="Every forecasting candidate failed",
    ):
        selector.select(
            series=increasing_demand,
            initial_train_size=6,
        )
