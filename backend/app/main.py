"""
FastAPI Application Entrypoint

Initializes the FastAPI application, registers middle-wares (like CORS),
handles database table generation via a lifespan context manager, and routes endpoints.

Author: Antigravity AI
"""

from contextlib import asynccontextmanager

from app.api.router import api_router
from app.core.config import settings
from app.core.logger import logger
from app.database.connection import Base, engine
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager that handles startup and shutdown operations.
    Enforces automatic DB table creation on application startup.
    """
    logger.info("Starting up Supply Chain Analytics API...")
    logger.info("Initializing database schema...")
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database schema initialized successfully.")
    except Exception as e:
        logger.critical(f"Critical failure initializing database schema: {str(e)}")
        raise e

    yield

    logger.info("Shutting down Supply Chain Analytics API...")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION,
    lifespan=lifespan,
    debug=settings.DEBUG,
)

# Configure CORS Middleware
if settings.ALLOWED_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.ALLOWED_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Include main API router
app.include_router(api_router, prefix=settings.API_PREFIX)


@app.get("/", tags=["Root"])
def root():
    """
    Root endpoint returning basic platform details.
    """
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "description": settings.APP_DESCRIPTION,
        "status": "online",
        "docs_url": "/docs",
    }
