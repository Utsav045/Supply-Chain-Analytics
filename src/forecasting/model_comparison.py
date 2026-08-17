"""Comparison and ranking of forecasting backtest results."""

from collections.abc import Sequence
from dataclasses import dataclass

import numpy as np
import pandas as pd

from src.forecasting.backtesting import BacktestResult
from src.forecasting.model_validation import ModelInputValidationError

METRIC_DIRECTIONS = {
    "mae": "minimize",
    "mape": "minimize",
    "mse": "minimize",
    "rmse": "minimize",
    "r2": "maximize",
}


@dataclass(frozen=True, slots=True)
class ModelComparisonResult:
    """Contain the ranked forecasting model results."""

    primary_metric: str
    best_model_name: str
    ranking: pd.DataFrame


def compare_backtest_results(
    results: Sequence[BacktestResult],
    primary_metric: str = "rmse",
) -> ModelComparisonResult:
    """
    Rank forecasting models using their backtest metrics.

    Args:
        results: Completed model backtest results.
        primary_metric: Metric used to select the best model.

    Returns:
        Ranked model-performance table and winning model name.

    Raises:
        ModelInputValidationError: If comparison data is invalid.
    """
    normalized_metric = primary_metric.strip().lower()

    if normalized_metric not in METRIC_DIRECTIONS:
        supported = ", ".join(METRIC_DIRECTIONS)

        raise ModelInputValidationError(
            f"Unsupported comparison metric. Use one of: {supported}."
        )

    if not results:
        raise ModelInputValidationError("At least one backtest result is required.")

    model_names: set[str] = set()
    records: list[dict[str, object]] = []

    for result in results:
        if not isinstance(result, BacktestResult):
            raise ModelInputValidationError(
                "All comparison inputs must be BacktestResult objects."
            )

        if result.model_name in model_names:
            raise ModelInputValidationError(
                f"Duplicate model result: {result.model_name}."
            )

        model_names.add(result.model_name)

        if normalized_metric not in result.metrics:
            raise ModelInputValidationError(
                f"{result.model_name} does not contain {normalized_metric}."
            )

        raw_value = result.metrics[normalized_metric]

        if raw_value is None:
            raise ModelInputValidationError(
                f"{normalized_metric} is unavailable for {result.model_name}."
            )

        try:
            metric_value = float(raw_value)
        except (TypeError, ValueError) as exc:
            raise ModelInputValidationError(
                f"{normalized_metric} must be numeric for {result.model_name}."
            ) from exc

        if not np.isfinite(metric_value):
            raise ModelInputValidationError(
                f"{normalized_metric} must be finite for {result.model_name}."
            )

        record: dict[str, object] = {
            "model_name": result.model_name,
        }

        record.update(result.metrics)
        records.append(record)

    ranking = pd.DataFrame.from_records(records)

    ascending = METRIC_DIRECTIONS[normalized_metric] == "minimize"

    ranking = ranking.sort_values(
        by=[
            normalized_metric,
            "model_name",
        ],
        ascending=[
            ascending,
            True,
        ],
        kind="stable",
    ).reset_index(drop=True)

    ranking.insert(
        loc=0,
        column="rank",
        value=range(1, len(ranking) + 1),
    )

    best_model_name = str(ranking.iloc[0]["model_name"])

    return ModelComparisonResult(
        primary_metric=normalized_metric,
        best_model_name=best_model_name,
        ranking=ranking,
    )
