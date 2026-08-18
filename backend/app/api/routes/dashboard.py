"""
Dashboard API Router

Provides aggregated KPI data for the Supply Chain Analytics dashboard.
"""

from pathlib import Path

import pandas as pd
from app.database.connection import get_db
from app.database.models import Product, Sales
from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

router = APIRouter()


# ---------------------------------------------------------
# Project / Dataset Paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[4]

DATA_DIR = PROJECT_ROOT / "data" / "processed"

INVENTORY_FILE = DATA_DIR / "clean_inventory_data.csv"
ANOMALY_FILE = DATA_DIR / "zscore_anomalies.csv"


# ---------------------------------------------------------
# Dashboard Summary
# ---------------------------------------------------------

@router.get("/summary")
def get_dashboard_summary(
    db: Session = Depends(get_db),
):
    """
    Return aggregated KPIs for the executive dashboard.

    Forecasts are generated dynamically by the forecasting API
    and are not persisted in the database. Therefore this
    endpoint does not fabricate a forecast value.
    """

    # -----------------------------------------------------
    # Products
    # -----------------------------------------------------

    total_products = (
        db.query(func.count(Product.id)).scalar()
        or 0
    )

    # -----------------------------------------------------
    # Sales Volume
    # -----------------------------------------------------

    total_sales_volume = (
        db.query(
            func.coalesce(
                func.sum(Sales.sales),
                0,
            )
        ).scalar()
        or 0
    )

    # -----------------------------------------------------
    # Revenue
    # -----------------------------------------------------

    total_revenue = (
        db.query(
            func.coalesce(
                func.sum(Sales.sales * Sales.price),
                0,
            )
        ).scalar()
        or 0
    )

    # -----------------------------------------------------
    # Inventory
    # -----------------------------------------------------

    total_inventory = 0.0

    if INVENTORY_FILE.exists():
        inventory_df = pd.read_csv(INVENTORY_FILE)

        if "closing_stock" in inventory_df.columns:
            inventory_df["closing_stock"] = pd.to_numeric(
                inventory_df["closing_stock"],
                errors="coerce",
            )

            total_inventory = float(
                inventory_df["closing_stock"]
                .fillna(0)
                .sum()
            )

    # -----------------------------------------------------
    # Forecast
    # -----------------------------------------------------
    #
    # Forecasting is currently dynamic.
    #
    # The forecasting API:
    #     POST /api/v1/forecast
    #
    # generates forecasts on demand using ForecastingService.
    #
    # No forecast result is currently persisted for dashboard
    # aggregation.
    #
    # Therefore we MUST NOT use total_sales_volume here as a
    # fake forecast value.
    #

    total_forecast = 0.0

    # -----------------------------------------------------
    # Anomalies
    # -----------------------------------------------------

    total_anomalies = 0
    high_severity_anomalies = 0
    medium_severity_anomalies = 0
    low_severity_anomalies = 0

    if ANOMALY_FILE.exists():
        anomaly_df = pd.read_csv(ANOMALY_FILE)

        if "anomaly" in anomaly_df.columns:
            anomaly_df["anomaly"] = pd.to_numeric(
                anomaly_df["anomaly"],
                errors="coerce",
            ).fillna(0)

            detected = anomaly_df[
                anomaly_df["anomaly"] == 1
            ].copy()

            if "z_score" in detected.columns:
                detected["z_score"] = pd.to_numeric(
                    detected["z_score"],
                    errors="coerce",
                )

                absolute_z = detected["z_score"].abs()

                # High: |z| >= 5
                high_severity_anomalies = int(
                    (absolute_z >= 5).sum()
                )

                # Medium: 2 <= |z| < 5
                medium_severity_anomalies = int(
                    (
                        (absolute_z >= 2)
                        & (absolute_z < 5)
                    ).sum()
                )

                # Low: |z| < 2
                low_severity_anomalies = int(
                    (absolute_z < 2).sum()
                )

                total_anomalies = (
                    high_severity_anomalies
                    + medium_severity_anomalies
                    + low_severity_anomalies
                )

    # -----------------------------------------------------
    # Service Level
    # -----------------------------------------------------

    service_level = 0.0

    if INVENTORY_FILE.exists():
        inventory_df = pd.read_csv(INVENTORY_FILE)

        required_columns = [
            "closing_stock",
            "reorder_level",
        ]

        if all(
            column in inventory_df.columns
            for column in required_columns
        ):
            inventory_df["closing_stock"] = pd.to_numeric(
                inventory_df["closing_stock"],
                errors="coerce",
            )

            inventory_df["reorder_level"] = pd.to_numeric(
                inventory_df["reorder_level"],
                errors="coerce",
            )

            valid_inventory = inventory_df.dropna(
                subset=[
                    "closing_stock",
                    "reorder_level",
                ]
            )

            if not valid_inventory.empty:
                service_level = round(
                    (
                        valid_inventory["closing_stock"]
                        >= valid_inventory["reorder_level"]
                    ).mean()
                    * 100,
                    2,
                )

    # -----------------------------------------------------
    # Response
    # -----------------------------------------------------

    return {
        "total_products": total_products,
        "total_sales_volume": float(total_sales_volume),
        "total_revenue": float(total_revenue),
        "total_inventory": float(total_inventory),
        "total_forecast": total_forecast,
        "total_anomalies": total_anomalies,
        "service_level": service_level,
        "anomalies": {
            "high": high_severity_anomalies,
            "medium": medium_severity_anomalies,
            "low": low_severity_anomalies,
        },
    }