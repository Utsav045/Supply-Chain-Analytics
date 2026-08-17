"""Tests for the production forecasting service."""

import pandas as pd
import pytest
from src.forecasting.model_validation import ModelInputValidationError
from src.forecasting.moving_average import MovingAverageForecaster
from src.forecasting.schemas import ForecastRequest
from src.forecasting.validation import ForecastingDataValidationError
from src.services.forecasting_service import ForecastingService


@pytest.fixture
def historical_data() -> pd.DataFrame:
    """Return complete historical supply-chain observations."""
    dates = pd.date_range(
        start="2026-01-01",
        periods=20,
        freq="D",
    )

    return pd.DataFrame(
        {
            "date": dates,
            "sku_id": ["SKU-001"] * 20,
            "demand": [float(value) for value in range(10, 50, 2)],
            "inventory_level": [float(value) for value in range(100, 80, -1)],
            "price": [50.0] * 20,
            "promotion": [False] * 15 + [True] * 5,
            "holiday": [False] * 20,
            "category": ["Electronics"] * 20,
            "location_id": ["LAGOS-01"] * 20,
        }
    )


@pytest.fixture
def forecasting_service() -> ForecastingService:
    """Return a deterministic service for unit testing."""
    return ForecastingService(
        model_factories={
            "moving_average_2": (lambda: MovingAverageForecaster(window=2)),
            "moving_average_5": (lambda: MovingAverageForecaster(window=5)),
        },
        primary_metric="rmse",
        backtest_ratio=0.25,
    )


def test_automatic_forecast_selects_best_model(
    forecasting_service: ForecastingService,
    historical_data: pd.DataFrame,
) -> None:
    """Automatic mode should select the strongest candidate."""
    request = ForecastRequest(
        sku_id="SKU-001",
        location_id="LAGOS-01",
        forecast_horizon=3,
        model_name="auto",
    )

    result = forecasting_service.forecast(
        historical_data,
        request,
    )

    assert result.model_name == "moving_average_2"
    assert result.forecast_horizon == 3
    assert len(result.forecasts) == 3
    assert result.selected_model.is_fitted is True


def test_explicit_model_can_be_requested(
    forecasting_service: ForecastingService,
    historical_data: pd.DataFrame,
) -> None:
    """A caller should be able to request a named model."""
    request = ForecastRequest(
        sku_id="SKU-001",
        location_id="LAGOS-01",
        forecast_horizon=2,
        model_name="moving_average_5",
    )

    result = forecasting_service.forecast(
        historical_data,
        request,
    )

    assert result.model_name == "moving_average_5"
    assert len(result.forecasts) == 2


def test_service_returns_evaluation_metrics(
    forecasting_service: ForecastingService,
    historical_data: pd.DataFrame,
) -> None:
    """Service results should contain model evaluation metrics."""
    result = forecasting_service.forecast(
        historical_data,
        ForecastRequest(
            sku_id="SKU-001",
            location_id="LAGOS-01",
            forecast_horizon=2,
        ),
    )

    assert set(result.metrics) == {
        "mae",
        "mape",
        "mse",
        "rmse",
        "r2",
    }


def test_forecast_starts_after_historical_data(
    forecasting_service: ForecastingService,
    historical_data: pd.DataFrame,
) -> None:
    """Forecast dates should follow the final historical date."""
    result = forecasting_service.forecast(
        historical_data,
        ForecastRequest(
            sku_id="SKU-001",
            location_id="LAGOS-01",
            forecast_horizon=2,
        ),
    )

    assert result.forecasts.index[0] == pd.Timestamp("2026-01-21")


def test_unknown_model_is_rejected(
    forecasting_service: ForecastingService,
    historical_data: pd.DataFrame,
) -> None:
    """Unsupported model names should fail clearly."""
    with pytest.raises(
        ModelInputValidationError,
        match="Unknown forecasting model",
    ):
        forecasting_service.forecast(
            historical_data,
            ForecastRequest(
                sku_id="SKU-001",
                location_id="LAGOS-01",
                model_name="unknown-model",
            ),
        )


def test_unknown_sku_is_rejected(
    forecasting_service: ForecastingService,
    historical_data: pd.DataFrame,
) -> None:
    """The selected SKU must exist in historical data."""
    with pytest.raises(
        ForecastingDataValidationError,
        match="No observations",
    ):
        forecasting_service.forecast(
            historical_data,
            ForecastRequest(
                sku_id="UNKNOWN-SKU",
                location_id="LAGOS-01",
            ),
        )


def test_available_models_include_auto(
    forecasting_service: ForecastingService,
) -> None:
    """The service should advertise all usable models."""
    assert forecasting_service.available_models == (
        "auto",
        "moving_average_2",
        "moving_average_5",
    )


def test_service_can_persist_selected_model(
    tmp_path,
    historical_data: pd.DataFrame,
) -> None:
    """The selected model should be saved when requested."""
    from src.forecasting.persistence import ModelStore

    service = ForecastingService(
        model_factories={
            "moving_average_2": (lambda: MovingAverageForecaster(window=2)),
        },
        model_store=ModelStore(tmp_path),
    )

    result = service.forecast(
        historical_data,
        ForecastRequest(
            sku_id="SKU-001",
            location_id="LAGOS-01",
            forecast_horizon=2,
        ),
        persist_model=True,
    )

    assert result.model_artifact_id is not None

    assert (tmp_path / f"{result.model_artifact_id}.joblib").is_file()
