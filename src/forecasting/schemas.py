"""Data schemas used by the demand forecasting module."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class DemandObservation(BaseModel):
    """Represent one historical demand observation."""

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    date: datetime
    sku_id: str = Field(min_length=1)
    demand: float = Field(ge=0)

    inventory_level: float | None = Field(default=None, ge=0)
    price: float | None = Field(default=None, ge=0)
    promotion: bool | None = None
    holiday: bool | None = None
    category: str | None = None
    location_id: str | None = None

    @field_validator("category", "location_id")
    @classmethod
    def convert_empty_strings_to_none(
        cls,
        value: str | None,
    ) -> str | None:
        """Convert optional empty text values to None."""
        if value is None:
            return None

        cleaned_value = value.strip()

        return cleaned_value or None


class ForecastRequest(BaseModel):
    """Represent a request to generate a demand forecast."""

    model_config = ConfigDict(extra="forbid")

    sku_id: str = Field(min_length=1)
    location_id: str | None = None
    forecast_horizon: int = Field(default=30, ge=1, le=365)
    model_name: str = Field(default="auto")
    confidence_level: float = Field(default=0.95, gt=0, lt=1)


class ForecastExecutionRequest(BaseModel):
    """Represent a complete API forecasting operation."""

    model_config = ConfigDict(extra="forbid")

    forecast: ForecastRequest
    observations: list[DemandObservation] = Field(min_length=4)
    persist_model: bool = False


class ForecastPoint(BaseModel):
    """Represent one predicted demand value."""

    forecast_date: datetime
    predicted_demand: float = Field(ge=0)
    lower_bound: float | None = Field(default=None, ge=0)
    upper_bound: float | None = Field(default=None, ge=0)


class ForecastMetrics(BaseModel):
    """Represent forecasting evaluation results."""

    mae: float
    mape: float | None
    mse: float
    rmse: float
    r2: float | None


class ForecastResponse(BaseModel):
    """Represent the complete result returned by a forecasting model."""

    sku_id: str
    location_id: str | None = None
    model_name: str
    forecast_horizon: int
    generated_at: datetime
    metrics: ForecastMetrics | None = None
    forecasts: list[ForecastPoint]
    model_artifact_id: str | None = None
