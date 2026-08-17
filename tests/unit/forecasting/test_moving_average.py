"""Tests for the Moving Average demand forecaster."""

import pandas as pd
import pytest

from src.forecasting.moving_average import MovingAverageForecaster


@pytest.fixture
def daily_demand() -> pd.Series:
    """Return ten days of historical demand."""
    return pd.Series(
        data=[10, 12, 11, 15, 13, 14, 16, 18, 20, 22],
        index=pd.date_range(
            start="2026-01-01",
            periods=10,
            freq="D",
        ),
        name="demand",
        dtype=float,
    )


def test_model_name_contains_window() -> None:
    """The model name should identify its configured window."""
    model = MovingAverageForecaster(window=7)

    assert model.model_name == "moving_average_7"


def test_new_model_is_not_fitted() -> None:
    """A new baseline model should start unfitted."""
    model = MovingAverageForecaster(window=3)

    assert model.is_fitted is False


def test_fit_marks_model_as_fitted(
    daily_demand: pd.Series,
) -> None:
    """Successful training should update fitted state."""
    model = MovingAverageForecaster(window=3)

    returned_model = model.fit(daily_demand)

    assert returned_model is model
    assert model.is_fitted is True


def test_forecast_uses_recent_window_mean(
    daily_demand: pd.Series,
) -> None:
    """Prediction should equal the final window's average."""
    model = MovingAverageForecaster(window=3)
    model.fit(daily_demand)

    forecast = model.predict(horizon=3)

    expected_prediction = (18 + 20 + 22) / 3

    assert len(forecast) == 3
    assert forecast["predicted_demand"].iloc[0] == pytest.approx(expected_prediction)
    assert forecast["predicted_demand"].nunique() == 1


def test_forecast_begins_after_last_observation(
    daily_demand: pd.Series,
) -> None:
    """Future dates should follow the historical series."""
    model = MovingAverageForecaster(window=3)
    model.fit(daily_demand)

    forecast = model.predict(horizon=2)

    assert forecast.index[0] == pd.Timestamp("2026-01-11")
    assert forecast.index[1] == pd.Timestamp("2026-01-12")
    assert forecast.index.name == "forecast_date"


def test_forecast_contains_confidence_bounds(
    daily_demand: pd.Series,
) -> None:
    """Every forecast should include lower and upper bounds."""
    model = MovingAverageForecaster(window=5)
    model.fit(daily_demand)

    forecast = model.predict(
        horizon=3,
        confidence_level=0.95,
    )

    assert list(forecast.columns) == [
        "predicted_demand",
        "lower_bound",
        "upper_bound",
    ]

    assert (forecast["lower_bound"] <= forecast["predicted_demand"]).all()

    assert (forecast["upper_bound"] >= forecast["predicted_demand"]).all()

    assert (forecast["lower_bound"] >= 0).all()


def test_prediction_before_fit_is_rejected() -> None:
    """An unfitted model should not generate forecasts."""
    model = MovingAverageForecaster(window=3)

    with pytest.raises(
        RuntimeError,
        match="must be fitted",
    ):
        model.predict(horizon=2)


@pytest.mark.parametrize(
    "invalid_window",
    [2.5, True],
)
def test_non_integer_window_is_rejected(
    invalid_window: object,
) -> None:
    """Non-integer windows should raise TypeError."""
    with pytest.raises(
        TypeError,
        match="must be an integer",
    ):
        MovingAverageForecaster(
            window=invalid_window,  # type: ignore[arg-type]
        )


def test_insufficient_history_is_rejected(
    daily_demand: pd.Series,
) -> None:
    """Historical demand must cover the selected window."""
    model = MovingAverageForecaster(window=20)

    with pytest.raises(
        ValueError,
        match="At least 20 observations",
    ):
        model.fit(daily_demand)


@pytest.mark.parametrize(
    "invalid_window",
    [0, -1],
)
def test_non_positive_window_is_rejected(
    invalid_window: int,
) -> None:
    """Zero and negative windows should raise ValueError."""
    with pytest.raises(
        ValueError,
        match="greater than zero",
    ):
        MovingAverageForecaster(
            window=invalid_window,
        )


def test_matching_future_exogenous_features_are_accepted(
    daily_demand: pd.Series,
) -> None:
    """Known future regressors may accompany a baseline forecast."""
    model = MovingAverageForecaster(window=3)
    model.fit(daily_demand)

    future_features = pd.DataFrame(
        {
            "price": [50, 55],
            "promotion": [0, 1],
        },
        index=pd.date_range(
            start="2026-01-11",
            periods=2,
            freq="D",
        ),
    )

    forecast = model.predict(
        horizon=2,
        future_exogenous=future_features,
    )

    assert len(forecast) == 2


def test_mismatched_future_exogenous_dates_are_rejected(
    daily_demand: pd.Series,
) -> None:
    """Future regressors must match forecast dates."""
    model = MovingAverageForecaster(window=3)
    model.fit(daily_demand)

    future_features = pd.DataFrame(
        {
            "price": [50, 55],
        },
        index=pd.date_range(
            start="2026-02-01",
            periods=2,
            freq="D",
        ),
    )

    with pytest.raises(
        ValueError,
        match="must match",
    ):
        model.predict(
            horizon=2,
            future_exogenous=future_features,
        )
