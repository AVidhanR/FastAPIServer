"""
User management API endpoints.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query

from app.models import User, UserCreate, UserUpdate, UserRole
from app.services.user_service import user_service
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


@router.get("/", response_model=List[User])
async def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get all users.
    
    Retrieve a list of all users with pagination.
    Only accessible by authenticated users.
    """
    return user_service.get_users(skip=skip, limit=limit)


@router.get("/{user_id}", response_model=User)
async def get_user(
    user_id: int,
    current_user: User = Depends(get_current_active_user)
):
    """
    Get user by ID.
    
    Retrieve a specific user by their ID.
    """
    user = user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.post("/", response_model=User)
async def create_user(
    user_create: UserCreate,
    current_user: User = Depends(get_admin_user)
):
    """
    Create a new user.
    
    Admin-only endpoint to create new users.
    """
    return user_service.create_user(user_create)


@router.put("/{user_id}", response_model=User)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user)
):
    """
    Update user information.
    
    Users can update their own information, admins can update any user.
    """
    # Users can only update themselves unless they're admin
    if current_user.id != user_id and current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    updated_user = user_service.update_user(user_id, user_update)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return updated_user


@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    current_user: User = Depends(get_admin_user)
):
    """
    Delete user.
    
    Admin-only endpoint to delete users.
    """
    if not user_service.delete_user(user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return {"message": "User deleted successfully"}
