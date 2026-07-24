"""Utilities for building model-ready demand series."""

import pandas as pd
from pandas.tseries.frequencies import to_offset

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

    Raises:
        ForecastingDataValidationError: If the selected series is invalid
            or ambiguous.
    """
    cleaned_sku_id = sku_id.strip()

    if not cleaned_sku_id:
        raise ForecastingDataValidationError("sku_id cannot be empty.")

    try:
        to_offset(frequency)
    except ValueError as exc:
        raise ForecastingDataValidationError(
            f"Invalid time-series frequency: {frequency}."
        ) from exc

    validated = validate_forecasting_dataframe(dataframe)

    product_data = validated.loc[validated["sku_id"] == cleaned_sku_id].copy()

    if product_data.empty:
        raise ForecastingDataValidationError(
            f"No observations were found for SKU '{cleaned_sku_id}'."
        )

    resolved_location: str | None = location_id

    if "location_id" in product_data.columns:
        available_locations = product_data["location_id"].dropna().astype(str).unique()

        if location_id is None and len(available_locations) > 1:
            raise ForecastingDataValidationError(
                "The selected product exists in multiple locations. "
                "Specify location_id before building the demand series."
            )

        if location_id is not None:
            cleaned_location_id = location_id.strip()

            if not cleaned_location_id:
                raise ForecastingDataValidationError("location_id cannot be empty.")

            product_data = product_data.loc[
                product_data["location_id"] == cleaned_location_id
            ].copy()

            resolved_location = cleaned_location_id

        elif len(available_locations) == 1:
            resolved_location = str(available_locations[0])

    elif location_id is not None:
        raise ForecastingDataValidationError(
            "location_id was requested but is absent from the dataset."
        )

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

    if "category" in product_data.columns:
        aggregation_rules["category"] = "last"

    regular_data = product_data.resample(frequency).agg(aggregation_rules)

    regular_data["demand"] = regular_data["demand"].fillna(0.0).astype(float)

    if "inventory_level" in regular_data.columns:
        regular_data["inventory_level"] = (
            regular_data["inventory_level"].ffill().bfill()
        )

    if "price" in regular_data.columns:
        regular_data["price"] = regular_data["price"].ffill().bfill()

    for binary_column in ("promotion", "holiday"):
        if binary_column in regular_data.columns:
            regular_data[binary_column] = (
                regular_data[binary_column].fillna(False).astype(bool)
            )

    if "category" in regular_data.columns:
        regular_data["category"] = regular_data["category"].ffill().bfill()

    regular_data.insert(
        loc=0,
        column="sku_id",
        value=cleaned_sku_id,
    )

    if resolved_location is not None:
        regular_data.insert(
            loc=1,
            column="location_id",
            value=resolved_location,
        )

    regular_data.index.name = "date"

    return regular_data
