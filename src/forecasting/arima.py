"""ARIMA demand forecasting model."""

from dataclasses import dataclass, field
from typing import Any, cast

import numpy as np
import pandas as pd
from pandas.tseries.frequencies import to_offset
from statsmodels.tsa.arima.model import ARIMA

from src.forecasting.arima_config import ARIMAConfig
from src.forecasting.base import BaseForecaster
from src.forecasting.model_validation import (
    ModelInputValidationError,
    infer_series_frequency,
    validate_confidence_level,
    validate_demand_series,
    validate_exogenous_features,
    validate_forecast_horizon,
)


class ARIMAModelError(RuntimeError):
    """Raised when ARIMA fitting or forecasting fails."""


@dataclass(slots=True)
class ARIMAForecaster(BaseForecaster):
    """Forecast demand using a configurable ARIMA model."""

    config: ARIMAConfig = field(default_factory=ARIMAConfig)
    _history: pd.Series | None = field(
        default=None,
        init=False,
        repr=False,
    )
    _frequency: str | None = field(
        default=None,
        init=False,
        repr=False,
    )
    _result: Any | None = field(
        default=None,
        init=False,
        repr=False,
    )
    _exogenous_columns: tuple[str, ...] = field(
        default=(),
        init=False,
        repr=False,
    )

    def __post_init__(self) -> None:
        """Validate the supplied ARIMA configuration."""
        if not isinstance(self.config, ARIMAConfig):
            raise TypeError("config must be an ARIMAConfig instance.")

    @property
    def model_name(self) -> str:
        """Return the configured ARIMA model name."""
        return self.config.model_name

    @property
    def is_fitted(self) -> bool:
        """Return whether ARIMA training has completed."""
        return (
            self._history is not None
            and self._frequency is not None
            and self._result is not None
        )

    @property
    def uses_exogenous_features(self) -> bool:
        """Return whether training used external regressors."""
        return bool(self._exogenous_columns)

    @property
    def aic(self) -> float | None:
        """Return the fitted Akaike information criterion."""
        if self._result is None:
            return None

        return float(self._result.aic)

    @property
    def bic(self) -> float | None:
        """Return the fitted Bayesian information criterion."""
        if self._result is None:
            return None

        return float(self._result.bic)

    @property
    def converged(self) -> bool | None:
        """Return the optimizer convergence status when available."""
        if self._result is None:
            return None

        return bool(
            self._result.mle_retvals.get(
                "converged",
                True,
            )
        )

    def fit(
        self,
        series: pd.Series,
        exogenous: pd.DataFrame | None = None,
    ) -> "ARIMAForecaster":
        """
        Fit ARIMA using historical demand and optional regressors.

        Args:
            series: Historical demand series.
            exogenous: Optional aligned external variables.

        Returns:
            The fitted ARIMA forecaster.

        Raises:
            ARIMAModelError: If statsmodels cannot fit the model.
        """
        validated_series = validate_demand_series(
            series,
            minimum_observations=self.config.minimum_observations,
        )

        validated_index = cast(
            pd.DatetimeIndex,
            validated_series.index,
        )

        validated_exogenous: pd.DataFrame | None = None

        if exogenous is not None:
            validated_exogenous = validate_exogenous_features(
                exogenous,
                expected_index=validated_index,
            )

        trend: str | None = None

        if validated_exogenous is not None:
            exogenous_values = validated_exogenous.to_numpy(dtype=float)

            constant_columns = np.all(
                np.isclose(
                    exogenous_values,
                    exogenous_values[0],
                ),
                axis=0,
            )

            nonzero_columns = ~np.isclose(
                exogenous_values[0],
                0.0,
            )

            has_nonzero_constant_column = bool(
                np.any(constant_columns & nonzero_columns)
            )

            if has_nonzero_constant_column:
                trend = "n"

        try:
            model = ARIMA(
                endog=validated_series,
                exog=validated_exogenous,
                order=self.config.order,
                trend=trend,
                enforce_stationarity=(self.config.enforce_stationarity),
                enforce_invertibility=(self.config.enforce_invertibility),
                missing="raise",
            )

            result = model.fit()

        except (
            ValueError,
            TypeError,
            np.linalg.LinAlgError,
        ) as exc:
            raise ARIMAModelError(f"Unable to fit {self.model_name}: {exc}") from exc

        self._history = validated_series
        self._frequency = infer_series_frequency(validated_index)
        self._result = result

        if validated_exogenous is not None:
            self._exogenous_columns = tuple(
                str(column) for column in validated_exogenous.columns
            )
        else:
            self._exogenous_columns = ()

        return self

    def _prepare_future_exogenous(
        self,
        future_exogenous: pd.DataFrame | None,
        expected_index: pd.DatetimeIndex,
    ) -> pd.DataFrame | None:
        """Validate regressors supplied for future periods."""
        if self.uses_exogenous_features:
            if future_exogenous is None:
                raise ModelInputValidationError(
                    "Future exogenous features are required because "
                    "the ARIMA model was trained with regressors."
                )

            validated = validate_exogenous_features(
                future_exogenous,
                expected_index=expected_index,
            )

            missing_columns = set(self._exogenous_columns).difference(validated.columns)

            unexpected_columns = set(validated.columns).difference(
                self._exogenous_columns
            )

            if missing_columns or unexpected_columns:
                raise ModelInputValidationError(
                    "Future exogenous columns must match the "
                    "training exogenous columns."
                )

            return validated.loc[
                :,
                list(self._exogenous_columns),
            ]

        if future_exogenous is not None:
            raise ModelInputValidationError(
                "Future exogenous features were supplied, but the "
                "ARIMA model was trained without regressors."
            )

        return None

    def predict(
        self,
        horizon: int,
        future_exogenous: pd.DataFrame | None = None,
        confidence_level: float = 0.95,
    ) -> pd.DataFrame:
        """
        Generate ARIMA demand forecasts and confidence intervals.

        Args:
            horizon: Number of future observations to forecast.
            future_exogenous: External variables for future dates.
            confidence_level: Required interval confidence level.

        Returns:
            Forecast values with lower and upper confidence bounds.
        """
        if not self.is_fitted:
            raise RuntimeError("The ARIMA model must be fitted before prediction.")

        validated_horizon = validate_forecast_horizon(horizon)

        validated_confidence = validate_confidence_level(confidence_level)

        if self._history is None or self._frequency is None or self._result is None:
            raise RuntimeError("The fitted ARIMA model state is incomplete.")

        history_index = cast(
            pd.DatetimeIndex,
            self._history.index,
        )

        offset = to_offset(self._frequency)

        future_index = pd.date_range(
            start=history_index[-1] + offset,
            periods=validated_horizon,
            freq=offset,
        )

        validated_future_exogenous = self._prepare_future_exogenous(
            future_exogenous,
            expected_index=future_index,
        )

        try:
            prediction_result = self._result.get_forecast(
                steps=validated_horizon,
                exog=validated_future_exogenous,
            )

            summary = prediction_result.summary_frame(alpha=1 - validated_confidence)

        except (
            ValueError,
            TypeError,
            np.linalg.LinAlgError,
        ) as exc:
            raise ARIMAModelError(
                f"Unable to generate forecast from " f"{self.model_name}: {exc}"
            ) from exc

        required_columns = {
            "mean",
            "mean_ci_lower",
            "mean_ci_upper",
        }

        missing_columns = required_columns.difference(summary.columns)

        if missing_columns:
            raise ARIMAModelError("Statsmodels returned an incomplete forecast result.")

        predicted_values = pd.to_numeric(
            summary["mean"],
            errors="coerce",
        ).to_numpy(dtype=float)

        lower_values = pd.to_numeric(
            summary["mean_ci_lower"],
            errors="coerce",
        ).to_numpy(dtype=float)

        upper_values = pd.to_numeric(
            summary["mean_ci_upper"],
            errors="coerce",
        ).to_numpy(dtype=float)

        if not (
            np.isfinite(predicted_values).all()
            and np.isfinite(lower_values).all()
            and np.isfinite(upper_values).all()
        ):
            raise ARIMAModelError("ARIMA produced non-finite forecast values.")

        return pd.DataFrame(
            {
                "predicted_demand": np.maximum(
                    predicted_values,
                    0.0,
                ),
                "lower_bound": np.maximum(
                    lower_values,
                    0.0,
                ),
                "upper_bound": np.maximum(
                    upper_values,
                    0.0,
                ),
            },
            index=future_index,
        ).rename_axis("forecast_date")
