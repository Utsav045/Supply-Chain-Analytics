"""
Dashboard API Router

Provides aggregated KPI data for the Supply Chain Analytics dashboard.
"""

from pathlib import Path

import pandas as pd
from app.database.connection import get_db
from app.database.models import Anomaly, Forecast, Inventory, Product, Sales
from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

router = APIRouter()


DATA_FILE = (
    Path(__file__).resolve().parents[4]
    / "data"
    / "processed"
    / "clean_inventory_data.csv"
)


@router.get("/summary")
def get_dashboard_summary(db: Session = Depends(get_db)):
    """Return aggregated KPIs for the executive dashboard."""

    total_products = db.query(func.count(Product.id)).scalar() or 0

    total_sales_volume = (
        db.query(func.coalesce(func.sum(Sales.sales), 0)).scalar() or 0
    )

    total_revenue = (
        db.query(
            func.coalesce(
                func.sum(Sales.sales * Sales.price),
                0,
            )
        ).scalar()
        or 0
    )

    total_inventory = (
        db.query(func.coalesce(func.sum(Inventory.inventory), 0)).scalar() or 0
    )

    total_forecast = (
        db.query(func.coalesce(func.sum(Forecast.forecast_value), 0)).scalar()
        or 0
    )

    total_anomalies = (
        db.query(func.count(Anomaly.id))
        .filter(Anomaly.is_anomaly.is_(True))
        .scalar()
        or 0
    )

    high_severity_anomalies = (
        db.query(func.count(Anomaly.id))
        .filter(
            Anomaly.is_anomaly.is_(True),
            Anomaly.severity == "high",
        )
        .scalar()
        or 0
    )

    medium_severity_anomalies = (
        db.query(func.count(Anomaly.id))
        .filter(
            Anomaly.is_anomaly.is_(True),
            Anomaly.severity == "medium",
        )
        .scalar()
        or 0
    )

    low_severity_anomalies = (
        db.query(func.count(Anomaly.id))
        .filter(
            Anomaly.is_anomaly.is_(True),
            Anomaly.severity == "low",
        )
        .scalar()
        or 0
    )

    # ---------------------------------------------------------
    # Service Level
    # ---------------------------------------------------------
    service_level = 0.0

    if DATA_FILE.exists():
        inventory_df = pd.read_csv(DATA_FILE)

        required_columns = [
            "closing_stock",
            "reorder_level",
        ]

        if all(column in inventory_df.columns for column in required_columns):
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

    return {
        "total_products": total_products,
        "total_sales_volume": total_sales_volume,
        "total_revenue": total_revenue,
        "total_inventory": total_inventory,
        "total_forecast": total_forecast,
        "total_anomalies": total_anomalies,
        "service_level": service_level,
        "anomalies": {
            "high": high_severity_anomalies,
            "medium": medium_severity_anomalies,
            "low": low_severity_anomalies,
        },
    }