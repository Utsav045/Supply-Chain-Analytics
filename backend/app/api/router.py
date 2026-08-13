"""
API Router Registration

Aggregates and registers all individual API route modules.
"""

from fastapi import APIRouter

from app.api.routes import (
    anomaly,
    dashboard,
    forecast,
    health,
    inventory,
    orders,
    reports,
    suppliers,
)

api_router = APIRouter()


api_router.include_router(
    health.router,
    prefix="/health",
    tags=["Health"],
)

api_router.include_router(
    forecast.router,
    prefix="/forecast",
    tags=["Forecasting"],
)

api_router.include_router(
    anomaly.router,
    prefix="/anomaly",
    tags=["Anomaly Detection"],
)

api_router.include_router(
    dashboard.router,
    prefix="/dashboard",
    tags=["Dashboard"],
)

api_router.include_router(
    orders.router,
    prefix="/orders",
    tags=["Orders"],
)

api_router.include_router(
    suppliers.router,
    prefix="/suppliers",
    tags=["Suppliers"],
)

api_router.include_router(
    inventory.router,
    prefix="/inventory",
    tags=["Inventory"],
)

api_router.include_router(
    reports.router,
    prefix="/reports",
    tags=["Reports"],
)
