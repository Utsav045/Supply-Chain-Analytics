"""
Common Pydantic Schemas

Defines core/base Pydantic schemas for models shared across the application,
such as Product, Sales, and Inventory, ensuring Pydantic v2 compliance.

Author: Antigravity AI
"""

from datetime import date, datetime
from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")


class ProductBase(BaseModel):
    """Base fields for a Product."""

    product_id: str = Field(
        ...,
        description="Unique product code/identifier (e.g., PROD-001)",
        min_length=1,
        max_length=50,
    )
    product_name: str = Field(
        ..., description="Name of the product", min_length=1, max_length=255
    )
    category: str = Field(
        ...,
        description="Product category (e.g., Electronics)",
        min_length=1,
        max_length=100,
    )
    price: float = Field(..., description="Unit price of the product", gt=0.0)


class ProductCreate(ProductBase):
    """Schema for creating a Product."""

    pass


class ProductUpdate(BaseModel):
    """Schema for updating a Product (all fields optional)."""

    product_name: Optional[str] = Field(None, min_length=1, max_length=255)
    category: Optional[str] = Field(None, min_length=1, max_length=100)
    price: Optional[float] = Field(None, gt=0.0)


class ProductResponse(ProductBase):
    """Schema for Product responses containing system generated fields."""

    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SalesBase(BaseModel):
    """Base fields for Sales data."""

    product_id: str = Field(
        ..., description="Associated product identifier", min_length=1, max_length=50
    )
    date: date = Field(..., description="Date of the sales record")
    sales: float = Field(..., description="Quantity/volume of sales", ge=0.0)
    price: float = Field(..., description="Price at which product was sold", gt=0.0)


class SalesCreate(SalesBase):
    """Schema for creating a Sales record."""

    pass


class SalesResponse(SalesBase):
    """Schema for Sales responses containing database ID."""

    id: int

    model_config = ConfigDict(from_attributes=True)


class InventoryBase(BaseModel):
    """Base fields for Inventory records."""

    product_id: str = Field(
        ..., description="Associated product identifier", min_length=1, max_length=50
    )
    date: date = Field(..., description="Date of the inventory record")
    inventory: float = Field(..., description="Current stock level", ge=0.0)


class InventoryCreate(InventoryBase):
    """Schema for creating an Inventory record."""

    pass


class InventoryResponse(InventoryBase):
    """Schema for Inventory responses containing database ID."""

    id: int

    model_config = ConfigDict(from_attributes=True)


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic response wrapper for paginated endpoints."""

    items: List[T]
    total: int
    page: int
    size: int
    pages: int


class MessageResponse(BaseModel):
    """Standard message response."""

    message: str
    status: str = Field(default="success")
