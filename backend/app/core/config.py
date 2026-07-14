"""
Application Configuration

This module centralizes all configurable settings for the Supply Chain
Analytics platform. Configuration values are loaded from environment
variables using Pydantic Settings.

Author: Utsav J. Charkhawala
"""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    # --------------------------------------------------
    # Application
    # --------------------------------------------------

    APP_NAME: str = "Supply Chain Analytics"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "Demand Forecasting & Anomaly Detection Platform"

    ENVIRONMENT: str = Field(
        default="development",
        description="development | testing | production",
    )

    DEBUG: bool = True

    # --------------------------------------------------
    # API
    # --------------------------------------------------

    API_PREFIX: str = "/api/v1"

    # --------------------------------------------------
    # Server
    # --------------------------------------------------

    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # --------------------------------------------------
    # Database
    # --------------------------------------------------

    DATABASE_URL: str = "sqlite:///./supply_chain.db"

    # --------------------------------------------------
    # Forecasting
    # --------------------------------------------------

    FORECAST_DAYS: int = 90

    # --------------------------------------------------
    # Logging
    # --------------------------------------------------

    LOG_LEVEL: str = "INFO"

    # --------------------------------------------------
    # Dataset
    # --------------------------------------------------

    DATA_DIRECTORY: str = "data"

    # --------------------------------------------------
    # CORS
    # --------------------------------------------------

    ALLOWED_ORIGINS: list[str] = [
        "http://localhost:5173",
    ]

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """
    Returns a cached Settings object.

    Ensures configuration is loaded only once.
    """
    return Settings()


settings = get_settings()
