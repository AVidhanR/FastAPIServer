"""
Product service for handling product-related business logic.
"""
from datetime import datetime
from typing import List, Optional
from fastapi import HTTPException, status

from app.models import Product, ProductCreate, ProductUpdate, ProductCategory


class ProductService:
    """Service class for product operations."""
    
    def __init__(self):
        # In-memory storage for demo purposes
        self._products: List[Product] = []
        self._next_id = 1
        
        # Create some sample products
        self._create_sample_products()
    
    def _create_sample_products(self):
        """Create sample products for demo."""
        sample_products = [
            ProductCreate(
                name="MacBook Pro",
                description="Apple MacBook Pro 16-inch with M2 chip",
                price=2499.99,
                category=ProductCategory.ELECTRONICS,
                stock_quantity=10
            ),
            ProductCreate(
                name="Nike Air Max",
                description="Comfortable running shoes",
                price=120.00,
                category=ProductCategory.SPORTS,
                stock_quantity=25
            ),
            ProductCreate(
                name="Python Programming Book",
                description="Learn Python programming from scratch",
                price=29.99,
                category=ProductCategory.BOOKS,
                stock_quantity=50
            ),
        ]
        
        for product_create in sample_products:
            self.create_product(product_create)
    
    def create_product(self, product_create: ProductCreate) -> Product:
        """Create a new product."""
        product = Product(
            id=self._next_id,
            **product_create.dict(),
            created_at=datetime.utcnow()
        )
        
        self._products.append(product)
        self._next_id += 1
        
        return product
    
    def get_product_by_id(self, product_id: int) -> Optional[Product]:
        """Get product by ID."""
        for product in self._products:
            if product.id == product_id:
                return product
        return None
    
    def get_products(
        self, 
        skip: int = 0, 
        limit: int = 100,
        category: Optional[ProductCategory] = None,
        in_stock: Optional[bool] = None
    ) -> List[Product]:
        """Get products with optional filtering."""
        products = self._products
        
        # Apply filters
        if category:
            products = [p for p in products if p.category == category]
        
        if in_stock is not None:
            products = [p for p in products if p.in_stock == in_stock]
        
        # Apply pagination
        return products[skip:skip + limit]
    
    def update_product(self, product_id: int, product_update: ProductUpdate) -> Optional[Product]:
        """Update product information."""
        for i, product in enumerate(self._products):
            if product.id == product_id:
                update_data = product_update.dict(exclude_unset=True)
                update_data["updated_at"] = datetime.utcnow()
                
                # Update product
                updated_product = product.copy(update=update_data)
                self._products[i] = updated_product
                
                return updated_product
        return None
    
    def delete_product(self, product_id: int) -> bool:
        """Delete product by ID."""
        for i, product in enumerate(self._products):
            if product.id == product_id:
                del self._products[i]
                return True
        return False
    
    def search_products(self, query: str) -> List[Product]:
        """Search products by name or description."""
        query = query.lower()
        return [
            product for product in self._products
            if query in product.name.lower() or 
               (product.description and query in product.description.lower())
        ]


# Global product service instance
product_service = ProductService()
