"""Abstract interface shared by all forecasting models."""

from abc import ABC, abstractmethod

import pandas as pd


class BaseForecaster(ABC):
    """
    Define the contract implemented by every forecasting model.

    Moving Average, ARIMA and Prophet implementations must expose the
    same fit and predict operations so that the service layer can use
    them interchangeably.
    """

    @property
    @abstractmethod
    def model_name(self) -> str:
        """Return the unique model name."""

    @property
    @abstractmethod
    def is_fitted(self) -> bool:
        """Return whether the model has been trained."""

    @abstractmethod
    def fit(
        self,
        series: pd.Series,
        exogenous: pd.DataFrame | None = None,
    ) -> "BaseForecaster":
        """
        Train the model using historical demand.

        Args:
            series: Historical demand series.
            exogenous: Optional external forecasting variables.

        Returns:
            The fitted forecasting model.
        """

    @abstractmethod
    def predict(
        self,
        horizon: int,
        future_exogenous: pd.DataFrame | None = None,
        confidence_level: float = 0.95,
    ) -> pd.DataFrame:
        """
        Generate future demand forecasts.

        Args:
            horizon: Number of future periods to forecast.
            future_exogenous: Known external variables for future dates.
            confidence_level: Requested prediction confidence level.

        Returns:
            DataFrame containing predictions and confidence bounds.
        """
