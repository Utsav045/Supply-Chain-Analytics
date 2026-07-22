"""
Test Fixtures for Preprocessing Module

Provides reusable fixtures for preprocessing tests including sample DataFrames,
dates, and common test data.

Author: Antigravity AI
"""

import pandas as pd
import pytest


@pytest.fixture
def sample_sales_df():
    """Create a sample sales DataFrame with valid dates."""
    return pd.DataFrame(
        {
            "date": pd.date_range("2024-01-01", periods=10, freq="D"),
            "product_id": ["PROD-001"] * 10,
            "sales": [
                100.0,
                105.0,
                110.0,
                95.0,
                120.0,
                115.0,
                130.0,
                125.0,
                140.0,
                135.0,
            ],
            "price": [10.0] * 10,
        }
    )


@pytest.fixture
def sample_inventory_df():
    """Create a sample inventory DataFrame with valid dates."""
    return pd.DataFrame(
        {
            "date": pd.date_range("2024-01-01", periods=10, freq="D"),
            "product_id": ["PROD-001"] * 10,
            "inventory": [
                500.0,
                495.0,
                490.0,
                485.0,
                480.0,
                475.0,
                470.0,
                465.0,
                460.0,
                455.0,
            ],
        }
    )


@pytest.fixture
def sample_df_with_datetime_index():
    """Create a sample DataFrame with DatetimeIndex."""
    df = pd.DataFrame(
        {
            "sales": [100.0, 105.0, 110.0, 95.0, 120.0],
            "inventory": [500.0, 495.0, 490.0, 485.0, 480.0],
        },
        index=pd.date_range("2024-01-01", periods=5, freq="D"),
    )
    df.index.name = "date"
    return df


@pytest.fixture
def df_with_missing_dates():
    """Create a DataFrame with missing dates in the time series."""
    dates = pd.to_datetime(["2024-01-01", "2024-01-03", "2024-01-05", "2024-01-06"])
    return pd.DataFrame(
        {
            "sales": [100.0, 110.0, 120.0, 125.0],
            "inventory": [500.0, 490.0, 480.0, 475.0],
        },
        index=dates,
    )


@pytest.fixture
def df_with_missing_values():
    """Create a DataFrame with NaN values."""
    return pd.DataFrame(
        {
            "sales": [100.0, None, 110.0, 95.0, None],
            "inventory": [500.0, 495.0, None, 485.0, 480.0],
        },
        index=pd.date_range("2024-01-01", periods=5, freq="D"),
    )


@pytest.fixture
def df_with_invalid_dates():
    """Create a DataFrame with invalid date strings."""
    return pd.DataFrame(
        {
            "date": [
                "2024-01-01",
                "invalid-date",
                "2024-01-03",
                "2024/13/45",
                "2024-01-05",
            ],
            "sales": [100.0, 105.0, 110.0, 95.0, 120.0],
        }
    )


@pytest.fixture
def df_with_duplicate_dates():
    """Create a DataFrame with duplicate timestamps."""
    return pd.DataFrame(
        {
            "date": pd.to_datetime(
                ["2024-01-01", "2024-01-01", "2024-01-02", "2024-01-02", "2024-01-03"]
            ),
            "sales": [100.0, 105.0, 110.0, 95.0, 120.0],
        }
    )


@pytest.fixture
def empty_df():
    """Create an empty DataFrame."""
    return pd.DataFrame()


@pytest.fixture
def df_with_one_row():
    """Create a DataFrame with a single row."""
    return pd.DataFrame(
        {
            "sales": [100.0],
            "inventory": [500.0],
        },
        index=pd.date_range("2024-01-01", periods=1, freq="D"),
    )
