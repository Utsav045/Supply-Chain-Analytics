"""
Forecast API Router

Exposes endpoints for generating demand forecasts.
"""

from pathlib import Path

import pandas as pd
from fastapi import APIRouter, HTTPException

from src.forecasting.schemas import ForecastRequest
from src.forecasting.response_mapper import build_forecast_response
from src.services.forecasting_service import ForecastingService

router = APIRouter()

PROJECT_ROOT = Path(__file__).resolve().parents[4]

SALES_FILE = PROJECT_ROOT / "data" / "processed" / "clean_sales_data.csv"


@router.post("")
def generate_forecast(request: ForecastRequest):
    """
    Generate a demand forecast for a product.

    The API maps the application's sales dataset into the
    forecasting engine's expected schema.
    """

    if not SALES_FILE.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Sales dataset not found: {SALES_FILE}",
        )

    try:
        sales_df = pd.read_csv(SALES_FILE)

        required_columns = [
            "date",
            "product_id",
            "warehouse",
            "units_sold",
            "unit_price",
            "promotion",
            "holiday",
            "category",
        ]

        missing_columns = [
            column
            for column in required_columns
            if column not in sales_df.columns
        ]

        if missing_columns:
            raise HTTPException(
                status_code=500,
                detail=f"Missing required sales columns: {missing_columns}",
            )

        # Map application dataset columns to forecasting-engine columns.
        forecasting_df = sales_df.rename(
            columns={
                "product_id": "sku_id",
                "units_sold": "demand",
                "warehouse": "location_id",
                "unit_price": "price",
            }
        ).copy()

        forecasting_df["date"] = pd.to_datetime(
            forecasting_df["date"],
            errors="coerce",
        )

        forecasting_df["demand"] = pd.to_numeric(
            forecasting_df["demand"],
            errors="coerce",
        )

        forecasting_df["price"] = pd.to_numeric(
            forecasting_df["price"],
            errors="coerce",
        )

        # Convert Yes/No dataset values to booleans.
        forecasting_df["promotion"] = (
            forecasting_df["promotion"]
            .astype(str)
            .str.strip()
            .str.lower()
            .eq("yes")
        )

        forecasting_df["holiday"] = (
            forecasting_df["holiday"]
            .astype(str)
            .str.strip()
            .str.lower()
            .eq("yes")
        )

        forecasting_df = forecasting_df.dropna(
            subset=[
                "date",
                "sku_id",
                "demand",
            ]
        )

        service = ForecastingService()

        result = service.forecast(
            dataframe=forecasting_df,
            request=request,
        )

        return build_forecast_response(result)

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate forecast: {str(exc)}",
        ) from exc