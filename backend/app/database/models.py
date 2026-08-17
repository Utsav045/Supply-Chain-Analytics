"""
Database Models

This module defines the SQLAlchemy ORM models for the Supply Chain Analytics platform.
Models include Products, Sales, Inventory, Forecasts, and Anomalies.

Author: Antigravity AI
"""

from app.database.connection import Base
from sqlalchemy import (Boolean, Column, Date, DateTime, Float, ForeignKey,
                        Integer, String, func)
from sqlalchemy.orm import relationship


class Product(Base):
    """
    Product Model

    Represents a product in the supply chain catalog.
    """

    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(String(50), unique=True, index=True, nullable=False)
    product_name = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relationships
    sales = relationship(
        "Sales",
        back_populates="product",
        cascade="all, delete-orphan",
    )
    inventory = relationship(
        "Inventory",
        back_populates="product",
        cascade="all, delete-orphan",
    )
    forecasts = relationship(
        "Forecast",
        back_populates="product",
        cascade="all, delete-orphan",
    )
    anomalies = relationship(
        "Anomaly",
        back_populates="product",
        cascade="all, delete-orphan",
    )


class Sales(Base):
    """
    Sales Model

    Represents daily sales records for a product.
    """

    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(
        String(50),
        ForeignKey("products.product_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    date = Column(Date, nullable=False, index=True)
    sales = Column(Float, nullable=False)  # Sales volume/quantity
    price = Column(Float, nullable=False)  # Unit price at the time of sale

    # Relationships
    product = relationship("Product", back_populates="sales")


class Inventory(Base):
    """
    Inventory Model

    Represents daily inventory levels for a product.
    """

    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(
        String(50),
        ForeignKey("products.product_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    date = Column(Date, nullable=False, index=True)
    inventory = Column(Float, nullable=False)  # Current stock level

    # Relationships
    product = relationship("Product", back_populates="inventory")


class Forecast(Base):
    """
    Forecast Model

    Stores generated demand forecasts for products.
    """

    __tablename__ = "forecasts"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(
        String(50),
        ForeignKey("products.product_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    date = Column(Date, nullable=False, index=True)
    forecast_value = Column(Float, nullable=False)
    lower_bound = Column(Float, nullable=True)  # Lower confidence interval
    upper_bound = Column(Float, nullable=True)  # Upper confidence interval
    model_name = Column(String(50), nullable=False)  # e.g., 'arima', 'prophet'
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    # Relationships
    product = relationship("Product", back_populates="forecasts")


class Anomaly(Base):
    """
    Anomaly Model

    Stores detected operational anomalies in sales or inventory.
    """

    __tablename__ = "anomalies"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(
        String(50),
        ForeignKey("products.product_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    date = Column(Date, nullable=False, index=True)
    metric_name = Column(String(50), nullable=False)  # e.g., 'sales', 'inventory'
    metric_value = Column(Float, nullable=False)  # Observed value
    is_anomaly = Column(Boolean, default=True, nullable=False)
    severity = Column(String(20), nullable=False)  # e.g., 'low', 'medium', 'high'
    method = Column(String(50), nullable=False)  # e.g., 'z_score', 'isolation_forest'
    description = Column(String(500), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    # Relationships
    product = relationship("Product", back_populates="anomalies")
