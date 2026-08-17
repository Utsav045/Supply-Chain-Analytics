"""
Data Cleaner Service

Cleans and standardizes datasets by handling duplicates, missing values,
and negative values in key metrics.

Author: Antigravity AI
"""

import pandas as pd
from app.core.constants import (CATEGORY_COLUMN, DATE_COLUMN, INVENTORY_COLUMN,
                                PRICE_COLUMN, PRODUCT_ID_COLUMN,
                                PRODUCT_NAME_COLUMN, SALES_COLUMN)
from app.core.logger import logger
from app.services.utils.exceptions import DataCleaningError


class DataCleaner:
    """Service to clean and standardize datasets."""

    @classmethod
    def clean_dataset(cls, df: pd.DataFrame, dataset_type: str) -> pd.DataFrame:
        """
        Main entry point for cleaning a dataset of a given type.

        Args:
            df: The DataFrame to clean.
            dataset_type: The type of dataset ('sales', 'inventory', 'product').

        Returns:
            pd.DataFrame: Cleaned and standardized DataFrame.

        Raises:
            DataCleaningError: If cleaning fails.
        """
        logger.info(f"Starting data cleaning for dataset type: {dataset_type}")
        if df is None:
            raise DataCleaningError("Cannot clean None DataFrame")

        try:
            # 1. Create a copy to avoid side-effects on original data
            cleaned_df = df.copy()

            # 2. Remove duplicate rows
            cleaned_df = cls.remove_duplicates(cleaned_df)

            # 3. Standardize column data types
            cleaned_df = cls.standardize_types(cleaned_df, dataset_type)

            # 4. Handle missing values
            cleaned_df = cls.impute_missing_values(cleaned_df, dataset_type)

            # 5. Handle negative values in numeric columns
            cleaned_df = cls.correct_negative_values(cleaned_df, dataset_type)

            logger.info(f"Finished data cleaning. Output shape: {cleaned_df.shape}")
            return cleaned_df

        except Exception as e:
            msg = f"Data cleaning failed for type '{dataset_type}': {str(e)}"
            logger.exception(msg)
            raise DataCleaningError(msg) from e

    @classmethod
    def remove_duplicates(cls, df: pd.DataFrame) -> pd.DataFrame:
        """Removes duplicate rows from the DataFrame."""
        initial_len = len(df)
        df_no_dup = df.drop_duplicates()
        removed = initial_len - len(df_no_dup)
        if removed > 0:
            logger.info(f"Removed {removed} duplicate rows.")
        return df_no_dup

    @classmethod
    def standardize_types(cls, df: pd.DataFrame, dataset_type: str) -> pd.DataFrame:
        """Standardizes data types: dates to datetime, numerics to floats/ints."""
        if DATE_COLUMN in df.columns:
            df[DATE_COLUMN] = pd.to_datetime(df[DATE_COLUMN])

        # Cast identifiers/strings to string
        if PRODUCT_ID_COLUMN in df.columns:
            df[PRODUCT_ID_COLUMN] = df[PRODUCT_ID_COLUMN].astype(str).str.strip()

        if dataset_type == "sales":
            df[SALES_COLUMN] = pd.to_numeric(df[SALES_COLUMN], errors="coerce")
            df[PRICE_COLUMN] = pd.to_numeric(df[PRICE_COLUMN], errors="coerce")
        elif dataset_type == "inventory":
            df[INVENTORY_COLUMN] = pd.to_numeric(df[INVENTORY_COLUMN], errors="coerce")
        elif dataset_type == "product":
            if PRODUCT_NAME_COLUMN in df.columns:
                df[PRODUCT_NAME_COLUMN] = (
                    df[PRODUCT_NAME_COLUMN].astype(str).str.strip()
                )
            if CATEGORY_COLUMN in df.columns:
                df[CATEGORY_COLUMN] = df[CATEGORY_COLUMN].astype(str).str.strip()
            df[PRICE_COLUMN] = pd.to_numeric(df[PRICE_COLUMN], errors="coerce")

        return df

    @classmethod
    def impute_missing_values(cls, df: pd.DataFrame, dataset_type: str) -> pd.DataFrame:
        """
        Imputes missing values:
        - Numeric columns: filled with median.
        - Categorical/String columns: filled with mode or a default string.
        """
        for column in df.columns:
            if df[column].isnull().any():
                missing_count = df[column].isnull().sum()
                logger.info(
                    f"Column '{column}' has {missing_count} missing values. Imputing..."
                )

                if pd.api.types.is_numeric_dtype(df[column]):
                    median_val = df[column].median()
                    if pd.isna(median_val):
                        median_val = 0.0
                    df[column] = df[column].fillna(median_val)
                else:
                    non_nulls = df[column].dropna()
                    if len(non_nulls) > 0:
                        mode_val = non_nulls.mode()[0]
                    else:
                        mode_val = "Unknown"
                    df[column] = df[column].fillna(mode_val)
        return df

    @classmethod
    def correct_negative_values(
        cls, df: pd.DataFrame, dataset_type: str
    ) -> pd.DataFrame:
        """
        Identifies negative values in non-negative numeric fields and resets them
        to the median of non-negative values (or 0.0 if not available).
        """
        numeric_cols = []
        if dataset_type == "sales":
            numeric_cols = [SALES_COLUMN, PRICE_COLUMN]
        elif dataset_type == "inventory":
            numeric_cols = [INVENTORY_COLUMN]
        elif dataset_type == "product":
            numeric_cols = [PRICE_COLUMN]

        for col in numeric_cols:
            if col in df.columns:
                negatives = (df[col] < 0).sum()
                if negatives > 0:
                    non_neg_data = df[df[col] >= 0][col]
                    median_val = non_neg_data.median()
                    if pd.isna(median_val) or median_val < 0:
                        median_val = 0.0

                    if pd.api.types.is_integer_dtype(df[col]):
                        median_val = int(round(median_val))

                    logger.warning(
                        f"Found {negatives} negative values in column '{col}'. "
                        f"Replacing with median {median_val}."
                    )
                    df.loc[df[col] < 0, col] = median_val

        return df
