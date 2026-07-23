"""Utilities for building model-ready demand series."""

import pandas as pd

from src.forecasting.validation import (
    ForecastingDataValidationError,
    validate_forecasting_dataframe,
)


def build_demand_series(
    dataframe: pd.DataFrame,
    sku_id: str,
    location_id: str | None = None,
    frequency: str = "D",
) -> pd.DataFrame:
    """
    Build a regular time-series dataset for one product and location.

    Args:
        dataframe: Complete validated forecasting dataset.
        sku_id: Product to include.
        location_id: Optional store or warehouse identifier.
        frequency: Required time-series frequency.

    Returns:
        Regular time-indexed forecasting dataset.
    """
    validated = validate_forecasting_dataframe(dataframe)

    product_data = validated.loc[
        validated["sku_id"] == sku_id
    ].copy()

    if location_id is not None:
        if "location_id" not in product_data.columns:
            raise ForecastingDataValidationError(
                "location_id was requested but is absent from the dataset."
            )

        product_data = product_data.loc[
            product_data["location_id"] == location_id
        ].copy()

    if product_data.empty:
        raise ForecastingDataValidationError(
            "No observations match the selected product and location."
        )

    product_data = product_data.set_index("date").sort_index()

    aggregation_rules: dict[str, str] = {
        "demand": "sum",
    }

    if "inventory_level" in product_data.columns:
        aggregation_rules["inventory_level"] = "last"

    if "price" in product_data.columns:
        aggregation_rules["price"] = "mean"

    if "promotion" in product_data.columns:
        aggregation_rules["promotion"] = "max"

    if "holiday" in product_data.columns:
        aggregation_rules["holiday"] = "max"

    regular_data = product_data.resample(frequency).agg(
        aggregation_rules
    )

    regular_data["demand"] = regular_data["demand"].fillna(0.0)

    if "inventory_level" in regular_data.columns:
        regular_data["inventory_level"] = (
            regular_data["inventory_level"]
            .ffill()
            .bfill()
        )

    if "price" in regular_data.columns:
        regular_data["price"] = (
            regular_data["price"]
            .ffill()
            .bfill()
        )

    for binary_column in ("promotion", "holiday"):
        if binary_column in regular_data.columns:
            regular_data[binary_column] = (
                regular_data[binary_column]
                .fillna(False)
                .astype(bool)
            )

    return regular_data