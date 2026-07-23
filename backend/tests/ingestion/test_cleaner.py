import pandas as pd

from app.core.constants import (
    DATE_COLUMN,
    PRICE_COLUMN,
    PRODUCT_ID_COLUMN,
    SALES_COLUMN,
)
from app.services.ingestion.cleaner import DataCleaner


def test_remove_duplicates():
    """Test duplicate row removal."""
    df = pd.DataFrame({"col1": [1, 1, 2], "col2": ["a", "a", "b"]})
    cleaned = DataCleaner.remove_duplicates(df)
    assert len(cleaned) == 2
    assert list(cleaned["col1"]) == [1, 2]


def test_standardize_types_sales():
    """Test date parsing and string trimming for sales."""
    df = pd.DataFrame(
        {
            DATE_COLUMN: ["2026-07-20", "2026-07-21"],
            PRODUCT_ID_COLUMN: [" PROD-01 ", "PROD-02"],
            SALES_COLUMN: ["10.5", 20],
            PRICE_COLUMN: [5.0, " 15.0 "],
        }
    )
    standardized = DataCleaner.standardize_types(df, "sales")

    assert pd.api.types.is_datetime64_any_dtype(standardized[DATE_COLUMN])
    assert list(standardized[PRODUCT_ID_COLUMN]) == ["PROD-01", "PROD-02"]
    assert list(standardized[SALES_COLUMN]) == [10.5, 20.0]
    assert list(standardized[PRICE_COLUMN]) == [5.0, 15.0]


def test_impute_missing_values():
    """Test filling missing values with median/mode."""
    df = pd.DataFrame(
        {"num_col": [1.0, 2.0, None, 4.0, 5.0], "cat_col": ["A", "A", None, "B", "B"]}
    )
    imputed = DataCleaner.impute_missing_values(df, "sales")

    # Median of [1, 2, 4, 5] is 3.0
    assert imputed["num_col"].iloc[2] == 3.0
    # Mode of ["A", "A", "B", "B"] is "A"
    assert imputed["cat_col"].iloc[2] == "A"


def test_correct_negative_values():
    """Test negative value replacement with median."""
    df = pd.DataFrame(
        {
            SALES_COLUMN: [10.0, 20.0, -5.0, 30.0, 40.0],
            PRICE_COLUMN: [2.0, -1.0, 4.0, 6.0, 8.0],
        }
    )
    corrected = DataCleaner.correct_negative_values(df, "sales")

    # Median of non-negative sales [10, 20, 30, 40] is 25.0
    assert corrected[SALES_COLUMN].iloc[2] == 25.0
    # Median of non-negative price [2, 4, 6, 8] is 5.0
    assert corrected[PRICE_COLUMN].iloc[1] == 5.0


def test_clean_dataset_pipeline():
    """Test complete pipeline cleaning."""
    df = pd.DataFrame(
        {
            DATE_COLUMN: [
                "2026-07-20",
                "2026-07-20",
                "2026-07-21",
                None,
            ],  # Duplicate and missing
            PRODUCT_ID_COLUMN: [" PROD-01 ", " PROD-01 ", "PROD-02", "PROD-03"],
            SALES_COLUMN: [10, 10, -50.0, None],  # Duplicate, negative, missing
            PRICE_COLUMN: [5.0, 5.0, 15.0, 10.0],
        }
    )
    cleaned = DataCleaner.clean_dataset(df, "sales")

    # 1 duplicate row removed
    # Total remaining rows should be 3
    assert len(cleaned) == 3

    # Check that product ID was stripped
    assert "PROD-01" in cleaned[PRODUCT_ID_COLUMN].values

    # Check date column is converted to datetime
    assert pd.api.types.is_datetime64_any_dtype(cleaned[DATE_COLUMN])

    # Check negative sales is corrected to median of non-negative sales (10.0)
    # Sales values were [10, -50, None], non-neg is [10], median is 10.0.
    # Missing is imputed to median 10.0.
    # So all sales values should be 10.0
    assert (cleaned[SALES_COLUMN] == 10.0).all()
