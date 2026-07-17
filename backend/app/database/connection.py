"""
Database Connection and Session Management

This module configures the SQLAlchemy engine, sessionmaker, and provides
a database session dependency for the FastAPI application.

Author: Antigravity AI
"""

from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from app.core.config import settings

DATABASE_URL = settings.DATABASE_URL

# For SQLite, enable multi-threaded access (useful for development/testing)
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False

# Create the SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    echo=False,  # Set to True for SQL query debugging
)

# Create a configured "Session" class
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Create a Declarative Base for models
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    Dependency generator that yields a database session.
    Ensures that the session is closed after the request is completed.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
