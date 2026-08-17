"""Tests for forecasting Pydantic schemas."""

from datetime import UTC, datetime

import pytest
from pydantic import ValidationError
from src.forecasting.schemas import DemandObservation, ForecastRequest


def test_complete_demand_observation_is_valid() -> None:
    """A complete historical observation should be accepted."""
    observation = DemandObservation(
        date=datetime(2026, 1, 1, tzinfo=UTC),
        sku_id="SKU-001",
        demand=25,
        inventory_level=100,
        price=50,
        promotion=True,
        holiday=False,
        category="Electronics",
        location_id="LAGOS-01",
    )

    assert observation.sku_id == "SKU-001"
    assert observation.demand == 25
    assert observation.location_id == "LAGOS-01"


def test_minimum_demand_observation_is_valid() -> None:
    """Optional business variables should remain optional."""
    observation = DemandObservation(
        date=datetime(2026, 1, 1, tzinfo=UTC),
        sku_id="SKU-001",
        demand=25,
    )

    assert observation.inventory_level is None
    assert observation.price is None
    assert observation.category is None


def test_negative_demand_is_rejected() -> None:
    """Schema validation should reject negative demand."""
    with pytest.raises(ValidationError):
        DemandObservation(
            date=datetime(2026, 1, 1, tzinfo=UTC),
            sku_id="SKU-001",
            demand=-1,
        )


def test_empty_optional_strings_become_none() -> None:
    """Empty category and location fields should be standardized."""
    observation = DemandObservation(
        date=datetime(2026, 1, 1, tzinfo=UTC),
        sku_id="SKU-001",
        demand=10,
        category=" ",
        location_id="",
    )

    assert observation.category is None
    assert observation.location_id is None


def test_forecast_horizon_must_be_positive() -> None:
    """A forecast request must contain a valid horizon."""
    with pytest.raises(ValidationError):
        ForecastRequest(
            sku_id="SKU-001",
            forecast_horizon=0,
        )


def test_forecast_horizon_cannot_exceed_limit() -> None:
    """The API should reject unsupported forecast horizons."""
    with pytest.raises(ValidationError):
        ForecastRequest(
            sku_id="SKU-001",
            forecast_horizon=366,
        )


def test_unknown_schema_field_is_rejected() -> None:
    """Unexpected API fields should not be silently accepted."""
    with pytest.raises(ValidationError):
        ForecastRequest(
            sku_id="SKU-001",
            forecast_horizon=30,
            unknown_field="unexpected",
        )
