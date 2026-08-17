"""Integration tests for forecasting API endpoints."""

from collections.abc import Iterator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.api.app import create_app
from src.api.forecasting import get_forecasting_service
from src.forecasting.moving_average import MovingAverageForecaster
from src.forecasting.persistence import ModelStore
from src.services.forecasting_service import ForecastingService


def build_observations() -> list[dict[str, object]]:
    """Create API-compatible historical observations."""
    return [
        {
            "date": f"2026-01-{day:02d}T00:00:00",
            "sku_id": "SKU-001",
            "demand": float(10 + (day * 2)),
            "inventory_level": float(120 - day),
            "price": 50.0,
            "promotion": day >= 15,
            "holiday": False,
            "category": "Electronics",
            "location_id": "LAGOS-01",
        }
        for day in range(1, 21)
    ]


@pytest.fixture
def application(tmp_path) -> Iterator[FastAPI]:
    """Return an application with deterministic dependencies."""
    app = create_app()

    test_service = ForecastingService(
        model_factories={
            "moving_average_2": (lambda: MovingAverageForecaster(window=2)),
            "moving_average_5": (lambda: MovingAverageForecaster(window=5)),
        },
        model_store=ModelStore(tmp_path),
    )

    app.dependency_overrides[get_forecasting_service] = lambda: test_service

    yield app

    app.dependency_overrides.clear()


@pytest.fixture
def client(
    application: FastAPI,
) -> Iterator[TestClient]:
    """Return a FastAPI test client."""
    with TestClient(application) as test_client:
        yield test_client


def test_health_endpoint(
    client: TestClient,
) -> None:
    """The application should expose a health check."""
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
    }


def test_models_endpoint(
    client: TestClient,
) -> None:
    """The API should expose its supported models."""
    response = client.get("/api/v1/forecasting/models")

    assert response.status_code == 200
    assert response.json() == [
        "auto",
        "moving_average_2",
        "moving_average_5",
    ]


def test_forecast_endpoint_returns_predictions(
    client: TestClient,
) -> None:
    """A valid payload should produce a forecast response."""
    response = client.post(
        "/api/v1/forecasting/forecast",
        json={
            "forecast": {
                "sku_id": "SKU-001",
                "location_id": "LAGOS-01",
                "forecast_horizon": 3,
                "model_name": "auto",
                "confidence_level": 0.95,
            },
            "observations": build_observations(),
            "persist_model": False,
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["sku_id"] == "SKU-001"
    assert body["location_id"] == "LAGOS-01"
    assert body["model_name"] == "moving_average_2"
    assert body["forecast_horizon"] == 3
    assert len(body["forecasts"]) == 3
    assert body["metrics"] is not None


def test_forecast_endpoint_can_persist_model(
    client: TestClient,
) -> None:
    """API clients should be able to request persistence."""
    response = client.post(
        "/api/v1/forecasting/forecast",
        json={
            "forecast": {
                "sku_id": "SKU-001",
                "location_id": "LAGOS-01",
                "forecast_horizon": 2,
                "model_name": "moving_average_2",
            },
            "observations": build_observations(),
            "persist_model": True,
        },
    )

    assert response.status_code == 200

    assert response.json()["model_artifact_id"] is not None


def test_unknown_model_returns_422(
    client: TestClient,
) -> None:
    """Unknown forecasting models should return a client error."""
    response = client.post(
        "/api/v1/forecasting/forecast",
        json={
            "forecast": {
                "sku_id": "SKU-001",
                "location_id": "LAGOS-01",
                "forecast_horizon": 2,
                "model_name": "unsupported-model",
            },
            "observations": build_observations(),
        },
    )

    assert response.status_code == 422

    assert "Unknown forecasting model" in (response.json()["detail"])


def test_invalid_horizon_returns_422(
    client: TestClient,
) -> None:
    """Pydantic should reject invalid forecasting horizons."""
    response = client.post(
        "/api/v1/forecasting/forecast",
        json={
            "forecast": {
                "sku_id": "SKU-001",
                "forecast_horizon": 0,
            },
            "observations": build_observations(),
        },
    )

    assert response.status_code == 422
