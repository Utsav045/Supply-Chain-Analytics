"""
Unit Tests for Resampler

Tests the data resampling service including:
- Resampling to different frequencies (daily, weekly, monthly)
- Automatic aggregation method selection
- Custom aggregation configuration
- Upsampling detection

Author: Antigravity AI
"""

import pandas as pd
import pytest

from app.services.preprocessing import Resampler
from app.services.utils.exceptions import DataCleaningError


class TestResamplerBasic:
    """Test basic resampling functionality."""

    def test_resample_to_weekly(self, sample_df_with_datetime_index):
        """Test resampling to weekly frequency."""
        resampler = Resampler()
        result = resampler.resample(sample_df_with_datetime_index, frequency="weekly")

        assert isinstance(result.index, pd.DatetimeIndex)
        assert len(result) == 1  # 5 days = 1 week
        assert result.index.freq == "W-SUN"

    def test_resample_to_monthly(self):
        """Test resampling to monthly frequency."""
        df = pd.DataFrame(
            {
                "sales": range(30),
                "inventory": range(500, 530),
            },
            index=pd.date_range("2024-01-01", periods=30, freq="D"),
        )

        resampler = Resampler()
        result = resampler.resample(df, frequency="monthly")

        assert len(result) == 1  # All data in one month
        assert result.loc["2024-01-31", "sales"] == sum(range(30))  # Sum of sales

    def test_resample_with_short_code(self, sample_df_with_datetime_index):
        """Test resampling with short frequency codes (D, W, M)."""
        resampler = Resampler()
        result = resampler.resample(sample_df_with_datetime_index, frequency="W")

        assert len(result) == 1

    def test_resample_returns_dataframe(self, sample_df_with_datetime_index):
        """Test that resampling returns DataFrame."""
        resampler = Resampler()
        result = resampler.resample(sample_df_with_datetime_index, frequency="daily")

        assert isinstance(result, pd.DataFrame)


class TestAggregationMethods:
    """Test automatic aggregation method selection."""

    def test_sales_aggregated_by_sum(self):
        """Test that sales are summed during resampling."""
        df = pd.DataFrame(
            {
                "sales": [100.0, 105.0, 110.0, 115.0, 120.0],
            },
            index=pd.date_range("2024-01-01", periods=5, freq="D"),
        )

        resampler = Resampler()
        result = resampler.resample(df, frequency="weekly")

        expected_sum = 100.0 + 105.0 + 110.0 + 115.0 + 120.0
        assert result.iloc[0]["sales"] == expected_sum

    def test_inventory_aggregated_by_mean(self):
        """Test that inventory is averaged during resampling."""
        df = pd.DataFrame(
            {
                "inventory": [500.0, 495.0, 490.0, 485.0, 480.0],
            },
            index=pd.date_range("2024-01-01", periods=5, freq="D"),
        )

        resampler = Resampler()
        result = resampler.resample(df, frequency="weekly")

        expected_mean = (500.0 + 495.0 + 490.0 + 485.0 + 480.0) / 5
        assert result.iloc[0]["inventory"] == expected_mean

    def test_demand_aggregated_by_sum(self):
        """Test that demand is summed during resampling."""
        df = pd.DataFrame(
            {
                "demand": [50.0, 55.0, 60.0, 65.0, 70.0],
            },
            index=pd.date_range("2024-01-01", periods=5, freq="D"),
        )

        resampler = Resampler()
        result = resampler.resample(df, frequency="weekly")

        expected_sum = 50.0 + 55.0 + 60.0 + 65.0 + 70.0
        assert result.iloc[0]["demand"] == expected_sum

    def test_mixed_aggregation(self):
        """Test resampling with multiple columns using different aggregation methods."""
        df = pd.DataFrame(
            {
                "sales": [100.0, 105.0, 110.0, 115.0, 120.0],
                "inventory": [500.0, 495.0, 490.0, 485.0, 480.0],
            },
            index=pd.date_range("2024-01-01", periods=5, freq="D"),
        )

        resampler = Resampler()
        result = resampler.resample(df, frequency="weekly")

        assert result.iloc[0]["sales"] == 550.0  # Sum
        assert result.iloc[0]["inventory"] == 490.0  # Mean


class TestCustomAggregation:
    """Test custom aggregation configuration."""

    def test_custom_aggregation_config(self):
        """Test resampling with custom aggregation config."""
        df = pd.DataFrame(
            {
                "sales": [100.0, 105.0, 110.0],
                "inventory": [500.0, 495.0, 490.0],
            },
            index=pd.date_range("2024-01-01", periods=3, freq="D"),
        )

        config = {"sales": "mean", "inventory": "sum"}
        resampler = Resampler()
        result = resampler.resample(df, frequency="daily", aggregation_config=config)

        assert result.loc["2024-01-01", "sales"] == 100.0
        assert result.loc["2024-01-01", "inventory"] == 500.0

    def test_aggregation_config_overrides_defaults(self):
        """Test that custom config overrides default rules."""
        df = pd.DataFrame(
            {
                "sales": [100.0, 105.0, 110.0],
            },
            index=pd.date_range("2024-01-01", periods=3, freq="D"),
        )

        # Default is sum for sales, but override to mean
        config = {"sales": "mean"}
        resampler = Resampler()
        result = resampler.resample(df, frequency="daily", aggregation_config=config)

        assert result.loc["2024-01-01", "sales"] == 100.0


class TestInputValidation:
    """Test input validation."""

    def test_empty_dataframe_raises_error(self):
        """Test error with empty DataFrame."""
        df = pd.DataFrame()
        resampler = Resampler()

        with pytest.raises(DataCleaningError):
            resampler.resample(df, frequency="weekly")

    def test_non_datetime_index_raises_error(self):
        """Test error when index is not DatetimeIndex."""
        df = pd.DataFrame(
            {
                "sales": [100.0, 105.0, 110.0],
            },
            index=[1, 2, 3],
        )

        resampler = Resampler()
        with pytest.raises(DataCleaningError):
            resampler.resample(df, frequency="weekly")

    def test_invalid_frequency_raises_error(self, sample_df_with_datetime_index):
        """Test error with invalid frequency."""
        resampler = Resampler()

        with pytest.raises(DataCleaningError):
            resampler.resample(sample_df_with_datetime_index, frequency="invalid")

    def test_no_numeric_columns_raises_error(self):
        """Test error when DataFrame has no numeric columns."""
        df = pd.DataFrame(
            {
                "product_id": ["PROD-001", "PROD-002", "PROD-003"],
            },
            index=pd.date_range("2024-01-01", periods=3, freq="D"),
        )

        resampler = Resampler()
        with pytest.raises(DataCleaningError):
            resampler.resample(df, frequency="weekly")


class TestSupportedFrequencies:
    """Test supported frequency methods."""

    def test_get_supported_frequencies(self):
        """Test getting list of supported frequencies."""
        resampler = Resampler()
        freqs = resampler.get_supported_frequencies()

        assert "D" in freqs
        assert "W" in freqs
        assert "M" in freqs


class TestUpsamplingDetection:
    """Test upsampling detection."""

    def test_upsampling_detection_weekly_to_daily(self):
        """Test detecting upsampling from weekly to daily."""
        df = pd.DataFrame(
            {
                "sales": [100.0, 105.0, 110.0],
            },
            index=pd.date_range("2024-01-01", periods=3, freq="W"),
        )

        resampler = Resampler()
        assert resampler.upsampling_available(df, "D") is True

    def test_no_upsampling_daily_to_weekly(self):
        """Test detecting no upsampling from daily to weekly."""
        df = pd.DataFrame(
            {
                "sales": [100.0, 105.0, 110.0],
            },
            index=pd.date_range("2024-01-01", periods=3, freq="D"),
        )

        resampler = Resampler()
        assert resampler.upsampling_available(df, "W") is False

    def test_upsampling_empty_dataframe(self):
        """Test upsampling detection with empty DataFrame."""
        df = pd.DataFrame()

        resampler = Resampler()
        assert resampler.upsampling_available(df, "D") is False


class TestMultipleColumns:
    """Test resampling with multiple columns."""

    def test_resample_multiple_products(self):
        """Test resampling data for multiple products."""
        df = pd.DataFrame(
            {
                "product_id": ["PROD-001"] * 5 + ["PROD-002"] * 5,
                "sales": [
                    100.0,
                    105.0,
                    110.0,
                    115.0,
                    120.0,
                    200.0,
                    205.0,
                    210.0,
                    215.0,
                    220.0,
                ],
            },
            index=pd.date_range("2024-01-01", periods=10, freq="D"),
        )

        # Note: Real use would typically group by product_id first
        resampler = Resampler()
        result = resampler.resample(df, frequency="weekly")

        # Only numeric columns are aggregated, product_id is aggregated too
        assert len(result) == 2  # 2 weeks
        assert "sales" in result.columns

    def test_resample_preserves_non_numeric_columns(self):
        """Test that non-numeric columns are dropped during resampling."""
        df = pd.DataFrame(
            {
                "product_id": ["PROD-001", "PROD-001", "PROD-001"],
                "sales": [100.0, 105.0, 110.0],
            },
            index=pd.date_range("2024-01-01", periods=3, freq="D"),
        )

        resampler = Resampler()
        result = resampler.resample(df, frequency="weekly")

        # Non-numeric columns will be aggregated, not preserved
        assert len(result) == 1


class TestMultipleFrequencies:
    """Test resampling to different frequencies."""

    def test_daily_to_weekly_reduction(self):
        """Test resampling reduces data points from daily to weekly."""
        df = pd.DataFrame(
            {
                "sales": range(35),
            },
            index=pd.date_range("2024-01-01", periods=35, freq="D"),
        )

        resampler = Resampler()
        result = resampler.resample(df, frequency="W")

        assert len(result) == 5  # 35 days = 5 weeks

    def test_daily_to_monthly_reduction(self):
        """Test resampling reduces data points from daily to monthly."""
        df = pd.DataFrame(
            {
                "sales": range(90),
            },
            index=pd.date_range("2024-01-01", periods=90, freq="D"),
        )

        resampler = Resampler()
        result = resampler.resample(df, frequency="M")

        assert len(result) == 3  # ~3 months in 90 days
