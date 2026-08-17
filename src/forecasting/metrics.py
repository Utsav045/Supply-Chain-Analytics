"""Performance metrics for demand forecasting models."""

from collections.abc import Sequence
from math import sqrt

import numpy as np
import pandas as pd
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)

MetricInput = Sequence[float] | np.ndarray | pd.Series


def _convert_metric_input(
    values: MetricInput,
    input_name: str,
) -> np.ndarray:
    """
    Convert metric input into a validated one-dimensional array.

    Args:
        values: Observed or predicted values.
        input_name: Name used in validation messages.

    Returns:
        One-dimensional floating-point NumPy array.
    """
    try:
        array = np.asarray(values, dtype=float)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{input_name} values must be numeric.") from exc

    if array.ndim != 1:
        raise ValueError(f"{input_name} values must be one-dimensional.")

    if array.size == 0:
        raise ValueError(f"{input_name} values cannot be empty.")

    if not np.isfinite(array).all():
        raise ValueError(f"{input_name} values must be finite.")

    return array


def calculate_safe_mape(
    actual: MetricInput,
    predicted: MetricInput,
) -> float | None:
    """
    Calculate MAPE while excluding zero actual-demand values.

    Args:
        actual: Observed demand.
        predicted: Forecast demand.

    Returns:
        MAPE as a percentage, or None when every actual value is zero.
    """
    actual_array = _convert_metric_input(actual, "Actual")
    predicted_array = _convert_metric_input(predicted, "Predicted")

    if actual_array.shape != predicted_array.shape:
        raise ValueError("Actual and predicted values must have matching shapes.")

    nonzero_mask = actual_array != 0

    if not nonzero_mask.any():
        return None

    percentage_errors = np.abs(
        (actual_array[nonzero_mask] - predicted_array[nonzero_mask])
        / actual_array[nonzero_mask]
    )

    return float(np.mean(percentage_errors) * 100)


def evaluate_forecast(
    actual: MetricInput,
    predicted: MetricInput,
) -> dict[str, float | None]:
    """
    Calculate the project's standard forecasting metrics.

    Args:
        actual: Observed demand values.
        predicted: Predicted demand values.

    Returns:
        MAE, MAPE, MSE, RMSE and R-squared results.
    """
    actual_array = _convert_metric_input(actual, "Actual")
    predicted_array = _convert_metric_input(predicted, "Predicted")

    if actual_array.shape != predicted_array.shape:
        raise ValueError("Actual and predicted values must have matching shapes.")

    mse = float(
        mean_squared_error(
            actual_array,
            predicted_array,
        )
    )

    if actual_array.size > 1 and not np.isclose(np.var(actual_array), 0.0):
        r2: float | None = float(
            r2_score(
                actual_array,
                predicted_array,
            )
        )
    else:
        r2 = None

    return {
        "mae": float(
            mean_absolute_error(
                actual_array,
                predicted_array,
            )
        ),
        "mape": calculate_safe_mape(
            actual_array,
            predicted_array,
        ),
        "mse": mse,
        "rmse": float(sqrt(mse)),
        "r2": r2,
    }
