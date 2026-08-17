import pandas as pd
import pytest
from app.core.constants import (CATEGORY_COLUMN, DATE_COLUMN, INVENTORY_COLUMN,
                                PRICE_COLUMN, PRODUCT_ID_COLUMN,
                                PRODUCT_NAME_COLUMN, SALES_COLUMN)
from app.services.ingestion.validator import DataValidator
from app.services.utils.exceptions import ValidationError


def test_validate_not_empty():
    """Test that empty or None DataFrames raise ValidationError."""
    with pytest.raises(ValidationError, match="Dataset is empty or None"):
        DataValidator.validate_not_empty(None)

    with pytest.raises(ValidationError, match="Dataset is empty or None"):
        DataValidator.validate_not_empty(pd.DataFrame())

    # Should not raise
    DataValidator.validate_not_empty(pd.DataFrame({"a": [1]}))


def test_validate_columns():
    """Test required column validation."""
    df = pd.DataFrame({"col1": [1], "col2": [2]})

    # Should pass
    DataValidator.validate_columns(df, ["col1"])

    # Should raise
    with pytest.raises(ValidationError, match="Missing required columns: col3"):
        DataValidator.validate_columns(df, ["col1", "col3"])


def test_validate_dataset_sales():
    """Test validating a sales dataset."""
    # Valid sales df
    valid_sales = pd.DataFrame(
        {
            DATE_COLUMN: ["2026-07-20"],
            PRODUCT_ID_COLUMN: ["PROD-01"],
            SALES_COLUMN: [100.5],
            PRICE_COLUMN: [10.0],
        }
    )
    DataValidator.validate_dataset(valid_sales, "sales")

    # Invalid date
    invalid_date_sales = pd.DataFrame(
        {
            DATE_COLUMN: ["not-a-date"],
            PRODUCT_ID_COLUMN: ["PROD-01"],
            SALES_COLUMN: [100.5],
            PRICE_COLUMN: [10.0],
        }
    )
    with pytest.raises(ValidationError, match="is not a valid date format"):
        DataValidator.validate_dataset(invalid_date_sales, "sales")

    # Invalid numeric sales
    invalid_numeric_sales = pd.DataFrame(
        {
            DATE_COLUMN: ["2026-07-20"],
            PRODUCT_ID_COLUMN: ["PROD-01"],
            SALES_COLUMN: ["invalid_number"],
            PRICE_COLUMN: [10.0],
        }
    )
    with pytest.raises(ValidationError, match="must be numeric"):
        DataValidator.validate_dataset(invalid_numeric_sales, "sales")


def test_validate_dataset_inventory():
    """Test validating an inventory dataset."""
    valid_inv = pd.DataFrame(
        {
            DATE_COLUMN: ["2026-07-20"],
            PRODUCT_ID_COLUMN: ["PROD-01"],
            INVENTORY_COLUMN: [50],
        }
    )
    DataValidator.validate_dataset(valid_inv, "inventory")

    # Missing inventory column
    invalid_inv = pd.DataFrame(
        {
            DATE_COLUMN: ["2026-07-20"],
            PRODUCT_ID_COLUMN: ["PROD-01"],
        }
    )
    with pytest.raises(ValidationError, match="Missing required columns"):
        DataValidator.validate_dataset(invalid_inv, "inventory")


def test_validate_dataset_product():
    """Test validating a product catalog dataset."""
    valid_prod = pd.DataFrame(
        {
            PRODUCT_ID_COLUMN: ["PROD-01"],
            PRODUCT_NAME_COLUMN: ["Product 1"],
            CATEGORY_COLUMN: ["Electronics"],
            PRICE_COLUMN: [99.99],
        }
    )
    DataValidator.validate_dataset(valid_prod, "product")

    # Invalid price type
    invalid_prod = pd.DataFrame(
        {
            PRODUCT_ID_COLUMN: ["PROD-01"],
            PRODUCT_NAME_COLUMN: ["Product 1"],
            CATEGORY_COLUMN: ["Electronics"],
            PRICE_COLUMN: ["invalid_price"],
        }
    )
    with pytest.raises(ValidationError, match="must be numeric"):
        DataValidator.validate_dataset(invalid_prod, "product")
