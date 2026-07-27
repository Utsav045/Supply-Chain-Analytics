"""Chronological splitting utilities for time-series modelling."""

from dataclasses import dataclass
from math import ceil

import pandas as pd

from src.forecasting.model_validation import (
    ModelInputValidationError,
    validate_demand_series,
    validate_exogenous_features,
)


@dataclass(frozen=True, slots=True)
class ChronologicalSplit:
    """Contain chronologically separated training and test data."""

    train_series: pd.Series
    test_series: pd.Series
    train_exogenous: pd.DataFrame | None = None
    test_exogenous: pd.DataFrame | None = None


def chronological_train_test_split(
    series: pd.Series,
    test_size: int | None = None,
    test_ratio: float = 0.20,
    exogenous: pd.DataFrame | None = None,
    minimum_train_size: int = 3,
) -> ChronologicalSplit:
    """
    Split time-series data without random shuffling.

    The oldest observations are assigned to training, while the newest
    observations are reserved for evaluation.

    Args:
        series: Historical demand series.
        test_size: Explicit number of observations assigned to testing.
        test_ratio: Proportion assigned to testing when test_size is None.
        exogenous: Optional external variables aligned with demand.
        minimum_train_size: Minimum allowable training observations.

    Returns:
        Chronologically separated training and test datasets.

    Raises:
        ModelInputValidationError: If the split configuration is invalid.
    """
    if not isinstance(minimum_train_size, int) or isinstance(
        minimum_train_size,
        bool,
    ):
        raise ModelInputValidationError("minimum_train_size must be an integer.")

    if minimum_train_size <= 0:
        raise ModelInputValidationError("minimum_train_size must be greater than zero.")

    validated_series = validate_demand_series(
        series,
        minimum_observations=minimum_train_size + 1,
    )

    if test_size is None:
        if isinstance(test_ratio, bool) or not isinstance(
            test_ratio,
            int | float,
        ):
            raise ModelInputValidationError("test_ratio must be numeric.")

        validated_ratio = float(test_ratio)

        if not 0 < validated_ratio < 1:
            raise ModelInputValidationError("test_ratio must be between zero and one.")

        resolved_test_size = max(
            1,
            ceil(len(validated_series) * validated_ratio),
        )
    else:
        if not isinstance(test_size, int) or isinstance(
            test_size,
            bool,
        ):
            raise ModelInputValidationError("test_size must be an integer.")

        if test_size <= 0:
            raise ModelInputValidationError("test_size must be greater than zero.")

        resolved_test_size = test_size

    if resolved_test_size >= len(validated_series):
        raise ModelInputValidationError(
            "Test data must be smaller than the complete series."
        )

    train_size = len(validated_series) - resolved_test_size

    if train_size < minimum_train_size:
        raise ModelInputValidationError(
            f"Training data must contain at least "
            f"{minimum_train_size} observations."
        )

    train_series = validated_series.iloc[:train_size].copy()
    test_series = validated_series.iloc[train_size:].copy()

    train_exogenous: pd.DataFrame | None = None
    test_exogenous: pd.DataFrame | None = None

    if exogenous is not None:
        validated_exogenous = validate_exogenous_features(
            exogenous,
            expected_index=validated_series.index,
        )

        train_exogenous = validated_exogenous.iloc[:train_size].copy()
        test_exogenous = validated_exogenous.iloc[train_size:].copy()

    return ChronologicalSplit(
        train_series=train_series,
        test_series=test_series,
        train_exogenous=train_exogenous,
        test_exogenous=test_exogenous,
    )
