"""Walk-forward backtesting for demand forecasting models."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import cast

import pandas as pd

from src.forecasting.base import BaseForecaster
from src.forecasting.metrics import evaluate_forecast
from src.forecasting.model_validation import (
    ModelInputValidationError,
    validate_confidence_level,
    validate_demand_series,
    validate_exogenous_features,
)

ForecasterFactory = Callable[[], BaseForecaster]


@dataclass(frozen=True, slots=True)
class BacktestResult:
    """Contain predictions and metrics from walk-forward validation."""

    model_name: str
    predictions: pd.DataFrame
    metrics: dict[str, float | None]


def _validate_forecast_output(
    forecast: pd.DataFrame,
    expected_date: pd.Timestamp,
) -> None:
    """
    Validate one-step output returned by a forecasting model.

    Args:
        forecast: Forecast output returned by the model.
        expected_date: Date that should be present in the forecast.

    Raises:
        ModelInputValidationError: If the output structure is invalid.
    """
    required_columns = {
        "predicted_demand",
        "lower_bound",
        "upper_bound",
    }

    if not isinstance(forecast, pd.DataFrame):
        raise ModelInputValidationError(
            "Forecasting models must return a pandas DataFrame."
        )

    missing_columns = required_columns.difference(forecast.columns)

    if missing_columns:
        missing_text = ", ".join(sorted(missing_columns))

        raise ModelInputValidationError(
            f"Forecast output is missing columns: {missing_text}."
        )

    if len(forecast) != 1:
        raise ModelInputValidationError(
            "Walk-forward validation requires one forecast observation."
        )

    forecast_date = pd.Timestamp(forecast.index[0])

    if forecast_date != expected_date:
        raise ModelInputValidationError(
            "Forecast date does not match the evaluation date."
        )


def walk_forward_backtest(
    series: pd.Series,
    model_factory: ForecasterFactory,
    initial_train_size: int,
    exogenous: pd.DataFrame | None = None,
    confidence_level: float = 0.95,
) -> BacktestResult:
    """
    Evaluate a forecasting model using expanding-window validation.

    A fresh model is trained on all observations available before each
    evaluation date. It then predicts the next observation.

    Args:
        series: Complete historical demand series.
        model_factory: Callable returning a new forecasting model.
        initial_train_size: Number of observations in the first window.
        exogenous: Optional aligned external variables.
        confidence_level: Confidence level used for prediction bounds.

    Returns:
        Backtest predictions and aggregate evaluation metrics.

    Raises:
        ModelInputValidationError: If the configuration is invalid.
    """
    if not isinstance(initial_train_size, int) or isinstance(
        initial_train_size,
        bool,
    ):
        raise ModelInputValidationError("initial_train_size must be an integer.")

    if initial_train_size < 3:
        raise ModelInputValidationError("initial_train_size must be at least three.")

    validated_confidence = validate_confidence_level(confidence_level)

    validated_series = validate_demand_series(
        series,
        minimum_observations=initial_train_size + 1,
    )

    if initial_train_size >= len(validated_series):
        raise ModelInputValidationError(
            "initial_train_size must be smaller than the series."
        )

    validated_exogenous: pd.DataFrame | None = None

    if exogenous is not None:
        validated_index = cast(
            pd.DatetimeIndex,
            validated_series.index,
        )

        validated_exogenous = validate_exogenous_features(
            exogenous,
            expected_index=validated_index,
        )

    prediction_rows: list[dict[str, object]] = []
    resolved_model_name: str | None = None

    for position in range(
        initial_train_size,
        len(validated_series),
    ):
        model = model_factory()

        if not isinstance(model, BaseForecaster):
            raise ModelInputValidationError(
                "model_factory must return a BaseForecaster instance."
            )

        training_series = validated_series.iloc[:position]
        evaluation_date = pd.Timestamp(validated_series.index[position])
        actual_demand = float(validated_series.iloc[position])

        training_exogenous: pd.DataFrame | None = None
        future_exogenous: pd.DataFrame | None = None

        if validated_exogenous is not None:
            training_exogenous = validated_exogenous.iloc[:position].copy()

            future_exogenous = validated_exogenous.iloc[position : position + 1].copy()

        model.fit(
            training_series,
            exogenous=training_exogenous,
        )

        forecast = model.predict(
            horizon=1,
            future_exogenous=future_exogenous,
            confidence_level=validated_confidence,
        )

        _validate_forecast_output(
            forecast,
            expected_date=evaluation_date,
        )

        if resolved_model_name is None:
            resolved_model_name = model.model_name
        elif resolved_model_name != model.model_name:
            raise ModelInputValidationError(
                "model_factory returned inconsistent model types."
            )

        forecast_row = forecast.iloc[0]

        prediction_rows.append(
            {
                "forecast_date": evaluation_date,
                "actual_demand": actual_demand,
                "predicted_demand": float(forecast_row["predicted_demand"]),
                "lower_bound": float(forecast_row["lower_bound"]),
                "upper_bound": float(forecast_row["upper_bound"]),
            }
        )

    if not prediction_rows:
        raise ModelInputValidationError(
            "Walk-forward validation produced no forecasts."
        )

    predictions = pd.DataFrame(prediction_rows).set_index("forecast_date").sort_index()

    metrics = evaluate_forecast(
        actual=predictions["actual_demand"],
        predicted=predictions["predicted_demand"],
    )

    if resolved_model_name is None:
        raise ModelInputValidationError(
            "Walk-forward validation could not determine the model name."
        )

    return BacktestResult(
        model_name=resolved_model_name,
        predictions=predictions,
        metrics=metrics,
    )
