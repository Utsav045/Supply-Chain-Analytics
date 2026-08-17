"""Tests for the ARIMA demand forecaster."""

import numpy as np
import pandas as pd
import pytest

from src.forecasting.arima import ARIMAForecaster
from src.forecasting.arima_config import ARIMAConfig
from src.forecasting.model_validation import ModelInputValidationError


@pytest.fixture
def demand_series() -> pd.Series:
    """Return reproducible positive autoregressive demand."""
    random_generator = np.random.default_rng(seed=42)
    noise = random_generator.normal(
        loc=0.0,
        scale=1.0,
        size=80,
    )

    values = np.zeros(80, dtype=float)
    values[0] = 40.0

    for position in range(1, len(values)):
        values[position] = 20.0 + (0.50 * values[position - 1]) + noise[position]

    return pd.Series(
        data=values,
        index=pd.date_range(
            start="2026-01-01",
            periods=80,
            freq="D",
        ),
        name="demand",
        dtype=float,
    )


def test_new_arima_model_is_not_fitted() -> None:
    """A new ARIMA model should begin unfitted."""
    model = ARIMAForecaster(config=ARIMAConfig(p=1, d=0, q=0))

    assert model.is_fitted is False
    assert model.aic is None
    assert model.bic is None


def test_arima_model_name_uses_order() -> None:
    """The model name should identify p, d and q."""
    model = ARIMAForecaster(config=ARIMAConfig(p=2, d=1, q=1))

    assert model.model_name == "arima_2_1_1"


def test_fit_returns_fitted_model(
    demand_series: pd.Series,
) -> None:
    """ARIMA fitting should update model state."""
    model = ARIMAForecaster(config=ARIMAConfig(p=1, d=0, q=0))

    returned_model = model.fit(demand_series)

    assert returned_model is model
    assert model.is_fitted is True
    assert model.aic is not None
    assert model.bic is not None
    assert model.converged is not None


def test_arima_generates_requested_horizon(
    demand_series: pd.Series,
) -> None:
    """ARIMA should return the requested number of periods."""
    model = ARIMAForecaster(config=ARIMAConfig(p=1, d=0, q=0))
    model.fit(demand_series)

    forecast = model.predict(horizon=5)

    assert len(forecast) == 5

    assert list(forecast.columns) == [
        "predicted_demand",
        "lower_bound",
        "upper_bound",
    ]

    assert forecast.index[0] == pd.Timestamp("2026-03-22")

    assert forecast.index.name == "forecast_date"


def test_arima_forecast_values_are_non_negative(
    demand_series: pd.Series,
) -> None:
    """Demand forecasts and bounds should not be negative."""
    model = ARIMAForecaster(config=ARIMAConfig(p=1, d=0, q=0))
    model.fit(demand_series)

    forecast = model.predict(horizon=5)

    assert (forecast["predicted_demand"] >= 0).all()
    assert (forecast["lower_bound"] >= 0).all()
    assert (forecast["upper_bound"] >= 0).all()


def test_confidence_bounds_surround_forecast(
    demand_series: pd.Series,
) -> None:
    """Lower and upper bounds should surround predictions."""
    model = ARIMAForecaster(config=ARIMAConfig(p=1, d=0, q=0))
    model.fit(demand_series)

    forecast = model.predict(
        horizon=5,
        confidence_level=0.95,
    )

    assert (forecast["lower_bound"] <= forecast["predicted_demand"]).all()

    assert (forecast["upper_bound"] >= forecast["predicted_demand"]).all()


def test_prediction_before_fit_is_rejected() -> None:
    """An unfitted ARIMA model should not forecast."""
    model = ARIMAForecaster(config=ARIMAConfig(p=1, d=0, q=0))

    with pytest.raises(
        RuntimeError,
        match="must be fitted",
    ):
        model.predict(horizon=3)


def test_arima_supports_exogenous_regressors(
    demand_series: pd.Series,
) -> None:
    """ARIMA should support aligned external variables."""
    exogenous = pd.DataFrame(
        {
            "price": np.linspace(
                50.0,
                60.0,
                len(demand_series),
            ),
            "promotion": (np.arange(len(demand_series)) % 10 == 0).astype(float),
        },
        index=demand_series.index,
    )

    model = ARIMAForecaster(config=ARIMAConfig(p=1, d=0, q=0))
    model.fit(
        demand_series,
        exogenous=exogenous,
    )

    future_index = pd.date_range(
        start=demand_series.index[-1] + pd.Timedelta(days=1),
        periods=3,
        freq="D",
    )

    future_exogenous = pd.DataFrame(
        {
            "price": [61.0, 61.5, 62.0],
            "promotion": [0.0, 1.0, 0.0],
        },
        index=future_index,
    )

    forecast = model.predict(
        horizon=3,
        future_exogenous=future_exogenous,
    )

    assert model.uses_exogenous_features is True
    assert len(forecast) == 3


def test_future_exogenous_features_are_required_after_training(
    demand_series: pd.Series,
) -> None:
    """Future regressors are required when training used regressors."""
    exogenous = pd.DataFrame(
        {
            "price": [50.0] * len(demand_series),
        },
        index=demand_series.index,
    )

    model = ARIMAForecaster(config=ARIMAConfig(p=1, d=0, q=0))
    model.fit(
        demand_series,
        exogenous=exogenous,
    )

    with pytest.raises(
        ModelInputValidationError,
        match="are required",
    ):
        model.predict(horizon=3)


def test_future_exogenous_columns_must_match_training(
    demand_series: pd.Series,
) -> None:
    """Future regressor names must match training names."""
    exogenous = pd.DataFrame(
        {
            "price": [50.0] * len(demand_series),
        },
        index=demand_series.index,
    )

    model = ARIMAForecaster(config=ARIMAConfig(p=1, d=0, q=0))
    model.fit(
        demand_series,
        exogenous=exogenous,
    )

    future_exogenous = pd.DataFrame(
        {
            "promotion": [0.0, 1.0],
        },
        index=pd.date_range(
            start=demand_series.index[-1] + pd.Timedelta(days=1),
            periods=2,
            freq="D",
        ),
    )

    with pytest.raises(
        ModelInputValidationError,
        match="columns must match",
    ):
        model.predict(
            horizon=2,
            future_exogenous=future_exogenous,
        )


def test_future_exogenous_rejected_when_not_trained_with_it(
    demand_series: pd.Series,
) -> None:
    """A univariate ARIMA model should reject future regressors."""
    model = ARIMAForecaster(config=ARIMAConfig(p=1, d=0, q=0))
    model.fit(demand_series)

    future_exogenous = pd.DataFrame(
        {
            "price": [50.0, 51.0],
        },
        index=pd.date_range(
            start=demand_series.index[-1] + pd.Timedelta(days=1),
            periods=2,
            freq="D",
        ),
    )

    with pytest.raises(
        ModelInputValidationError,
        match="trained without regressors",
    ):
        model.predict(
            horizon=2,
            future_exogenous=future_exogenous,
        )
