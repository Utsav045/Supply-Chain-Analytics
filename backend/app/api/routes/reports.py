"""
Reports API Router

Provides summary metrics for the Reports page.
"""

from pathlib import Path

import pandas as pd
from fastapi import APIRouter, HTTPException

router = APIRouter()


# --------------------------------------------------
# Project paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[4]

SALES_FILE = PROJECT_ROOT / "data" / "processed" / "clean_sales_data.csv"

SUPPLIER_FILE = PROJECT_ROOT / "data" / "processed" / "clean_supplier_data.csv"


# --------------------------------------------------
# Reports endpoint
# --------------------------------------------------


@router.get("")
def get_reports():
    """Return summary metrics for the Reports page."""

    # --------------------------------------------------
    # Check datasets
    # --------------------------------------------------

    if not SALES_FILE.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Sales dataset not found: {SALES_FILE}",
        )

    if not SUPPLIER_FILE.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Supplier dataset not found: {SUPPLIER_FILE}",
        )

    try:
        # --------------------------------------------------
        # Load datasets
        # --------------------------------------------------

        sales_df = pd.read_csv(SALES_FILE)
        supplier_df = pd.read_csv(SUPPLIER_FILE)

        # --------------------------------------------------
        # Validate sales columns
        # --------------------------------------------------

        required_columns = [
            "order_id",
            "product_id",
            "product_name",
            "units_sold",
            "revenue",
        ]

        missing_columns = [
            column for column in required_columns if column not in sales_df.columns
        ]

        if missing_columns:
            raise HTTPException(
                status_code=500,
                detail=(
                    "Missing required columns in sales dataset: " f"{missing_columns}"
                ),
            )

        # --------------------------------------------------
        # Convert numeric columns
        # --------------------------------------------------

        sales_df["units_sold"] = pd.to_numeric(
            sales_df["units_sold"],
            errors="coerce",
        )

        sales_df["revenue"] = pd.to_numeric(
            sales_df["revenue"],
            errors="coerce",
        )

        # --------------------------------------------------
        # Remove invalid rows
        # --------------------------------------------------

        sales_df = sales_df.dropna(
            subset=[
                "order_id",
                "product_id",
                "product_name",
                "units_sold",
                "revenue",
            ]
        )

        # --------------------------------------------------
        # KPI calculations
        # --------------------------------------------------

        total_orders = int(sales_df["order_id"].nunique())

        total_quantity = int(sales_df["units_sold"].sum())

        total_revenue = float(sales_df["revenue"].sum())

        # --------------------------------------------------
        # Top products by revenue
        # --------------------------------------------------

        product_sales = sales_df.groupby(
            ["product_id", "product_name"],
            as_index=False,
        )["revenue"].sum()

        # Convert grouped data to plain Python records.
        # This avoids Pandas/Pylance sorting type issues.
        product_records = []

        for _, row in product_sales.iterrows():
            product_records.append(
                {
                    "productId": str(row["product_id"]),
                    "productName": str(row["product_name"]),
                    "revenue": float(row["revenue"]),
                }
            )

        # Sort using normal Python.
        product_records.sort(
            key=lambda item: item["revenue"],
            reverse=True,
        )

        # Keep only top 10 products.
        top_products = [
            {
                "productId": product["productId"],
                "productName": product["productName"],
                "revenue": round(
                    product["revenue"],
                    2,
                ),
            }
            for product in product_records[:10]
        ]

        # --------------------------------------------------
        # Supplier count
        # --------------------------------------------------

        supplier_count = 0

        if "supplier_id" in supplier_df.columns:
            supplier_count = int(supplier_df["supplier_id"].dropna().nunique())

        elif "supplier_name" in supplier_df.columns:
            supplier_count = int(supplier_df["supplier_name"].dropna().nunique())

        # --------------------------------------------------
        # API response
        # --------------------------------------------------

        return {
            "totalOrders": total_orders,
            "totalQuantity": total_quantity,
            "totalRevenue": round(
                total_revenue,
                2,
            ),
            "supplierCount": supplier_count,
            "topProducts": top_products,
        }

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate reports: {str(exc)}",
        ) from exc
