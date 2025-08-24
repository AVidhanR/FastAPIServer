"""
Product management API endpoints.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query

from app.models import Product, ProductCreate, ProductUpdate, ProductCategory, User, UserRole
from app.services.product_service import product_service
from app.api.auth import get_current_active_user

router = APIRouter()


async def get_admin_user(current_user: User = Depends(get_current_active_user)) -> User:
    """Dependency to ensure user has admin role."""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user


@router.get("/", response_model=List[Product])
async def get_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    category: Optional[ProductCategory] = None,
    in_stock: Optional[bool] = None
):
    """
    Get all products.
    
    Retrieve a list of products with optional filtering by category and stock status.
    Public endpoint - no authentication required.
    """
    return product_service.get_products(
        skip=skip, 
        limit=limit, 
        category=category, 
        in_stock=in_stock
    )


@router.get("/search", response_model=List[Product])
async def search_products(q: str = Query(..., min_length=1, description="Search query")):
    """
    Search products.
    
    Search for products by name or description.
    Public endpoint - no authentication required.
    """
    return product_service.search_products(q)


@router.get("/{product_id}", response_model=Product)
async def get_product(product_id: int):
    """
    Get product by ID.
    
    Retrieve a specific product by its ID.
    Public endpoint - no authentication required.
    """
    product = product_service.get_product_by_id(product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return product


@router.post("/", response_model=Product)
async def create_product(
    product_create: ProductCreate,
    current_user: User = Depends(get_admin_user)
):
    """
    Create a new product.
    
    Admin-only endpoint to create new products.
    """
    return product_service.create_product(product_create)


@router.put("/{product_id}", response_model=Product)
async def update_product(
    product_id: int,
    product_update: ProductUpdate,
    current_user: User = Depends(get_admin_user)
):
    """
    Update product information.
    
    Admin-only endpoint to update product details.
    """
    updated_product = product_service.update_product(product_id, product_update)
    if not updated_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return updated_product


@router.delete("/{product_id}")
async def delete_product(
    product_id: int,
    current_user: User = Depends(get_admin_user)
):
    """
    Delete product.
    
    Admin-only endpoint to delete products.
    """
    if not product_service.delete_product(product_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return {"message": "Product deleted successfully"}
