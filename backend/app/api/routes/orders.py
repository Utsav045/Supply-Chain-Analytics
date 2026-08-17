"""
Orders API Router

Exposes sales records as order records for the Supply Chain Analytics frontend.
"""

from app.database.connection import get_db
from app.database.models import Sales
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("")
def get_orders(db: Session = Depends(get_db)):
    """
    Return sales records as order records.
    """

    orders = db.query(Sales).order_by(Sales.date.desc(), Sales.id.desc()).all()

    return [
        {
            "id": order.id,
            "productId": order.product_id,
            "date": order.date,
            "quantity": order.sales,
            "price": order.price,
            "total": order.sales * order.price,
        }
        for order in orders
    ]
