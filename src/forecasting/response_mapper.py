"""Convert internal forecasting results into API schemas."""

from datetime import UTC, datetime
from typing import Any

import numpy as np
import pandas as pd

from src.forecasting.model_validation import (
    ModelInputValidationError,
)
from src.forecasting.schemas import (
    ForecastMetrics,
    ForecastPoint,
    ForecastResponse,
)
from src.services.forecasting_service import (
    ForecastingServiceResult,
)

REQUIRED_FORECAST_COLUMNS = {
    "predicted_demand",
    "lower_bound",
    "upper_bound",
}


def _to_utc_datetime(
    value: Any,
) -> datetime:
    """Convert a forecast timestamp into a UTC-aware datetime."""
    try:
        timestamp = pd.Timestamp(value)
    except (TypeError, ValueError) as exc:
        raise ModelInputValidationError(
            "forecast_date must be a valid datetime."
        ) from exc

    if pd.isna(timestamp):
        raise ModelInputValidationError("forecast_date cannot be missing.")

    if timestamp.tzinfo is None:
        timestamp = timestamp.tz_localize(UTC)
    else:
        timestamp = timestamp.tz_convert(UTC)

    return timestamp.to_pydatetime()


def _finite_float(
    value: Any,
    field_name: str,
) -> float:
    """Convert one value into a finite float."""
    try:
        converted = float(value)
    except (TypeError, ValueError) as exc:
        raise ModelInputValidationError(f"{field_name} must be numeric.") from exc

    if not np.isfinite(converted):
        raise ModelInputValidationError(f"{field_name} must be finite.")

    return converted


def _required_metric(
    metrics: dict[str, float | None],
    metric_name: str,
) -> float:
    """Return a required forecasting metric."""
    if metric_name not in metrics:
        raise ModelInputValidationError(f"Required metric is missing: {metric_name}.")

    value = metrics[metric_name]

    if value is None:
        raise ModelInputValidationError(
            f"Required metric cannot be None: {metric_name}."
        )

    return _finite_float(
        value,
        metric_name,
    )


def _optional_metric(
    metrics: dict[str, float | None],
    metric_name: str,
) -> float | None:
    """Return an optional forecasting metric."""
    value = metrics.get(metric_name)

    if value is None:
        return None

    return _finite_float(
        value,
        metric_name,
    )


def build_forecast_response(
    result: ForecastingServiceResult,
) -> ForecastResponse:
    """
    Convert a service result into the public response schema.

    Args:
        result: Internal forecasting operation result.

    Returns:
        Validated API-facing forecast response.
    """
    if not isinstance(result, ForecastingServiceResult):
        raise ModelInputValidationError("result must be a ForecastingServiceResult.")

    forecast = result.forecasts

    if not isinstance(forecast, pd.DataFrame):
        raise ModelInputValidationError("Forecast output must be a pandas DataFrame.")

    if not isinstance(forecast.index, pd.DatetimeIndex):
        raise ModelInputValidationError("Forecast output must use a DatetimeIndex.")

    missing_columns = REQUIRED_FORECAST_COLUMNS.difference(forecast.columns)

    if missing_columns:
        missing_text = ", ".join(sorted(missing_columns))

        raise ModelInputValidationError(
            f"Forecast output is missing columns: {missing_text}."
        )

    if len(forecast) != result.forecast_horizon:
        raise ModelInputValidationError(
            "Forecast output length does not match " "forecast_horizon."
        )

    forecast_points = [
        ForecastPoint(
            forecast_date=_to_utc_datetime(
                forecast_date,
            ),
            predicted_demand=_finite_float(
                row["predicted_demand"],
                "predicted_demand",
            ),
            lower_bound=_finite_float(
                row["lower_bound"],
                "lower_bound",
            ),
            upper_bound=_finite_float(
                row["upper_bound"],
                "upper_bound",
            ),
        )
        for forecast_date, row in forecast.iterrows()
    ]

    metrics = ForecastMetrics(
        mae=_required_metric(
            result.metrics,
            "mae",
        ),
        mape=_optional_metric(
            result.metrics,
            "mape",
        ),
        mse=_required_metric(
            result.metrics,
            "mse",
        ),
        rmse=_required_metric(
            result.metrics,
            "rmse",
        ),
        r2=_optional_metric(
            result.metrics,
            "r2",
        ),
    )

    return ForecastResponse(
        sku_id=result.sku_id,
        location_id=result.location_id,
        model_name=result.model_name,
        forecast_horizon=result.forecast_horizon,
        generated_at=result.generated_at,
        metrics=metrics,
        forecasts=forecast_points,
        model_artifact_id=result.model_artifact_id,
    )
