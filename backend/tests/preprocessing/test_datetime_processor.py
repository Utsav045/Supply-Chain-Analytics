"""
Unit Tests for DatetimeProcessor

Tests the datetime processing service including:
- DateTime parsing and validation
- Invalid date handling
- Duplicate timestamp removal
- Chronological sorting
- DateTime indexing

Author: Antigravity AI
"""

import pandas as pd
import pytest

from app.services.preprocessing import DatetimeProcessor
from app.services.utils.exceptions import DataCleaningError


class TestDatetimeProcessorBasic:
    """Test basic datetime processing functionality."""

    def test_process_valid_dates(self, sample_sales_df):
        """Test processing of valid dates."""
        processor = DatetimeProcessor()
        result = processor.process(sample_sales_df)

        assert isinstance(result.index, pd.DatetimeIndex)
        assert len(result) == 10
        assert result.index.is_monotonic_increasing

    def test_process_sorts_chronologically(self):
        """Test that dates are sorted chronologically."""
        df = pd.DataFrame(
            {
                "date": pd.to_datetime(["2024-01-05", "2024-01-01", "2024-01-03"]),
                "sales": [120.0, 100.0, 110.0],
            }
        )

        processor = DatetimeProcessor()
        result = processor.process(df)

        expected_dates = pd.date_range("2024-01-01", periods=3, freq="2D")
        assert all(result.index == expected_dates)

    def test_process_sets_datetime_index(self, sample_sales_df):
        """Test that datetime is set as index."""
        processor = DatetimeProcessor()
        result = processor.process(sample_sales_df)

        assert isinstance(result.index, pd.DatetimeIndex)
        assert result.index.name == "date"

    def test_missing_date_column_raises_error(self):
        """Test error when date column is missing."""
        df = pd.DataFrame({"sales": [100.0, 105.0]})
        processor = DatetimeProcessor(date_column="date")

        with pytest.raises(DataCleaningError, match="not found"):
            processor.process(df)

    def test_custom_date_column(self):
        """Test processing with a custom date column name."""
        df = pd.DataFrame(
            {
                "transaction_date": pd.date_range("2024-01-01", periods=3),
                "sales": [100.0, 105.0, 110.0],
            }
        )

        processor = DatetimeProcessor(date_column="transaction_date")
        result = processor.process(df)

        assert isinstance(result.index, pd.DatetimeIndex)
        assert len(result) == 3


class TestDatetimeProcessorInvalidDates:
    """Test handling of invalid dates."""

    def test_invalid_dates_raise_error_by_default(self, df_with_invalid_dates):
        """Test that invalid dates raise error by default."""
        processor = DatetimeProcessor()

        with pytest.raises(DataCleaningError):
            processor.process(df_with_invalid_dates, errors="raise")

    def test_invalid_dates_coerced_to_nat(self, df_with_invalid_dates):
        """Test that invalid dates are coerced to NaT."""
        processor = DatetimeProcessor()
        result = processor.process(df_with_invalid_dates, errors="coerce")

        # Should remove NaT rows
        assert len(result) < len(df_with_invalid_dates)
        assert result.isna().sum().sum() == 0  # No remaining NaT

    def test_empty_dataframe_raises_error(self):
        """Test error with empty DataFrame."""
        df = pd.DataFrame()
        processor = DatetimeProcessor()

        with pytest.raises(DataCleaningError):
            processor.process(df)


class TestDatetimeProcessorDuplicates:
    """Test duplicate timestamp handling."""

    def test_removes_duplicate_timestamps(self, df_with_duplicate_dates):
        """Test that duplicate timestamps are removed."""
        processor = DatetimeProcessor()
        result = processor.process(df_with_duplicate_dates)

        assert len(result) == 3  # Only 3 unique dates
        assert result.index.is_unique

    def test_keeps_first_duplicate(self, df_with_duplicate_dates):
        """Test that first duplicate is kept."""
        processor = DatetimeProcessor()
        result = processor.process(df_with_duplicate_dates)

        # First entry for 2024-01-01 should be kept (100.0)
        assert result.iloc[0]["sales"] == 100.0


class TestValidateDatetimeColumn:
    """Test datetime column validation."""

    def test_validate_valid_datetime_column(self, sample_df_with_datetime_index):
        """Test validation of valid datetime column."""
        df = sample_df_with_datetime_index.copy()
        df["date"] = df.index
        processor = DatetimeProcessor()
        assert processor.validate_datetime_column(df) is True

    def test_validate_missing_column_raises_error(self):
        """Test error when date column is missing."""
        df = pd.DataFrame({"sales": [100.0, 105.0]})
        processor = DatetimeProcessor(date_column="date")

        with pytest.raises(DataCleaningError):
            processor.validate_datetime_column(df)

    def test_validate_non_datetime_column_raises_error(self):
        """Test error when column is not datetime."""
        df = pd.DataFrame({"date": ["2024-01-01", "2024-01-02"]})
        processor = DatetimeProcessor()

        with pytest.raises(DataCleaningError):
            processor.validate_datetime_column(df)


class TestGetDateRange:
    """Test date range extraction."""

    def test_get_date_range_from_index(self, sample_df_with_datetime_index):
        """Test getting date range from DatetimeIndex."""
        processor = DatetimeProcessor()
        min_date, max_date = processor.get_date_range(sample_df_with_datetime_index)

        assert min_date == pd.Timestamp("2024-01-01")
        assert max_date == pd.Timestamp("2024-01-05")

    def test_get_date_range_from_column(self, sample_sales_df):
        """Test getting date range from date column."""
        processor = DatetimeProcessor()
        min_date, max_date = processor.get_date_range(sample_sales_df)

        assert min_date == pd.Timestamp("2024-01-01")
        assert max_date == pd.Timestamp("2024-01-10")


class TestRemoveDuplicates:
    """Test duplicate removal."""

    def test_remove_duplicates_from_index(self):
        """Test removing duplicate timestamps from index."""
        df = pd.DataFrame(
            {
                "sales": [100.0, 105.0, 110.0],
            },
            index=pd.to_datetime(["2024-01-01", "2024-01-01", "2024-01-02"]),
        )

        processor = DatetimeProcessor()
        result = processor.remove_duplicates(df)

        assert len(result) == 2
        assert result.index.is_unique

    def test_remove_duplicates_requires_datetime_index(self):
        """Test error when index is not DatetimeIndex."""
        df = pd.DataFrame({"sales": [100.0, 105.0]})
        processor = DatetimeProcessor()

        with pytest.raises(DataCleaningError):
            processor.remove_duplicates(df)


class TestEdgeCases:
    """Test edge cases and error conditions."""

    def test_single_row_dataframe(self, df_with_one_row):
        """Test processing single-row DataFrame."""
        df = df_with_one_row.copy()
        df["date"] = df.index
        processor = DatetimeProcessor()
        result = processor.process(df)

        assert len(result) == 1
        assert isinstance(result.index, pd.DatetimeIndex)

    def test_large_date_range(self):
        """Test processing large date ranges."""
        df = pd.DataFrame(
            {
                "date": pd.date_range("2020-01-01", periods=1000, freq="D"),
                "sales": range(1000),
            }
        )

        processor = DatetimeProcessor()
        result = processor.process(df)

        assert len(result) == 1000
        assert result.index.is_monotonic_increasing

    def test_preserves_other_columns(self, sample_sales_df):
        """Test that other columns are preserved."""
        processor = DatetimeProcessor()
        result = processor.process(sample_sales_df)

        assert "product_id" in result.columns
        assert "sales" in result.columns
        assert "price" in result.columns
        assert (
            len(result.columns) == len(sample_sales_df.columns) - 1
        )  # minus date column
