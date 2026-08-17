"""
Data Validator Service

Validates the structure and data types of datasets to ensure compatibility with
the platform schemas and database models.

Author: Antigravity AI
"""

from typing import List

import pandas as pd
from app.core.constants import (CATEGORY_COLUMN, DATE_COLUMN, INVENTORY_COLUMN,
                                PRICE_COLUMN, PRODUCT_ID_COLUMN,
                                PRODUCT_NAME_COLUMN, SALES_COLUMN)
from app.core.logger import logger
from app.services.utils.exceptions import ValidationError


class DataValidator:
    """Service to validate pandas DataFrames against schemas and content rules."""

    REQUIRED_COLUMNS_MAP = {
        "sales": [DATE_COLUMN, PRODUCT_ID_COLUMN, SALES_COLUMN, PRICE_COLUMN],
        "inventory": [DATE_COLUMN, PRODUCT_ID_COLUMN, INVENTORY_COLUMN],
        "product": [
            PRODUCT_ID_COLUMN,
            PRODUCT_NAME_COLUMN,
            CATEGORY_COLUMN,
            PRICE_COLUMN,
        ],
    }

    @classmethod
    def validate_not_empty(cls, df: pd.DataFrame) -> None:
        """
        Validates that the DataFrame is not empty.

        Raises:
            ValidationError: If the DataFrame is empty.
        """
        if df is None or df.empty:
            msg = "Dataset is empty or None."
            logger.error(msg)
            raise ValidationError(msg)

    @classmethod
    def validate_columns(cls, df: pd.DataFrame, required_columns: List[str]) -> None:
        """
        Validates that all required columns are present in the DataFrame.

        Raises:
            ValidationError: If any required column is missing.
        """
        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            msg = f"Missing required columns: {', '.join(missing_cols)}"
            logger.error(msg)
            raise ValidationError(msg)

    @classmethod
    def validate_data_types(cls, df: pd.DataFrame, dataset_type: str) -> None:
        """
        Validates that columns have correct/convertible data types.

        Raises:
            ValidationError: If data type conversion/validation fails.
        """
        if dataset_type == "sales":
            cls._check_date_column(df, DATE_COLUMN)
            cls._check_numeric_column(df, SALES_COLUMN)
            cls._check_numeric_column(df, PRICE_COLUMN)
        elif dataset_type == "inventory":
            cls._check_date_column(df, DATE_COLUMN)
            cls._check_numeric_column(df, INVENTORY_COLUMN)
        elif dataset_type == "product":
            cls._check_numeric_column(df, PRICE_COLUMN)

    @classmethod
    def validate_dataset(cls, df: pd.DataFrame, dataset_type: str) -> None:
        """
        Runs full validation on a dataset of a given type.

        Args:
            df: The DataFrame to validate.
            dataset_type: The type of dataset ('sales', 'inventory', 'product').

        Raises:
            ValidationError: If any validation rule fails.
        """
        logger.info(f"Starting schema validation for dataset type: {dataset_type}")
        cls.validate_not_empty(df)

        if dataset_type not in cls.REQUIRED_COLUMNS_MAP:
            supported = list(cls.REQUIRED_COLUMNS_MAP.keys())
            msg = f"Unknown dataset type: {dataset_type}. Supported: {supported}"
            logger.error(msg)
            raise ValidationError(msg)

        required = cls.REQUIRED_COLUMNS_MAP[dataset_type]
        cls.validate_columns(df, required)
        cls.validate_data_types(df, dataset_type)
        logger.info(f"Dataset of type '{dataset_type}' successfully validated.")

    @staticmethod
    def _check_date_column(df: pd.DataFrame, col: str) -> None:
        """Helper to verify if a column is or can be cast to date/datetime."""
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            return
        try:
            pd.to_datetime(df[col].dropna().head(10), errors="raise")
        except Exception as e:
            msg = f"Column '{col}' is not a valid date format. Error: {str(e)}"
            logger.error(msg)
            raise ValidationError(msg) from e

    @staticmethod
    def _check_numeric_column(df: pd.DataFrame, col: str) -> None:
        """Helper to verify if a column is or can be cast to numeric."""
        if pd.api.types.is_numeric_dtype(df[col]):
            return
        try:
            pd.to_numeric(df[col].dropna().head(10), errors="raise")
        except Exception as e:
            msg = f"Column '{col}' must be numeric. Error: {str(e)}"
            logger.error(msg)
            raise ValidationError(msg) from e
