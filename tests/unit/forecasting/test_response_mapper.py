"""Tests for forecast response conversion."""

from datetime import UTC, datetime

import pandas as pd
import pytest

from src.forecasting.model_validation import (
    ModelInputValidationError,
)
from src.forecasting.moving_average import (
    MovingAverageForecaster,
)
from src.forecasting.response_mapper import (
    build_forecast_response,
)
from src.services.forecasting_service import (
    ForecastingServiceResult,
)


def make_service_result() -> ForecastingServiceResult:
    """Create a valid internal service result."""
    history = pd.Series(
        data=[10.0, 12.0, 14.0, 16.0],
        index=pd.date_range(
            "2026-01-01",
            periods=4,
            freq="D",
        ),
        name="demand",
    )

    model = MovingAverageForecaster(window=2)
    model.fit(history)

    forecasts = model.predict(horizon=2)

    return ForecastingServiceResult(
        sku_id="SKU-001",
        location_id="LAGOS-01",
        model_name=model.model_name,
        forecast_horizon=2,
        generated_at=datetime.now(UTC),
        metrics={
            "mae": 1.0,
            "mape": 5.0,
            "mse": 1.5,
            "rmse": 1.2247,
            "r2": 0.90,
        },
        forecasts=forecasts,
        selected_model=model,
    )


def test_service_result_converts_to_response() -> None:
    """Internal results should map to Pydantic schemas."""
    response = build_forecast_response(make_service_result())

    assert response.sku_id == "SKU-001"
    assert response.model_name == "moving_average_2"
    assert response.forecast_horizon == 2
    assert len(response.forecasts) == 2
    assert response.metrics is not None
    assert response.metrics.rmse == pytest.approx(1.2247)


def test_forecast_dates_are_converted() -> None:
    """Pandas timestamps should become UTC-aware datetimes."""
    response = build_forecast_response(make_service_result())

    assert response.forecasts[0].forecast_date == datetime(
        2026,
        1,
        5,
        tzinfo=UTC,
    )


def test_incorrect_forecast_length_is_rejected() -> None:
    """Response length must match the declared horizon."""
    result = make_service_result()

    invalid_result = ForecastingServiceResult(
        sku_id=result.sku_id,
        location_id=result.location_id,
        model_name=result.model_name,
        forecast_horizon=5,
        generated_at=result.generated_at,
        metrics=result.metrics,
        forecasts=result.forecasts,
        selected_model=result.selected_model,
    )

    with pytest.raises(
        ModelInputValidationError,
        match="does not match",
    ):
        build_forecast_response(invalid_result)


def test_missing_forecast_column_is_rejected() -> None:
    """All public forecast fields must be present."""
    result = make_service_result()

    invalid_result = ForecastingServiceResult(
        sku_id=result.sku_id,
        location_id=result.location_id,
        model_name=result.model_name,
        forecast_horizon=result.forecast_horizon,
        generated_at=result.generated_at,
        metrics=result.metrics,
        forecasts=result.forecasts.drop(columns=["upper_bound"]),
        selected_model=result.selected_model,
    )

    with pytest.raises(
        ModelInputValidationError,
        match="missing columns",
    ):
        build_forecast_response(invalid_result)
