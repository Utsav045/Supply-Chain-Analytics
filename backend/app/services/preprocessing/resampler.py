"""
Data Resampling Service

Handles resampling and aggregation of time-series data to different time
frequencies (daily, weekly, monthly) with appropriate aggregation methods
for different metric types (sum, mean).

Author: Antigravity AI
"""

from typing import Dict, Optional

import pandas as pd
from app.core.constants import (DAILY, DEMAND_COLUMN, INVENTORY_COLUMN,
                                MONTHLY, SALES_COLUMN, SUPPORTED_FREQUENCIES,
                                WEEKLY)
from app.core.logger import logger
from app.services.utils.exceptions import DataCleaningError


class Resampler:
    """
    Service for resampling and aggregating time-series data.

    Supports resampling to different frequencies (daily, weekly, monthly)
    with automatic aggregation method selection based on column type.

    Aggregation Rules:
    - Sales, Demand → Sum (cumulative)
    - Inventory → Mean (average state)
    - Revenue (price * sales) → Sum
    """

    # Define aggregation methods per column type
    AGGREGATION_METHODS = {
        "sum": [SALES_COLUMN, DEMAND_COLUMN, "revenue"],
        "mean": [INVENTORY_COLUMN],
    }

    # Frequency mapping
    FREQUENCY_MAP = {
        "daily": DAILY,
        "weekly": WEEKLY,
        "monthly": MONTHLY,
        "D": DAILY,
        "W": WEEKLY,
        "M": MONTHLY,
    }

    def __init__(self):
        """Initialize the Resampler."""
        pass

    def resample(
        self,
        df: pd.DataFrame,
        frequency: str,
        aggregation_config: Optional[Dict[str, str]] = None,
    ) -> pd.DataFrame:
        """
        Resample time-series data to a specified frequency.

        Args:
            df: DataFrame with DatetimeIndex
            frequency: Target frequency ('daily', 'weekly', 'monthly',
                or 'D', 'W', 'M')
            aggregation_config: Optional dict mapping column names
                to aggregation methods
                (e.g., {'sales': 'sum', 'inventory': 'mean'})

        Returns:
            pd.DataFrame: Resampled DataFrame

        Raises:
            DataCleaningError: If resampling fails or frequency is invalid
        """
        logger.info(f"Resampling data to frequency: {frequency}")

        # Validate input
        self._validate_input(df, frequency)

        # Normalize frequency
        freq_key = self.FREQUENCY_MAP.get(frequency.lower(), frequency)

        # Map M to ME for pandas 2.0+ compatibility
        if freq_key == "M":
            freq_key = "ME"

        if freq_key not in SUPPORTED_FREQUENCIES and freq_key != "ME":
            msg = (
                f"Unsupported frequency: {frequency}. "
                f"Supported: {SUPPORTED_FREQUENCIES}"
            )
            logger.error(msg)
            raise DataCleaningError(msg)

        try:
            # Determine aggregation methods
            agg_methods = self._get_aggregation_methods(df, aggregation_config)

            if not agg_methods:
                msg = "No numeric columns to resample"
                logger.error(msg)
                raise DataCleaningError(msg)

            # Perform resampling
            df_resampled = df.resample(freq_key).agg(agg_methods)

            logger.info(
                f"Successfully resampled to {frequency}. "
                f"Original shape: {df.shape}, Resampled shape: {df_resampled.shape}"
            )

            return df_resampled

        except DataCleaningError:
            raise
        except Exception as e:
            msg = f"Failed to resample data: {str(e)}"
            logger.exception(msg)
            raise DataCleaningError(msg) from e

    def _validate_input(self, df: pd.DataFrame, frequency: str) -> None:
        """
        Validate that input is suitable for resampling.

        Args:
            df: DataFrame to validate
            frequency: Frequency to validate

        Raises:
            DataCleaningError: If validation fails
        """
        if df is None or df.empty:
            msg = "DataFrame is empty or None"
            logger.error(msg)
            raise DataCleaningError(msg)

        if not isinstance(df.index, pd.DatetimeIndex):
            msg = "DataFrame must have a DatetimeIndex for resampling"
            logger.error(msg)
            raise DataCleaningError(msg)

        if frequency.lower() not in [
            "daily",
            "weekly",
            "monthly",
            "d",
            "w",
            "m",
        ]:
            msg = f"Invalid frequency: {frequency}"
            logger.error(msg)
            raise DataCleaningError(msg)

    def _get_aggregation_methods(
        self,
        df: pd.DataFrame,
        custom_config: Optional[Dict[str, str]] = None,
    ) -> Dict[str, str]:
        """
        Determine aggregation methods for each numeric column.

        If custom_config is provided, it takes precedence. Otherwise,
        uses default rules (sum for sales/demand, mean for inventory).

        Args:
            df: Input DataFrame
            custom_config: Optional column→method mapping

        Returns:
            dict: Mapping of column names to aggregation methods
        """
        agg_methods = {}

        # Use custom config if provided
        if custom_config:
            for col in df.select_dtypes(include=["number"]).columns:
                if col in custom_config:
                    agg_methods[col] = custom_config[col]
                else:
                    # Default for non-configured columns
                    agg_methods[col] = "mean"
        else:
            # Use default rules based on column name
            for col in df.select_dtypes(include=["number"]).columns:
                agg_methods[col] = self._get_default_method(col)

        return agg_methods

    def _get_default_method(self, column_name: str) -> str:
        """
        Get default aggregation method for a column based on its name.

        Rules:
        - Sales, Demand → Sum
        - Inventory → Mean
        - Everything else → Mean

        Args:
            column_name: Name of the column

        Returns:
            str: Aggregation method ('sum' or 'mean')
        """
        column_lower = column_name.lower()

        # Check sum columns
        for sum_col in self.AGGREGATION_METHODS["sum"]:
            if sum_col in column_lower:
                return "sum"

        # Default to mean
        return "mean"

    def get_supported_frequencies(self) -> list[str]:
        """
        Get list of supported resampling frequencies.

        Returns:
            list: Supported frequency codes
        """
        return SUPPORTED_FREQUENCIES

    def upsampling_available(self, df: pd.DataFrame, target_frequency: str) -> bool:
        """
        Check if upsampling to target frequency is possible.

        Upsampling (e.g., weekly → daily) requires interpolation.
        This method checks if the target frequency is higher resolution
        than the current data frequency.

        Args:
            df: DataFrame with DatetimeIndex
            target_frequency: Target frequency code

        Returns:
            bool: True if upsampling is needed
        """
        if not isinstance(df.index, pd.DatetimeIndex) or df.empty:
            return False

        # Calculate approximate frequency of current data
        time_diffs = df.index.to_series().diff()
        current_freq_days = time_diffs.median().days

        # Map target frequency to days
        freq_days_map = {"D": 1, "W": 7, "M": 30}
        target_days = freq_days_map.get(
            self.FREQUENCY_MAP.get(target_frequency.lower(), target_frequency), 30
        )

        return target_days < current_freq_days
