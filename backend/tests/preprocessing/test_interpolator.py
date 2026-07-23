"""
Unit Tests for Interpolator

Tests the interpolation service including:
- Missing date filling
- Missing value interpolation
- Multiple interpolation methods (linear, forward fill, backward fill, time)
- Data continuity validation
- Missing value statistics

Author: Antigravity AI
"""

import pandas as pd
import pytest

from app.services.preprocessing import Interpolator
from app.services.utils.exceptions import DataCleaningError


class TestFillMissingDates:
    """Test missing date filling."""

    def test_fill_missing_dates_creates_continuous_index(self, df_with_missing_dates):
        """Test that fill_missing_dates creates a continuous date range."""
        interpolator = Interpolator()
        result = interpolator.fill_missing_dates(df_with_missing_dates)

        # Should have 6 dates: 2024-01-01 to 2024-01-06
        assert len(result) == 6
        assert result.index.is_monotonic_increasing

    def test_fill_missing_dates_preserves_existing_values(self, df_with_missing_dates):
        """Test that existing values are preserved."""
        interpolator = Interpolator()
        result = interpolator.fill_missing_dates(df_with_missing_dates)

        # Check that original values are preserved
        assert result.loc["2024-01-01", "sales"] == 100.0
        assert result.loc["2024-01-03", "sales"] == 110.0

    def test_fill_missing_dates_creates_nans_for_gaps(self, df_with_missing_dates):
        """Test that NaN values are created for missing dates."""
        interpolator = Interpolator()
        result = interpolator.fill_missing_dates(df_with_missing_dates)

        # Dates 2024-01-02 and 2024-01-04 should have NaN for sales
        assert pd.isna(result.loc["2024-01-02", "sales"])
        assert pd.isna(result.loc["2024-01-04", "sales"])

    def test_fill_missing_dates_with_custom_frequency(self, df_with_missing_dates):
        """Test fill_missing_dates with custom frequency."""
        interpolator = Interpolator()
        result = interpolator.fill_missing_dates(df_with_missing_dates, frequency="D")

        assert len(result) == 6


class TestInterpolateLinear:
    """Test linear interpolation."""

    def test_interpolate_linear_fills_gaps(self, df_with_missing_values):
        """Test linear interpolation fills missing values."""
        interpolator = Interpolator()
        result = interpolator.interpolate(df_with_missing_values, method="linear")

        # Check that NaN values are filled
        assert result["sales"].isna().sum() == 0 or result["sales"].isna().sum() < 2
        assert result["inventory"].isna().sum() <= 1

    def test_interpolate_linear_maintains_endpoints(self):
        """Test that endpoints are preserved with linear interpolation."""
        df = pd.DataFrame(
            {
                "value": [10.0, None, None, 40.0],
            },
            index=pd.date_range("2024-01-01", periods=4, freq="D"),
        )

        interpolator = Interpolator()
        result = interpolator.interpolate(df, method="linear")

        assert result.iloc[0]["value"] == 10.0
        assert result.iloc[-1]["value"] == 40.0

    def test_interpolate_linear_intermediate_values(self):
        """Test linear interpolation calculates intermediate values correctly."""
        df = pd.DataFrame(
            {
                "value": [10.0, None, None, 40.0],
            },
            index=pd.date_range("2024-01-01", periods=4, freq="D"),
        )

        interpolator = Interpolator()
        result = interpolator.interpolate(df, method="linear")

        # Linear interpolation: 10 -> 20 -> 30 -> 40
        assert result.iloc[1]["value"] == pytest.approx(20.0)
        assert result.iloc[2]["value"] == pytest.approx(30.0)


class TestInterpolateForwardFill:
    """Test forward fill interpolation."""

    def test_forward_fill_propagates_last_value(self):
        """Test forward fill propagates last valid value forward."""
        df = pd.DataFrame(
            {
                "value": [10.0, None, None, 40.0],
            },
            index=pd.date_range("2024-01-01", periods=4, freq="D"),
        )

        interpolator = Interpolator()
        result = interpolator.interpolate(df, method="forward_fill")

        assert result.iloc[1]["value"] == 10.0
        assert result.iloc[2]["value"] == 10.0

    def test_forward_fill_shorthand(self, df_with_missing_values):
        """Test forward_fill shorthand method."""
        interpolator = Interpolator()
        result = interpolator.forward_fill(df_with_missing_values)

        assert result["sales"].notna().all() or result["sales"].isna().sum() < 2

    def test_forward_fill_with_limit(self):
        """Test forward fill with limit parameter."""
        df = pd.DataFrame(
            {
                "value": [10.0, None, None, None, 50.0],
            },
            index=pd.date_range("2024-01-01", periods=5, freq="D"),
        )

        interpolator = Interpolator()
        result = interpolator.interpolate(df, method="forward_fill", limit=1)

        # Only fills 1 NaN per forward fill group
        assert result.iloc[1]["value"] == 10.0
        assert pd.isna(result.iloc[2]["value"])
        assert pd.isna(result.iloc[3]["value"])


class TestInterpolateBackwardFill:
    """Test backward fill interpolation."""

    def test_backward_fill_propagates_next_value(self):
        """Test backward fill propagates next valid value backward."""
        df = pd.DataFrame(
            {
                "value": [10.0, None, None, 40.0],
            },
            index=pd.date_range("2024-01-01", periods=4, freq="D"),
        )

        interpolator = Interpolator()
        result = interpolator.interpolate(df, method="backward_fill")

        assert result.iloc[1]["value"] == 40.0
        assert result.iloc[2]["value"] == 40.0

    def test_backward_fill_shorthand(self, df_with_missing_values):
        """Test backward_fill shorthand method."""
        interpolator = Interpolator()
        result = interpolator.backward_fill(df_with_missing_values)

        assert result["sales"].notna().all() or result["sales"].isna().sum() < 2


class TestInterpolateTime:
    """Test time-based interpolation."""

    def test_interpolate_time_method(self):
        """Test time-based interpolation."""
        df = pd.DataFrame(
            {
                "value": [10.0, None, None, 40.0],
            },
            index=pd.date_range("2024-01-01", periods=4, freq="D"),
        )

        interpolator = Interpolator()
        result = interpolator.interpolate(df, method="time")

        # Time-based should be similar to linear for regular intervals
        assert result.iloc[1]["value"] == pytest.approx(20.0)
        assert result.iloc[2]["value"] == pytest.approx(30.0)


class TestSelectiveColumnInterpolation:
    """Test interpolating specific columns."""

    def test_interpolate_specific_columns(self, df_with_missing_values):
        """Test interpolating only specific columns."""
        interpolator = Interpolator()
        result = interpolator.interpolate(
            df_with_missing_values, method="linear", columns=["sales"]
        )

        assert (
            result["sales"].isna().sum() < df_with_missing_values["sales"].isna().sum()
        )

    def test_non_numeric_columns_ignored(self):
        """Test that non-numeric columns are ignored."""
        df = pd.DataFrame(
            {
                "category": ["A", "B", "C"],
                "value": [10.0, None, 30.0],
            },
            index=pd.date_range("2024-01-01", periods=3, freq="D"),
        )

        interpolator = Interpolator()
        result = interpolator.interpolate(df, method="linear")

        # Non-numeric column unchanged
        assert (result["category"] == df["category"]).all()


class TestValidateContinuity:
    """Test continuity validation."""

    def test_continuous_index_passes_validation(self, sample_df_with_datetime_index):
        """Test that continuous index passes validation."""
        interpolator = Interpolator()
        assert interpolator.validate_continuity(sample_df_with_datetime_index) is True

    def test_discontinuous_index_fails_validation(self, df_with_missing_dates):
        """Test that discontinuous index fails validation."""
        interpolator = Interpolator()
        assert interpolator.validate_continuity(df_with_missing_dates) is False

    def test_single_row_dataframe_passes_validation(self, df_with_one_row):
        """Test that single-row DataFrame passes validation."""
        interpolator = Interpolator()
        assert interpolator.validate_continuity(df_with_one_row) is True


class TestMissingStatistics:
    """Test missing value statistics calculation."""

    def test_get_missing_stats_no_missing_values(self, sample_df_with_datetime_index):
        """Test missing stats with no missing values."""
        interpolator = Interpolator()
        stats = interpolator.get_missing_stats(sample_df_with_datetime_index)

        assert stats["total_missing"] == 0
        for col in stats["missing_by_column"]:
            assert stats["missing_by_column"][col] == 0
            assert stats["missing_percentage_by_column"][col] == 0.0

    def test_get_missing_stats_with_missing_values(self, df_with_missing_values):
        """Test missing stats with missing values."""
        interpolator = Interpolator()
        stats = interpolator.get_missing_stats(df_with_missing_values)

        assert stats["total_missing"] > 0
        assert stats["total_rows"] == 5
        assert stats["total_cols"] == 2

    def test_missing_stats_percentages(self, df_with_missing_values):
        """Test that missing percentages are calculated correctly."""
        interpolator = Interpolator()
        stats = interpolator.get_missing_stats(df_with_missing_values)

        # sales has 2 NaN, inventory has 1 NaN out of 5
        assert stats["missing_by_column"]["sales"] == 2
        assert stats["missing_by_column"]["inventory"] == 1
        assert stats["missing_percentage_by_column"]["sales"] == pytest.approx(40.0)
        assert stats["missing_percentage_by_column"]["inventory"] == pytest.approx(20.0)


class TestInputValidation:
    """Test input validation."""

    def test_non_datetime_index_raises_error(self):
        """Test error when DataFrame doesn't have DatetimeIndex."""
        df = pd.DataFrame(
            {
                "value": [10.0, None, 30.0],
            },
            index=[0, 1, 2],
        )

        interpolator = Interpolator()
        with pytest.raises(DataCleaningError):
            interpolator.interpolate(df)

    def test_empty_dataframe_raises_error(self):
        """Test error with empty DataFrame."""
        df = pd.DataFrame()

        interpolator = Interpolator()
        with pytest.raises(DataCleaningError):
            interpolator.interpolate(df)

    def test_invalid_method_raises_error(self, sample_df_with_datetime_index):
        """Test error with invalid interpolation method."""
        interpolator = Interpolator()

        with pytest.raises(DataCleaningError):
            interpolator.interpolate(
                sample_df_with_datetime_index, method="invalid_method"
            )

    def test_validate_continuity_non_datetime_index_raises_error(self):
        """Test error validating continuity with non-datetime index."""
        df = pd.DataFrame(
            {
                "value": [10.0, 20.0, 30.0],
            },
            index=[0, 1, 2],
        )

        interpolator = Interpolator()
        with pytest.raises(DataCleaningError):
            interpolator.validate_continuity(df)


class TestInterpolationWorkflow:
    """Test complete interpolation workflows."""

    def test_fill_then_interpolate_workflow(self):
        """Test complete workflow: fill missing dates then interpolate values."""
        df = pd.DataFrame(
            {
                "sales": [100.0, 110.0, 120.0],
            },
            index=pd.to_datetime(["2024-01-01", "2024-01-03", "2024-01-05"]),
        )

        interpolator = Interpolator()

        # Step 1: Fill missing dates
        df_filled = interpolator.fill_missing_dates(df)
        assert len(df_filled) == 5  # All 5 dates

        # Step 2: Interpolate missing values
        df_interpolated = interpolator.interpolate(df_filled, method="linear")
        assert df_interpolated["sales"].isna().sum() == 0  # No more NaN

    def test_forward_fill_then_backward_fill(self):
        """Test combining forward and backward fills."""
        df = pd.DataFrame(
            {
                "value": [10.0, None, None, 40.0, None],
            },
            index=pd.date_range("2024-01-01", periods=5, freq="D"),
        )

        interpolator = Interpolator()

        # Fill with forward fill
        result = interpolator.forward_fill(df)
        assert result.iloc[1]["value"] == 10.0
        assert result.iloc[2]["value"] == 10.0
        # Forward fill fills all remaining values with last valid
        assert result.iloc[4]["value"] == 40.0


class TestEdgeCases:
    """Test edge cases."""

    def test_all_missing_values(self):
        """Test interpolation with all NaN values."""
        df = pd.DataFrame(
            {
                "value": [None, None, None],
            },
            index=pd.date_range("2024-01-01", periods=3, freq="D"),
        )

        interpolator = Interpolator()
        result = interpolator.interpolate(df, method="linear")

        # All values remain NaN
        assert result["value"].isna().all()

    def test_single_non_null_value(self):
        """Test interpolation with only one non-null value."""
        df = pd.DataFrame(
            {
                "value": [None, 20.0, None],
            },
            index=pd.date_range("2024-01-01", periods=3, freq="D"),
        )

        interpolator = Interpolator()
        result = interpolator.interpolate(df, method="linear")

        assert result.iloc[1]["value"] == 20.0
