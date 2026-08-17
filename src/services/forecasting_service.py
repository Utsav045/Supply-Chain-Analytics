"""Production orchestration service for demand forecasting."""

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import UTC, datetime
from functools import partial
from math import ceil

import pandas as pd

from src.forecasting.arima import ARIMAForecaster
from src.forecasting.arima_config import ARIMAConfig
from src.forecasting.backtesting import ForecasterFactory
from src.forecasting.base import BaseForecaster
from src.forecasting.model_selector import AutomaticModelSelector
from src.forecasting.model_validation import ModelInputValidationError
from src.forecasting.moving_average import MovingAverageForecaster
from src.forecasting.persistence import ModelStore
from src.forecasting.schemas import ForecastRequest
from src.forecasting.series_builder import build_demand_series


@dataclass(frozen=True, slots=True)
class ForecastingServiceResult:
    """Represent the internal result of a forecast operation."""

    sku_id: str
    location_id: str | None
    model_name: str
    forecast_horizon: int
    generated_at: datetime
    metrics: dict[str, float | None]
    forecasts: pd.DataFrame
    selected_model: BaseForecaster
    model_artifact_id: str | None = None


def build_default_model_factories() -> dict[str, ForecasterFactory]:
    """Create the forecasting models available to the service."""
    arima_100 = ARIMAConfig(
        p=1,
        d=0,
        q=0,
        enforce_stationarity=False,
        enforce_invertibility=False,
    )

    arima_111 = ARIMAConfig(
        p=1,
        d=1,
        q=1,
        enforce_stationarity=False,
        enforce_invertibility=False,
    )

    return {
        "moving_average_3": partial(
            MovingAverageForecaster,
            window=3,
        ),
        "moving_average_7": partial(
            MovingAverageForecaster,
            window=7,
        ),
        arima_100.model_name: partial(
            ARIMAForecaster,
            config=arima_100,
        ),
        arima_111.model_name: partial(
            ARIMAForecaster,
            config=arima_111,
        ),
    }


class ForecastingService:
    """Coordinate data preparation, selection and forecasting."""

    def __init__(
        self,
        model_factories: (
            Mapping[
                str,
                ForecasterFactory,
            ]
            | None
        ) = None,
        model_store: ModelStore | None = None,
        primary_metric: str = "rmse",
        backtest_ratio: float = 0.25,
        frequency: str = "D",
    ) -> None:
        """
        Initialize the forecasting service.

        Args:
            model_factories: Models available for forecasting.
            primary_metric: Metric used for automatic selection.
            backtest_ratio: Historical proportion used for evaluation.
            frequency: Required demand-series frequency.
        """
        if isinstance(backtest_ratio, bool) or not isinstance(
            backtest_ratio,
            int | float,
        ):
            raise ModelInputValidationError("backtest_ratio must be numeric.")

        validated_ratio = float(backtest_ratio)

        if not 0 < validated_ratio < 1:
            raise ModelInputValidationError(
                "backtest_ratio must be between zero and one."
            )

        if not isinstance(frequency, str) or not frequency.strip():
            raise ModelInputValidationError("frequency must be non-empty text.")

        resolved_factories = (
            build_default_model_factories()
            if model_factories is None
            else dict(model_factories)
        )

        if not resolved_factories:
            raise ModelInputValidationError(
                "At least one forecasting model is required."
            )

        self._model_factories = resolved_factories
        self._primary_metric = primary_metric
        self._backtest_ratio = validated_ratio
        self._frequency = frequency.strip()
        self._model_store = model_store

    @property
    def available_models(self) -> tuple[str, ...]:
        """Return models available through the service."""
        return (
            "auto",
            *tuple(sorted(self._model_factories)),
        )

    def _resolve_candidate_factories(
        self,
        requested_model: str,
    ) -> dict[str, ForecasterFactory]:
        """Resolve automatic or explicitly requested candidates."""
        normalized_name = requested_model.strip().lower()

        if normalized_name == "auto":
            return dict(self._model_factories)

        if normalized_name not in self._model_factories:
            available = ", ".join(self.available_models)

            raise ModelInputValidationError(
                f"Unknown forecasting model: {requested_model}. "
                f"Available models: {available}."
            )

        return {normalized_name: self._model_factories[normalized_name]}

    @staticmethod
    def _minimum_model_history(
        factory: ForecasterFactory,
    ) -> int:
        """Return the minimum useful history for one candidate."""
        model = factory()

        if not isinstance(model, BaseForecaster):
            raise ModelInputValidationError(
                "Every model factory must return a BaseForecaster instance."
            )

        if isinstance(model, MovingAverageForecaster):
            return max(3, model.window)

        if isinstance(model, ARIMAForecaster):
            return max(
                3,
                model.config.minimum_observations,
            )

        return 3

    def _resolve_initial_train_size(
        self,
        series_length: int,
        candidates: Mapping[
            str,
            ForecasterFactory,
        ],
    ) -> int:
        """Calculate the first expanding training-window size."""
        candidate_minimums = [
            self._minimum_model_history(factory) for factory in candidates.values()
        ]

        smallest_candidate_minimum = min(candidate_minimums)

        evaluation_size = max(
            1,
            ceil(series_length * self._backtest_ratio),
        )

        suggested_training_size = series_length - evaluation_size

        resolved_size = max(
            3,
            smallest_candidate_minimum,
            suggested_training_size,
        )

        if resolved_size >= series_length:
            raise ModelInputValidationError(
                "The selected models require more historical "
                "observations before backtesting can begin."
            )

        return resolved_size

    @staticmethod
    def _resolve_location(
        series_data: pd.DataFrame,
        requested_location: str | None,
    ) -> str | None:
        """Resolve the location represented by the final series."""
        if requested_location is not None:
            return requested_location.strip()

        if "location_id" not in series_data.columns:
            return None

        locations = series_data["location_id"].dropna().astype(str).unique()

        if len(locations) == 1:
            return str(locations[0])

        return None

    def forecast(
        self,
        dataframe: pd.DataFrame,
        request: ForecastRequest,
        persist_model: bool = False,
    ) -> ForecastingServiceResult:
        """
        Generate a production-ready demand forecast.

        Historical optional variables are preserved by the data
        pipeline. Current models remain univariate unless future
        regressor values are supplied by a later scenario interface.

        Args:
            dataframe: Historical supply-chain observations.
            request: Validated forecasting request.

        Returns:
            Forecasting service result.
        """
        if not isinstance(request, ForecastRequest):
            raise ModelInputValidationError(
                "request must be a ForecastRequest instance."
            )

        candidate_factories = self._resolve_candidate_factories(request.model_name)

        series_data = build_demand_series(
            dataframe=dataframe,
            sku_id=request.sku_id,
            location_id=request.location_id,
            frequency=self._frequency,
        )

        demand_series = series_data["demand"].copy()
        demand_series.name = "demand"

        initial_train_size = self._resolve_initial_train_size(
            series_length=len(demand_series),
            candidates=candidate_factories,
        )

        selector = AutomaticModelSelector(
            model_factories=candidate_factories,
            primary_metric=self._primary_metric,
        )

        selection = selector.select(
            series=demand_series,
            initial_train_size=initial_train_size,
            confidence_level=request.confidence_level,
        )

        forecast = selection.selected_model.predict(
            horizon=request.forecast_horizon,
            confidence_level=request.confidence_level,
        )

        selected_backtest = selection.backtests[selection.selected_model_name]

        model_artifact_id: str | None = None

        if persist_model:
            if self._model_store is None:
                raise ModelInputValidationError(
                    "Model persistence was requested, but no ModelStore is configured."
                )

            artifact = self._model_store.save(
                model=selection.selected_model,
                sku_id=request.sku_id,
                location_id=self._resolve_location(
                    series_data,
                    request.location_id,
                ),
            )

            model_artifact_id = artifact.artifact_id

        return ForecastingServiceResult(
            sku_id=request.sku_id.strip(),
            location_id=self._resolve_location(
                series_data,
                request.location_id,
            ),
            model_name=selection.selected_model_name,
            forecast_horizon=request.forecast_horizon,
            generated_at=datetime.now(UTC),
            metrics=dict(selected_backtest.metrics),
            forecasts=forecast.copy(),
            selected_model=selection.selected_model,
            model_artifact_id=model_artifact_id,
        )
