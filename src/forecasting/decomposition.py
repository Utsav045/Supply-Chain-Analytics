"""Trend and seasonal decomposition for demand time series."""

import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose

from src.forecasting.model_validation import (
    ModelInputValidationError,
    validate_demand_series,
)

SUPPORTED_MODELS = {
    "additive",
    "multiplicative",
}


def decompose_time_series(
    series: pd.Series,
    period: int,
    model: str = "additive",
) -> pd.DataFrame:
    """
    Decompose demand into observed, trend, seasonal and residual parts.

    Args:
        series: Historical demand series.
        period: Number of observations in one seasonal cycle.
        model: Additive or multiplicative decomposition.

    Returns:
        DataFrame containing the decomposition components.

    Raises:
        ModelInputValidationError: If decomposition cannot be performed.
    """
    if not isinstance(period, int) or isinstance(period, bool):
        raise ModelInputValidationError("Decomposition period must be an integer.")

    if period < 2:
        raise ModelInputValidationError("Decomposition period must be at least two.")

    if not isinstance(model, str):
        raise ModelInputValidationError("Decomposition model must be text.")

    normalized_model = model.strip().lower()

    if normalized_model not in SUPPORTED_MODELS:
        raise ModelInputValidationError(
            "Decomposition model must be additive or multiplicative."
        )

    validated_series = validate_demand_series(
        series,
        minimum_observations=period * 2,
    )

    if normalized_model == "multiplicative" and (validated_series <= 0).any():
        raise ModelInputValidationError(
            "Multiplicative decomposition requires positive values."
        )

    try:
        decomposition = seasonal_decompose(
            validated_series,
            model=normalized_model,
            period=period,
            extrapolate_trend="freq",
        )
    except ValueError as exc:
        raise ModelInputValidationError(
            "Unable to decompose the supplied demand series."
        ) from exc

    result = pd.DataFrame(
        {
            "observed": decomposition.observed,
            "trend": decomposition.trend,
            "seasonal": decomposition.seasonal,
            "residual": decomposition.resid,
        },
        index=validated_series.index,
    )

    result.index.name = validated_series.index.name or "date"

    return result
