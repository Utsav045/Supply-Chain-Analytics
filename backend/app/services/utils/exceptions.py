"""
Custom Exceptions for Supply Chain Analytics Platform.

Author: Antigravity AI
"""


class SupplyChainError(Exception):
    """Base exception for all Supply Chain Analytics errors."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class DataLoadError(SupplyChainError):
    """Exception raised when loading a dataset fails."""

    pass


class ValidationError(SupplyChainError):
    """Exception raised when dataset structure or content validation fails."""

    pass


class DataCleaningError(SupplyChainError):
    """Exception raised when data cleaning operations fail."""

    pass
