"""Validation utilities for demand forecasting datasets."""

import pandas as pd

REQUIRED_COLUMNS = {
    "date",
    "sku_id",
    "demand",
}

OPTIONAL_COLUMNS = {
    "inventory_level",
    "price",
    "promotion",
    "holiday",
    "category",
    "location_id",
}

NUMERIC_COLUMNS = {
    "demand",
    "inventory_level",
    "price",
}

BOOLEAN_COLUMNS = {
    "promotion",
    "holiday",
}


class ForecastingDataValidationError(ValueError):
    """Raised when forecasting data fails validation."""


def validate_forecasting_dataframe(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """Validate and standardize the forecasting dataset."""
    if not isinstance(dataframe, pd.DataFrame):
        raise ForecastingDataValidationError(
            "Forecasting input must be a pandas DataFrame."
        )

    if dataframe.empty:
        raise ForecastingDataValidationError("Forecasting dataset cannot be empty.")

    missing_columns = REQUIRED_COLUMNS.difference(dataframe.columns)

    if missing_columns:
        missing_text = ", ".join(sorted(missing_columns))
        raise ForecastingDataValidationError(
            f"Missing required columns: {missing_text}."
        )

    validated = dataframe.copy()

    validated["date"] = pd.to_datetime(
        validated["date"],
        errors="coerce",
        format="mixed",
    )

    if validated["date"].isna().any():
        raise ForecastingDataValidationError("The date column contains invalid values.")

    validated["sku_id"] = validated["sku_id"].astype("string").str.strip()

    if validated["sku_id"].isna().any():
        raise ForecastingDataValidationError(
            "The sku_id column contains missing values."
        )

    if validated["sku_id"].eq("").any():
        raise ForecastingDataValidationError("The sku_id column contains empty values.")

    for column in NUMERIC_COLUMNS.intersection(validated.columns):
        validated[column] = pd.to_numeric(
            validated[column],
            errors="coerce",
        )

        if column == "demand" and validated[column].isna().any():
            raise ForecastingDataValidationError(
                "Demand contains missing or non-numeric values."
            )

        negative_values = validated[column].dropna() < 0

        if negative_values.any():
            raise ForecastingDataValidationError(
                f"{column} cannot contain negative values."
            )

    for column in BOOLEAN_COLUMNS.intersection(validated.columns):
        validated[column] = normalize_boolean_column(
            validated[column],
            column,
        )

    for column in {
        "category",
        "location_id",
    }.intersection(validated.columns):
        validated[column] = (
            validated[column].astype("string").str.strip().replace("", pd.NA)
        )

    duplicate_keys = ["date", "sku_id"]

    if "location_id" in validated.columns:
        duplicate_keys.append("location_id")

    duplicated_rows = validated.duplicated(
        subset=duplicate_keys,
        keep=False,
    )

    if duplicated_rows.any():
        raise ForecastingDataValidationError(
            "Duplicate time-series observations were detected."
        )

    return validated.sort_values(duplicate_keys).reset_index(drop=True)


def normalize_boolean_column(
    series: pd.Series,
    column_name: str,
) -> pd.Series:
    """Convert common binary representations to nullable booleans."""
    mapping = {
        "1": True,
        "0": False,
        "true": True,
        "false": False,
        "yes": True,
        "no": False,
        "y": True,
        "n": False,
    }

    normalized = series.map(
        lambda value: (
            mapping.get(str(value).strip().lower()) if pd.notna(value) else pd.NA
        )
    )

    invalid_values = series.notna() & normalized.isna()

    if invalid_values.any():
        raise ForecastingDataValidationError(
            f"{column_name} contains invalid boolean values."
        )

    return normalized.astype("boolean")
