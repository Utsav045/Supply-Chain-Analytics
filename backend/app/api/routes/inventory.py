"""
Inventory API Router

Exposes the latest inventory status for each product.
"""

from pathlib import Path

import pandas as pd
from app.database.connection import get_db
from app.database.models import Product
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter()


DATA_FILE = (
    Path(__file__).resolve().parents[4]
    / "data"
    / "processed"
    / "clean_inventory_data.csv"
)

SUPPLIER_FILE = (
    Path(__file__).resolve().parents[4]
    / "data"
    / "processed"
    / "clean_supplier_data.csv"
)


@router.get("")
def get_inventory(db: Session = Depends(get_db)):
    """
    Return the latest inventory record for each product.
    """

    if not DATA_FILE.exists():
        raise HTTPException(
            status_code=404,
            detail="Inventory dataset not found.",
        )

    if not SUPPLIER_FILE.exists():
        raise HTTPException(
            status_code=404,
            detail="Supplier dataset not found.",
        )

    try:
        inventory_df = pd.read_csv(DATA_FILE)
        supplier_df = pd.read_csv(SUPPLIER_FILE)

        required_inventory_columns = [
            "date",
            "product_id",
            "closing_stock",
            "reorder_level",
        ]

        missing_inventory = [
            column
            for column in required_inventory_columns
            if column not in inventory_df.columns
        ]

        if missing_inventory:
            raise HTTPException(
                status_code=500,
                detail=f"Missing inventory columns: {missing_inventory}",
            )

        required_supplier_columns = [
            "product_id",
            "supplier_name",
        ]

        missing_supplier = [
            column
            for column in required_supplier_columns
            if column not in supplier_df.columns
        ]

        if missing_supplier:
            raise HTTPException(
                status_code=500,
                detail=f"Missing supplier columns: {missing_supplier}",
            )

        inventory_df["date"] = pd.to_datetime(
            inventory_df["date"],
            errors="coerce",
        )

        inventory_df["closing_stock"] = pd.to_numeric(
            inventory_df["closing_stock"],
            errors="coerce",
        )

        inventory_df["reorder_level"] = pd.to_numeric(
            inventory_df["reorder_level"],
            errors="coerce",
        )

        inventory_df = inventory_df.dropna(
            subset=[
                "date",
                "product_id",
                "closing_stock",
                "reorder_level",
            ]
        )

        inventory_df = inventory_df.sort_values("date").drop_duplicates(
            subset=["product_id"],
            keep="last",
        )

        supplier_df = supplier_df[["product_id", "supplier_name"]].drop_duplicates(
            subset=["product_id"],
            keep="last",
        )

        inventory_df = inventory_df.merge(
            supplier_df,
            on="product_id",
            how="left",
        )

        products = db.query(Product).all()

        product_map = {product.product_id: product for product in products}

        result = []

        for _, row in inventory_df.iterrows():
            product_id = str(row["product_id"])
            stock = float(row["closing_stock"])
            reorder_level = float(row["reorder_level"])

            product = product_map.get(product_id)

            if stock <= 0:
                status = "Out of Stock"
            elif stock <= reorder_level:
                status = "Low Stock"
            else:
                status = "In Stock"

            result.append(
                {
                    "id": product_id,
                    "productName": (product.product_name if product else product_id),
                    "category": (product.category if product else "Unknown"),
                    "supplier": (
                        str(row["supplier_name"])
                        if pd.notna(row["supplier_name"])
                        else "Unknown"
                    ),
                    "stock": stock,
                    "reorderLevel": reorder_level,
                    "status": status,
                }
            )

        return result

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to load inventory data: {str(exc)}",
        ) from exc
