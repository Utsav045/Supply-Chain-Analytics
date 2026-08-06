"""FastAPI application factory."""

from fastapi import FastAPI

from src.api.forecasting import router as forecasting_router


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    application = FastAPI(
        title="Supply Chain Analytics API",
        description=("Demand forecasting and anomaly detection platform."),
        version="0.1.0",
    )

    application.include_router(forecasting_router)

    @application.get(
        "/health",
        tags=["system"],
    )
    def health_check() -> dict[str, str]:
        """Return the application health status."""
        return {
            "status": "healthy",
        }

    return application


app = create_app()
