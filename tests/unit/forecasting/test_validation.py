"""Tests for forecasting dataset validation."""

import pandas as pd
import pytest

from src.forecasting.validation import (
    ForecastingDataValidationError,
    validate_forecasting_dataframe,
)


@pytest.fixture
def valid_dataframe() -> pd.DataFrame:
    """Return a complete valid forecasting dataset."""
    return pd.DataFrame(
        {
            "date": [
                "2026-01-01",
                "2026-01-02",
            ],
            "sku_id": [
                "SKU-001",
                "SKU-001",
            ],
            "demand": [10, 12],
            "inventory_level": [100, 88],
            "price": [50.0, 50.0],
            "promotion": ["no", "yes"],
            "holiday": [0, 1],
            "category": [
                "Electronics",
                "Electronics",
            ],
            "location_id": [
                "LAGOS-01",
                "LAGOS-01",
            ],
        }
    )


def test_complete_dataframe_passes_validation(
    valid_dataframe: pd.DataFrame,
) -> None:
    """A valid complete dataset should be standardized."""
    result = validate_forecasting_dataframe(valid_dataframe)

    assert len(result) == 2
    assert pd.api.types.is_datetime64_any_dtype(result["date"])
    assert str(result["promotion"].dtype) == "boolean"
    assert str(result["holiday"].dtype) == "boolean"


@pytest.mark.parametrize(
    "missing_column",
    [
        "date",
        "sku_id",
        "demand",
    ],
)
def test_missing_required_column_is_rejected(
    valid_dataframe: pd.DataFrame,
    missing_column: str,
) -> None:
    """Every required forecasting field should be enforced."""
    invalid = valid_dataframe.drop(columns=[missing_column])

    with pytest.raises(
        ForecastingDataValidationError,
        match="Missing required columns",
    ):
        validate_forecasting_dataframe(invalid)


def test_invalid_date_is_rejected(
    valid_dataframe: pd.DataFrame,
) -> None:
    """Invalid date values should fail validation."""
    valid_dataframe.loc[0, "date"] = "not-a-date"

    with pytest.raises(
        ForecastingDataValidationError,
        match="invalid values",
    ):
        validate_forecasting_dataframe(valid_dataframe)


def test_negative_demand_is_rejected(
    valid_dataframe: pd.DataFrame,
) -> None:
    """Demand cannot be negative."""
    valid_dataframe.loc[0, "demand"] = -10

    with pytest.raises(
        ForecastingDataValidationError,
        match="demand cannot contain negative",
    ):
        validate_forecasting_dataframe(valid_dataframe)


def test_negative_inventory_is_rejected(
    valid_dataframe: pd.DataFrame,
) -> None:
    """Inventory values cannot be negative."""
    valid_dataframe.loc[0, "inventory_level"] = -1

    with pytest.raises(
        ForecastingDataValidationError,
        match="inventory_level cannot contain negative",
    ):
        validate_forecasting_dataframe(valid_dataframe)


def test_invalid_boolean_value_is_rejected(
    valid_dataframe: pd.DataFrame,
) -> None:
    """Unknown promotion representations should fail."""
    valid_dataframe.loc[0, "promotion"] = "sometimes"

    with pytest.raises(
        ForecastingDataValidationError,
        match="promotion contains invalid boolean",
    ):
        validate_forecasting_dataframe(valid_dataframe)


def test_duplicate_observation_is_rejected(
    valid_dataframe: pd.DataFrame,
) -> None:
    """Duplicate date, SKU and location combinations should fail."""
    duplicate = pd.concat(
        [
            valid_dataframe,
            valid_dataframe.iloc[[0]],
        ],
        ignore_index=True,
    )

    with pytest.raises(
        ForecastingDataValidationError,
        match="Duplicate time-series observations",
    ):
        validate_forecasting_dataframe(duplicate)


def test_optional_columns_are_not_required() -> None:
    """The minimum accepted dataset should remain valid."""
    dataframe = pd.DataFrame(
        {
            "date": [
                "2026-01-01",
                "2026-01-02",
            ],
            "sku_id": [
                "SKU-001",
                "SKU-001",
            ],
            "demand": [10, 15],
        }
    )

    result = validate_forecasting_dataframe(dataframe)

    assert list(result.columns) == [
        "date",
        "sku_id",
        "demand",
    ]
