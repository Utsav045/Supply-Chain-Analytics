"""
Suppliers API Router

Exposes supplier records from the processed supplier dataset
for the Supply Chain Analytics frontend.
"""

from pathlib import Path

import pandas as pd
from fastapi import APIRouter, HTTPException

router = APIRouter()


DATA_FILE = (
    Path(__file__).resolve().parents[4]
    / "data"
    / "processed"
    / "clean_supplier_data.csv"
)


@router.get("")
def get_suppliers():
    """
    Return supplier records from the processed supplier dataset.
    """

    if not DATA_FILE.exists():
        raise HTTPException(
            status_code=404,
            detail="Supplier dataset not found.",
        )

    try:
        df = pd.read_csv(DATA_FILE)

        required_columns = [
            "supplier_id",
            "supplier_name",
            "product_id",
            "delivery_date",
            "expected_date",
            "delay_days",
            "supplier_rating",
            "transportation_cost",
        ]

        missing_columns = [
            column for column in required_columns if column not in df.columns
        ]

        if missing_columns:
            raise HTTPException(
                status_code=500,
                detail=f"Missing supplier columns: {missing_columns}",
            )

        df = df[required_columns].copy()

        df = df.fillna(
            {
                "supplier_id": "",
                "supplier_name": "",
                "product_id": "",
                "delivery_date": "",
                "expected_date": "",
                "delay_days": 0,
                "supplier_rating": 0,
                "transportation_cost": 0,
            }
        )

        return [
            {
                "supplierId": row["supplier_id"],
                "supplierName": row["supplier_name"],
                "productId": row["product_id"],
                "deliveryDate": str(row["delivery_date"]),
                "expectedDate": str(row["expected_date"]),
                "delayDays": float(row["delay_days"]),
                "supplierRating": float(row["supplier_rating"]),
                "transportationCost": float(row["transportation_cost"]),
            }
            for _, row in df.iterrows()
        ]

    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to load supplier data: {str(exc)}",
        ) from exc
