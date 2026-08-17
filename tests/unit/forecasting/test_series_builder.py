"""Tests for demand-series construction."""

import pandas as pd
import pytest
from src.forecasting.series_builder import build_demand_series
from src.forecasting.validation import ForecastingDataValidationError


@pytest.fixture
def single_location_data() -> pd.DataFrame:
    """Return sample data for one product and location."""
    return pd.DataFrame(
        {
            "date": [
                "2026-01-01",
                "2026-01-03",
                "2026-01-04",
            ],
            "sku_id": [
                "SKU-001",
                "SKU-001",
                "SKU-001",
            ],
            "demand": [10, 20, 15],
            "inventory_level": [100, 80, 65],
            "price": [50.0, 50.0, 55.0],
            "promotion": [False, True, False],
            "holiday": [False, False, True],
            "category": [
                "Electronics",
                "Electronics",
                "Electronics",
            ],
            "location_id": [
                "LAGOS-01",
                "LAGOS-01",
                "LAGOS-01",
            ],
        }
    )


def test_build_demand_series_regularizes_dates(
    single_location_data: pd.DataFrame,
) -> None:
    """Missing dates should be introduced during resampling."""
    result = build_demand_series(
        dataframe=single_location_data,
        sku_id="SKU-001",
        location_id="LAGOS-01",
        frequency="D",
    )

    assert len(result) == 4
    assert pd.Timestamp("2026-01-02") in result.index
    assert result.loc["2026-01-02", "demand"] == 0.0


def test_builder_preserves_product_metadata(
    single_location_data: pd.DataFrame,
) -> None:
    """Product, location and category should remain available."""
    result = build_demand_series(
        dataframe=single_location_data,
        sku_id="SKU-001",
        location_id="LAGOS-01",
    )

    assert result["sku_id"].eq("SKU-001").all()
    assert result["location_id"].eq("LAGOS-01").all()
    assert result["category"].eq("Electronics").all()


def test_inventory_is_carried_forward(
    single_location_data: pd.DataFrame,
) -> None:
    """Missing inventory snapshots should use the preceding value."""
    result = build_demand_series(
        dataframe=single_location_data,
        sku_id="SKU-001",
        location_id="LAGOS-01",
    )

    assert result.loc["2026-01-02", "inventory_level"] == 100


def test_multiple_locations_require_location_selection() -> None:
    """A product in multiple locations should not be mixed silently."""
    dataframe = pd.DataFrame(
        {
            "date": [
                "2026-01-01",
                "2026-01-01",
            ],
            "sku_id": [
                "SKU-001",
                "SKU-001",
            ],
            "demand": [10, 15],
            "location_id": [
                "LAGOS-01",
                "ABUJA-01",
            ],
        }
    )

    with pytest.raises(
        ForecastingDataValidationError,
        match="multiple locations",
    ):
        build_demand_series(
            dataframe=dataframe,
            sku_id="SKU-001",
        )


def test_unknown_location_is_rejected(
    single_location_data: pd.DataFrame,
) -> None:
    """An unknown product-location combination should fail."""
    with pytest.raises(
        ForecastingDataValidationError,
        match="No observations match",
    ):
        build_demand_series(
            dataframe=single_location_data,
            sku_id="SKU-001",
            location_id="UNKNOWN-LOCATION",
        )


def test_invalid_frequency_is_rejected(
    single_location_data: pd.DataFrame,
) -> None:
    """Invalid pandas frequency values should fail validation."""
    with pytest.raises(
        ForecastingDataValidationError,
        match="Invalid time-series frequency",
    ):
        build_demand_series(
            dataframe=single_location_data,
            sku_id="SKU-001",
            location_id="LAGOS-01",
            frequency="INVALID",
        )
