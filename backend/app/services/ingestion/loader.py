"""
Data Loader Service

Handles loading raw datasets (CSV, Excel, JSON) into pandas DataFrames.

Author: Antigravity AI
"""

import os
from typing import Union

import pandas as pd

from app.core.logger import logger
from app.services.utils.exceptions import DataLoadError


class DataLoader:
    """Service to load datasets from various file formats into pandas DataFrames."""

    @staticmethod
    def load_file(file_path: Union[str, os.PathLike]) -> pd.DataFrame:
        """
        Loads a data file (CSV or Excel) into a pandas DataFrame.

        Args:
            file_path: Path to the data file.

        Returns:
            pd.DataFrame: Loaded dataset.

        Raises:
            DataLoadError: If file loading fails due to missing file,
                           unsupported format, or pandas execution errors.
        """
        path_str = str(file_path)
        logger.info(f"Attempting to load file: {path_str}")

        if not os.path.exists(file_path):
            msg = f"File not found: {path_str}"
            logger.error(msg)
            raise DataLoadError(msg)

        _, ext = os.path.splitext(path_str.lower())

        try:
            if ext == ".csv":
                df = pd.read_csv(file_path)
            elif ext in (".xlsx", ".xls"):
                df = pd.read_excel(file_path)
            elif ext == ".json":
                df = pd.read_json(file_path)
            else:
                msg = (
                    f"Unsupported file extension '{ext}' for file: {path_str}. "
                    "Supported: .csv, .xlsx, .xls, .json"
                )
                logger.error(msg)
                raise DataLoadError(msg)

            logger.info(f"Successfully loaded file {path_str} with shape: {df.shape}")
            return df

        except DataLoadError:
            raise
        except Exception as e:
            msg = f"Failed to load file {path_str} due to error: {str(e)}"
            logger.exception(msg)
            raise DataLoadError(msg) from e
