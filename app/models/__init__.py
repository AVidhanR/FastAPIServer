"""
Pydantic models for the application.
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, field_validator
from enum import Enum


class UserRole(str, Enum):
    """User roles enumeration."""
    ADMIN = "admin"
    USER = "user"
    MODERATOR = "moderator"


class UserBase(BaseModel):
    """Base user model."""
    username: str
    email: str
    full_name: Optional[str] = None
    role: UserRole = UserRole.USER
    is_active: bool = True


class UserCreate(UserBase):
    """User creation model."""
    password: str
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters long')
        return v


class UserUpdate(BaseModel):
    """User update model."""
    email: Optional[str] = None
    full_name: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None


class User(UserBase):
    """User response model."""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserInDB(User):
    """User model with hashed password (for internal use)."""
    hashed_password: str


# Product models
class ProductCategory(str, Enum):
    """Product categories."""
    ELECTRONICS = "electronics"
    CLOTHING = "clothing"
    BOOKS = "books"
    HOME = "home"
    SPORTS = "sports"


class ProductBase(BaseModel):
    """Base product model."""
    name: str
    description: Optional[str] = None
    price: float
    category: ProductCategory
    in_stock: bool = True
    stock_quantity: int = 0
    
    @field_validator('price')
    @classmethod
    def validate_price(cls, v):
        if v < 0:
            raise ValueError('Price must be positive')
        return v


class ProductCreate(ProductBase):
    """Product creation model."""
    pass


class ProductUpdate(BaseModel):
    """Product update model."""
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[ProductCategory] = None
    in_stock: Optional[bool] = None
    stock_quantity: Optional[int] = None


class Product(ProductBase):
    """Product response model."""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Order models
class OrderStatus(str, Enum):
    """Order status enumeration."""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class OrderItem(BaseModel):
    """Order item model."""
    product_id: int
    quantity: int
    price: float


class OrderCreate(BaseModel):
    """Order creation model."""
    items: List[OrderItem]
    shipping_address: str
    notes: Optional[str] = None


class Order(BaseModel):
    """Order response model."""
    id: int
    user_id: int
    items: List[OrderItem]
    total_amount: float
    status: OrderStatus
    shipping_address: str
    notes: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Generic response models
class MessageResponse(BaseModel):
    """Generic message response."""
    message: str
    success: bool = True


class PaginatedResponse(BaseModel):
    """Paginated response model."""
    items: List[dict]
    total: int
    page: int
    size: int
    pages: int


# File upload models
class FileInfo(BaseModel):
    """File information model."""
    filename: str
    content_type: str
    size: int
    uploaded_at: datetime


class UploadResponse(BaseModel):
    """File upload response."""
    message: str
    file_info: FileInfo
    file_url: Optional[str] = None
