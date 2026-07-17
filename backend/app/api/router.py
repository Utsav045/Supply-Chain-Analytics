"""
API Router Registration

Aggregates and registers all individual API route modules.

Author: Antigravity AI
"""

from fastapi import APIRouter

from app.api.routes import anomaly, dashboard, forecast, health

api_router = APIRouter()

# Register sub-routers with appropriate prefixes and tags
api_router.include_router(health.router, prefix="/health", tags=["Health"])
api_router.include_router(forecast.router, prefix="/forecast", tags=["Forecasting"])
api_router.include_router(anomaly.router, prefix="/anomaly", tags=["Anomaly Detection"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
