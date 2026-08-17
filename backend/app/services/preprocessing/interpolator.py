"""
Missing Value Interpolation Service

Handles interpolation of missing values and dates in time-series data.
Supports multiple interpolation methods: linear, forward fill, backward fill,
and time-based interpolation.

Author: Antigravity AI
"""

from typing import Literal, Optional

import pandas as pd

from app.core.logger import logger
from app.services.utils.exceptions import DataCleaningError


class Interpolator:
    """
    Service for interpolating missing values in time-series data.

    Supports multiple interpolation methods:
    - linear: Linear interpolation between values
    - forward_fill: Propagate last valid value forward
    - backward_fill: Propagate next valid value backward
    - time: Interpolation accounting for time intervals

    Responsibilities:
    - Fill missing dates in time-series
    - Interpolate missing observations
    - Validate data continuity
    """

    # Supported interpolation methods
    SUPPORTED_METHODS = ["linear", "forward_fill", "backward_fill", "time"]

    def __init__(self):
        """Initialize the Interpolator."""
        pass

    def fill_missing_dates(
        self, df: pd.DataFrame, frequency: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Create a continuous date range and reindex DataFrame.

        Fills missing dates by creating a continuous index from min to max date
        and reindexing the DataFrame to include all dates.

        Args:
            df: DataFrame with DatetimeIndex
            frequency: Frequency for the continuous index (e.g., 'D', 'W', 'M')
                      If None, infers from existing data

        Returns:
            pd.DataFrame: DataFrame with continuous date index
                (but values still NaN for gaps)

        Raises:
            DataCleaningError: If operation fails
        """
        logger.info("Filling missing dates...")

        self._validate_datetime_index(df)

        try:
            # Create continuous date range
            date_range = pd.date_range(
                start=df.index.min(),
                end=df.index.max(),
                freq=frequency or "D",
            )

            # Reindex to include all dates
            df_reindexed = df.reindex(date_range)

            missing_dates = df_reindexed.isna().sum(axis=0)
            logger.info(
                f"Created continuous index. Total dates: {len(date_range)}, "
                f"Missing values per column: {missing_dates.to_dict()}"
            )

            return df_reindexed

        except DataCleaningError:
            raise
        except Exception as e:
            msg = f"Failed to fill missing dates: {str(e)}"
            logger.exception(msg)
            raise DataCleaningError(msg) from e

    def interpolate(
        self,
        df: pd.DataFrame,
        method: Literal["linear", "forward_fill", "backward_fill", "time"] = "linear",
        limit: Optional[int] = None,
        columns: Optional[list[str]] = None,
    ) -> pd.DataFrame:
        """
        Interpolate missing values using the specified method.

        Args:
            df: DataFrame with DatetimeIndex (may contain NaN values)
            method: Interpolation method
                ('linear', 'forward_fill', 'backward_fill', 'time')
            limit: Maximum number of consecutive NaN values to forward/backward fill
            columns: List of columns to interpolate.
                If None, interpolates all numeric columns

        Returns:
            pd.DataFrame: DataFrame with interpolated values

        Raises:
            DataCleaningError: If method is invalid or interpolation fails
        """
        if method not in self.SUPPORTED_METHODS:
            msg = (
                f"Unsupported interpolation method: {method}. "
                f"Supported: {self.SUPPORTED_METHODS}"
            )
            logger.error(msg)
            raise DataCleaningError(msg)

        logger.info(f"Interpolating missing values using method: {method}")

        self._validate_datetime_index(df)

        try:
            df = df.copy()

            # Select columns to interpolate
            if columns:
                cols_to_interpolate = columns
            else:
                cols_to_interpolate = df.select_dtypes(
                    include=["number"]
                ).columns.tolist()

            if not cols_to_interpolate:
                logger.warning("No numeric columns to interpolate")
                return df

            # Apply interpolation based on method
            if method == "linear":
                df[cols_to_interpolate] = df[cols_to_interpolate].interpolate(
                    method="linear",
                    limit=limit,
                )

            elif method == "time":
                df[cols_to_interpolate] = df[cols_to_interpolate].interpolate(
                    method="time",
                    limit=limit,
                )

            elif method == "forward_fill":
                df[cols_to_interpolate] = df[cols_to_interpolate].ffill(limit=limit)

            elif method == "backward_fill":
                df[cols_to_interpolate] = df[cols_to_interpolate].bfill(limit=limit)

            # Log interpolation results
            remaining_na = df[cols_to_interpolate].isna().sum()
            logger.info(
                f"Interpolation complete. "
                f"Remaining NaN values: {remaining_na.to_dict()}"
            )

            return df

        except DataCleaningError:
            raise
        except Exception as e:
            msg = f"Failed to interpolate data: {str(e)}"
            logger.exception(msg)
            raise DataCleaningError(msg) from e

    def forward_fill(
        self, df: pd.DataFrame, limit: Optional[int] = None
    ) -> pd.DataFrame:
        """
        Forward fill missing values (propagate last valid observation forward).

        Args:
            df: Input DataFrame
            limit: Maximum consecutive NaN to fill

        Returns:
            pd.DataFrame: Forward-filled DataFrame
        """
        return self.interpolate(df, method="forward_fill", limit=limit)

    def backward_fill(
        self, df: pd.DataFrame, limit: Optional[int] = None
    ) -> pd.DataFrame:
        """
        Backward fill missing values (propagate next valid observation backward).

        Args:
            df: Input DataFrame
            limit: Maximum consecutive NaN to fill

        Returns:
            pd.DataFrame: Backward-filled DataFrame
        """
        return self.interpolate(df, method="backward_fill", limit=limit)

    def validate_continuity(self, df: pd.DataFrame) -> bool:
        """
        Validate that the DataFrame has no missing timestamps in its DatetimeIndex.

        Args:
            df: DataFrame with DatetimeIndex to validate

        Returns:
            bool: True if continuous, False otherwise

        Raises:
            DataCleaningError: If validation fails
        """
        self._validate_datetime_index(df)

        try:
            # Check for gaps in the index
            if len(df) <= 1:
                return True

            time_diffs = df.index.to_series().diff()
            max_diff = time_diffs.max()

            # If max difference is more than 1 day (assuming daily data), there are gaps
            # This is a simple check; could be more sophisticated
            if max_diff > pd.Timedelta(days=1):
                logger.warning(
                    f"DataFrame has gaps in DatetimeIndex. Max gap: {max_diff}"
                )
                return False

            logger.info("DatetimeIndex is continuous")
            return True

        except DataCleaningError:
            raise
        except Exception as e:
            msg = f"Failed to validate continuity: {str(e)}"
            logger.exception(msg)
            raise DataCleaningError(msg) from e

    def get_missing_stats(self, df: pd.DataFrame) -> dict:
        """
        Calculate statistics about missing values in the DataFrame.

        Args:
            df: Input DataFrame

        Returns:
            dict: Statistics including:
                - total_rows: Total number of rows
                - total_cols: Total number of columns
                - missing_by_column: Dict of column → count of missing values
                - missing_percentage_by_column: Dict of column → percentage missing

        Raises:
            DataCleaningError: If operation fails
        """
        try:
            missing_counts = df.isna().sum()
            missing_percentages = (df.isna().sum() / len(df)) * 100

            stats = {
                "total_rows": len(df),
                "total_cols": len(df.columns),
                "total_missing": df.isna().sum().sum(),
                "missing_by_column": missing_counts.to_dict(),
                "missing_percentage_by_column": missing_percentages.to_dict(),
            }

            logger.info(f"Missing value statistics: {stats}")
            return stats

        except Exception as e:
            msg = f"Failed to calculate missing statistics: {str(e)}"
            logger.exception(msg)
            raise DataCleaningError(msg) from e

    def _validate_datetime_index(self, df: pd.DataFrame) -> None:
        """
        Validate that DataFrame has a DatetimeIndex.

        Args:
            df: DataFrame to validate

        Raises:
            DataCleaningError: If validation fails
        """
        if df is None or df.empty:
            msg = "DataFrame is empty or None"
            logger.error(msg)
            raise DataCleaningError(msg)

        if not isinstance(df.index, pd.DatetimeIndex):
            msg = "DataFrame must have a DatetimeIndex"
            logger.error(msg)
            raise DataCleaningError(msg)
