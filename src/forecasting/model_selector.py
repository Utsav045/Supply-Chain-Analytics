"""Automatic selection of the best forecasting model."""

from collections.abc import Mapping
from dataclasses import dataclass

import numpy as np
import pandas as pd

from src.forecasting.backtesting import (
    BacktestResult,
    ForecasterFactory,
    walk_forward_backtest,
)
from src.forecasting.base import BaseForecaster
from src.forecasting.model_comparison import (
    ModelComparisonResult,
    compare_backtest_results,
)
from src.forecasting.model_validation import (
    ModelInputValidationError,
)


@dataclass(frozen=True, slots=True)
class ModelSelectionResult:
    """Contain automatic forecasting-model selection results."""

    selected_model_name: str
    selected_model: BaseForecaster
    comparison: ModelComparisonResult
    backtests: dict[str, BacktestResult]
    failures: dict[str, str]


class AutomaticModelSelector:
    """Backtest candidate models and fit the best performer."""

    def __init__(
        self,
        model_factories: Mapping[
            str,
            ForecasterFactory,
        ],
        primary_metric: str = "rmse",
    ) -> None:
        """
        Initialize the model selector.

        Args:
            model_factories: Named forecasting-model factories.
            primary_metric: Metric used to identify the winner.
        """
        if not model_factories:
            raise ModelInputValidationError("At least one model factory is required.")

        validated_factories: dict[
            str,
            ForecasterFactory,
        ] = {}

        for model_name, factory in model_factories.items():
            cleaned_name = model_name.strip()

            if not cleaned_name:
                raise ModelInputValidationError("Model factory names cannot be empty.")

            if not callable(factory):
                raise ModelInputValidationError(
                    f"Factory for {cleaned_name} must be callable."
                )

            validated_factories[cleaned_name] = factory

        self._model_factories = validated_factories
        self._primary_metric = primary_metric

    def select(
        self,
        series: pd.Series,
        initial_train_size: int,
        exogenous: pd.DataFrame | None = None,
        confidence_level: float = 0.95,
    ) -> ModelSelectionResult:
        """
        Backtest all candidates and fit the best model on full data.

        Candidates that fail during backtesting are recorded and
        excluded, provided at least one candidate completes.

        Args:
            series: Complete historical demand.
            initial_train_size: First backtesting training-window size.
            exogenous: Optional external regressors.
            confidence_level: Forecast interval confidence level.

        Returns:
            Fitted winning model and complete comparison results.
        """
        successful_backtests: dict[
            str,
            BacktestResult,
        ] = {}

        failures: dict[str, str] = {}

        for expected_name, factory in self._model_factories.items():
            try:
                backtest = walk_forward_backtest(
                    series=series,
                    model_factory=factory,
                    initial_train_size=initial_train_size,
                    exogenous=exogenous,
                    confidence_level=confidence_level,
                )

                if backtest.model_name != expected_name:
                    raise ModelInputValidationError(
                        f"Factory registered as {expected_name} "
                        f"returned {backtest.model_name}."
                    )

                successful_backtests[expected_name] = backtest

            except (
                ValueError,
                TypeError,
                RuntimeError,
                np.linalg.LinAlgError,
            ) as exc:
                failures[expected_name] = str(exc)

        if not successful_backtests:
            failure_summary = "; ".join(
                f"{name}: {message}" for name, message in failures.items()
            )

            raise ModelInputValidationError(
                "Every forecasting candidate failed. " f"{failure_summary}"
            )

        comparison = compare_backtest_results(
            list(successful_backtests.values()),
            primary_metric=self._primary_metric,
        )

        selected_name = comparison.best_model_name
        selected_factory = self._model_factories[selected_name]
        selected_model = selected_factory()

        if not isinstance(selected_model, BaseForecaster):
            raise ModelInputValidationError(
                "The selected factory did not return a " "BaseForecaster instance."
            )

        selected_model.fit(
            series,
            exogenous=exogenous,
        )

        return ModelSelectionResult(
            selected_model_name=selected_name,
            selected_model=selected_model,
            comparison=comparison,
            backtests=successful_backtests,
            failures=failures,
        )
