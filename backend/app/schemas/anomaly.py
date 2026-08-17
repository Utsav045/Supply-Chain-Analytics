"""
Anomaly Pydantic Schemas

Defines validation and serialization schemas for anomaly records and anomaly
detection requests, ensuring strict compliance with application constants.

Author: Antigravity AI
"""

import datetime
from typing import List, Optional

from app.core.constants import SUPPORTED_ANOMALY_METHODS
from pydantic import BaseModel, ConfigDict, Field, field_validator


class AnomalyBase(BaseModel):
    """Base fields for an Anomaly record."""

    product_id: str = Field(
        ..., description="Associated product identifier", min_length=1, max_length=50
    )

    date: datetime.date = Field(..., description="Date of the anomaly record")

    metric_name: str = Field(
        ...,
        description="Target metric (e.g., sales, inventory)",
        min_length=1,
        max_length=50,
    )

    metric_value: float = Field(..., description="Observed metric value")

    is_anomaly: bool = Field(
        default=True,
        description="True if this data point is flagged as an anomaly",
    )

    severity: str = Field(
        ...,
        description="Severity of anomaly (low, medium, high)",
    )

    method: str = Field(
        ...,
        description="Detection method used",
    )

    description: Optional[str] = Field(
        None,
        description="Detailed explanation/context of the anomaly",
        max_length=500,
    )

    @field_validator("method")
    @classmethod
    def validate_method(cls, v: str) -> str:
        """Validates that the detection method is supported."""
        if v not in SUPPORTED_ANOMALY_METHODS:
            supported = ", ".join(SUPPORTED_ANOMALY_METHODS)
            raise ValueError(
                f"Unsupported anomaly detection method '{v}'. "
                f"Supported methods are: {supported}"
            )
        return v

    @field_validator("severity")
    @classmethod
    def validate_severity(cls, v: str) -> str:
        """Validates that the severity is low, medium, high, or critical."""
        valid_severities = {"low", "medium", "high", "critical"}
        if v.lower() not in valid_severities:
            allowed = ", ".join(sorted(valid_severities))
            raise ValueError(f"Invalid severity level '{v}'. Allowed levels: {allowed}")
        return v.lower()


class AnomalyCreate(AnomalyBase):
    """Schema for creating an Anomaly record."""

    pass


class AnomalyResponse(AnomalyBase):
    """Schema for Anomaly responses containing database ID."""

    id: int
    created_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)


class AnomalyDetectionRequest(BaseModel):
    """Request schema to trigger anomaly detection."""

    product_ids: Optional[List[str]] = Field(
        None,
        description=(
            "List of product IDs to execute detection on. "
            "If null or empty, processes all products."
        ),
    )

    method: str = Field(
        default="z_score",
        description=(
            "The method to use for detecting anomalies (z_score, iqr, isolation_forest)"
        ),
    )

    threshold: float = Field(
        default=3.0,
        gt=0.0,
        description="Z-score threshold or multiplier for IQR",
    )

    contamination: float = Field(
        default=0.05,
        gt=0.0,
        lt=0.5,
        description=(
            "Contamination rate representing proportion of "
            "expected anomalies (used in isolation_forest)"
        ),
    )

    @field_validator("method")
    @classmethod
    def validate_method(cls, v: str) -> str:
        """Validates that the detection method is supported."""
        if v not in SUPPORTED_ANOMALY_METHODS:
            supported = ", ".join(SUPPORTED_ANOMALY_METHODS)
            raise ValueError(
                f"Unsupported anomaly detection method '{v}'. "
                f"Supported methods are: {supported}"
            )
        return v
