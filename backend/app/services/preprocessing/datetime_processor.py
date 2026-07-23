"""
DateTime Processing Service

Handles datetime operations including parsing, validation, indexing, and
sorting of time-series data. Ensures chronological ordering and removes
duplicate timestamps.

Author: Antigravity AI
"""

import pandas as pd

from app.core.constants import DATE_COLUMN
from app.core.logger import logger
from app.services.utils.exceptions import DataCleaningError


class DatetimeProcessor:
    """
    Service for processing and validating datetime columns in time-series data.

    Responsibilities:
    - Validate date column presence and format
    - Convert strings to datetime objects
    - Handle invalid date values
    - Sort data chronologically
    - Set datetime index
    - Remove duplicate timestamps
    """

    def __init__(self, date_column: str = DATE_COLUMN):
        """
        Initialize the DatetimeProcessor.

        Args:
            date_column: Name of the date column in the DataFrame (default: 'date')
        """
        self.date_column = date_column

    def process(
        self,
        df: pd.DataFrame,
        infer_datetime_format: bool = True,
        errors: str = "raise",
    ) -> pd.DataFrame:
        """
        Process and validate the datetime column in a DataFrame.

        Steps:
        1. Validate that the date column exists
        2. Convert to datetime format
        3. Handle invalid dates based on 'errors' parameter
        4. Sort chronologically
        5. Remove duplicate timestamps
        6. Set datetime as index

        Args:
            df: Input DataFrame containing a date column
            infer_datetime_format: Whether to infer datetime format (faster parsing)
            errors: How to handle errors ('raise', 'coerce', 'ignore')
                   - 'raise': Raise exception on invalid dates
                   - 'coerce': Convert invalid dates to NaT
                   - 'ignore': Return original column on error

        Returns:
            pd.DataFrame: Processed DataFrame with datetime index

        Raises:
            DataCleaningError: If date column is missing or processing fails
        """
        logger.info(f"Processing datetime column: {self.date_column}")

        # Validate column exists
        if self.date_column not in df.columns:
            msg = (
                f"Date column '{self.date_column}' not found in DataFrame. "
                f"Available columns: {list(df.columns)}"
            )
            logger.error(msg)
            raise DataCleaningError(msg)

        # Make a copy to avoid modifying the original
        df = df.copy()

        try:
            # Convert to datetime
            df[self.date_column] = pd.to_datetime(
                df[self.date_column],
                format="mixed",
                errors=errors,
            )

            # Remove rows with NaT (invalid dates)
            initial_rows = len(df)
            df = df.dropna(subset=[self.date_column])
            removed_invalid = initial_rows - len(df)

            if removed_invalid > 0:
                logger.warning(f"Removed {removed_invalid} rows with invalid dates")

            # Sort by date chronologically
            df = df.sort_values(by=self.date_column)
            logger.info(f"Sorted DataFrame by {self.date_column}")

            # Remove duplicate timestamps
            initial_rows = len(df)
            df = df.drop_duplicates(subset=[self.date_column], keep="first")
            removed_duplicates = initial_rows - len(df)

            if removed_duplicates > 0:
                logger.warning(f"Removed {removed_duplicates} duplicate timestamps")

            # Set datetime as index
            df = df.set_index(self.date_column)
            logger.info(
                f"Successfully processed datetime. Index shape: {df.index.shape}"
            )

            return df

        except DataCleaningError:
            raise
        except Exception as e:
            msg = f"Failed to process datetime column '{self.date_column}': {str(e)}"
            logger.exception(msg)
            raise DataCleaningError(msg) from e

    def validate_datetime_column(self, df: pd.DataFrame) -> bool:
        """
        Validate that the datetime column exists and is in datetime format.

        Args:
            df: DataFrame to validate

        Returns:
            bool: True if valid, False otherwise

        Raises:
            DataCleaningError: If validation fails
        """
        if self.date_column not in df.columns:
            msg = f"Date column '{self.date_column}' not found"
            logger.error(msg)
            raise DataCleaningError(msg)

        if not pd.api.types.is_datetime64_any_dtype(df[self.date_column]):
            msg = f"Column '{self.date_column}' is not in datetime format"
            logger.error(msg)
            raise DataCleaningError(msg)

        logger.info(f"DateTime column '{self.date_column}' is valid")
        return True

    def get_date_range(self, df: pd.DataFrame) -> tuple[pd.Timestamp, pd.Timestamp]:
        """
        Get the min and max dates from the DataFrame.

        Args:
            df: DataFrame with datetime index or column

        Returns:
            tuple: (min_date, max_date)

        Raises:
            DataCleaningError: If datetime column is invalid
        """
        if isinstance(df.index, pd.DatetimeIndex):
            min_date = df.index.min()
            max_date = df.index.max()
        elif self.date_column in df.columns:
            self.validate_datetime_column(df)
            min_date = df[self.date_column].min()
            max_date = df[self.date_column].max()
        else:
            msg = f"No valid datetime column found (looking for: {self.date_column})"
            logger.error(msg)
            raise DataCleaningError(msg)

        logger.info(f"Date range: {min_date} to {max_date}")
        return (min_date, max_date)

    def remove_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Remove duplicate timestamps from DataFrame.

        Args:
            df: Input DataFrame with datetime index

        Returns:
            pd.DataFrame: DataFrame with duplicates removed

        Raises:
            DataCleaningError: If operation fails
        """
        try:
            if not isinstance(df.index, pd.DatetimeIndex):
                msg = "DataFrame index must be a DatetimeIndex"
                logger.error(msg)
                raise DataCleaningError(msg)

            initial_rows = len(df)
            df = df[~df.index.duplicated(keep="first")]
            removed = initial_rows - len(df)

            if removed > 0:
                logger.info(f"Removed {removed} duplicate timestamps")

            return df

        except DataCleaningError:
            raise
        except Exception as e:
            msg = f"Failed to remove duplicates: {str(e)}"
            logger.exception(msg)
            raise DataCleaningError(msg) from e
