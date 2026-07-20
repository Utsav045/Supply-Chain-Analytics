"""
Health Check Route

Provides basic application status and checks database connection health.

Author: Antigravity AI
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from app.core.config import settings
from app.core.logger import logger
from app.database.connection import get_db

router = APIRouter()


@router.get("", status_code=status.HTTP_200_OK)
def health_check(db: Annotated[Session, Depends(get_db)]):
    """
    Check the health of the application and database.

    Returns 200 if database connection is successful,
    otherwise returns 503 Service Unavailable.
    """
    try:
        # Execute simple query to test DB connection
        db.execute(text("SELECT 1"))
        return {
            "status": "healthy",
            "database": "connected",
        }
    except Exception as e:
        logger.error(f"Database health check failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "status": "unhealthy",
                "database": "disconnected",
                "error": str(e) if settings.DEBUG else "Database connection failure",
            },
        ) from e
