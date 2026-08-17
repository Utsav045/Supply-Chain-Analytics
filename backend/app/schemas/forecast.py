"""
Forecast Pydantic Schemas

Defines validation and serialization schemas for forecasting requests, responses,
and generation requests, ensuring alignment with application constants.

Author: Antigravity AI
"""

from datetime import date, datetime
from typing import List, Optional

from app.core.constants import DEFAULT_FORECAST_DAYS, SUPPORTED_FORECAST_MODELS
from pydantic import BaseModel, ConfigDict, Field, field_validator


class ForecastBase(BaseModel):
    """Base fields for a Forecast record."""

    product_id: str = Field(
        ..., description="Associated product identifier", min_length=1, max_length=50
    )
    date: date = Field(..., description="Date of the forecast")
    forecast_value: float = Field(..., description="Predicted demand value")
    lower_bound: Optional[float] = Field(
        None, description="Lower prediction interval bound"
    )
    upper_bound: Optional[float] = Field(
        None, description="Upper prediction interval bound"
    )
    model_name: str = Field(..., description="Name of the model used for forecasting")

    @field_validator("model_name")
    @classmethod
    def validate_model_name(cls, v: str) -> str:
        """Validates that the model name is supported."""
        if v not in SUPPORTED_FORECAST_MODELS:
            supported = ", ".join(SUPPORTED_FORECAST_MODELS)
            raise ValueError(
                f"Unsupported model name '{v}'. Supported models are: {supported}"
            )
        return v


class ForecastCreate(ForecastBase):
    """Schema for creating a Forecast record."""

    pass


class ForecastResponse(ForecastBase):
    """Schema for Forecast responses containing system fields."""

    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ForecastGenerationRequest(BaseModel):
    """Request schema for generating new forecasts."""

    product_ids: Optional[List[str]] = Field(
        None,
        description=(
            "List of product IDs to generate forecasts for. "
            "If null or empty, forecasts all products."
        ),
    )
    forecast_days: int = Field(
        default=DEFAULT_FORECAST_DAYS,
        ge=1,
        le=365,
        description="Forecasting horizon (number of days ahead)",
    )
    model_name: str = Field(
        default="arima",
        description=(
            "The algorithm to use for forecasting (moving_average, arima, prophet)"
        ),
    )

    @field_validator("model_name")
    @classmethod
    def validate_model_name(cls, v: str) -> str:
        """Validates that the model name is supported."""
        if v not in SUPPORTED_FORECAST_MODELS:
            supported = ", ".join(SUPPORTED_FORECAST_MODELS)
            raise ValueError(
                f"Unsupported model name '{v}'. Supported models are: {supported}"
            )
        return v


class ForecastSummaryMetric(BaseModel):
    """Metrics summary for model evaluation."""

    mape: Optional[float] = Field(None, description="Mean Absolute Percentage Error")
    rmse: Optional[float] = Field(None, description="Root Mean Squared Error")
    mae: Optional[float] = Field(None, description="Mean Absolute Error")


class ForecastModelPerformance(BaseModel):
    """Performance evaluation response for a product-model pair."""

    product_id: str
    model_name: str
    metrics: ForecastSummaryMetric
    training_time_seconds: float
    evaluated_at: datetime
