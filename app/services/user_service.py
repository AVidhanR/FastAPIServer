"""
User service for handling user-related business logic.
"""
from datetime import datetime
from typing import List, Optional
from fastapi import HTTPException, status

from app.models import User, UserCreate, UserUpdate, UserInDB, UserRole
from app.core.security import get_password_hash, verify_password


class UserService:
    """Service class for user operations."""
    
    def __init__(self):
        # In-memory storage for demo purposes
        # In production, this would be replaced with database operations
        self._users: List[UserInDB] = []
        self._next_id = 1
        
        # Create a default admin user
        self._create_default_users()
    
    def _create_default_users(self):
        """Create default users for demo."""
        admin_user = UserCreate(
            username="admin",
            email="admin@example.com",
            password="admin123",
            full_name="Administrator",
            role=UserRole.ADMIN
        )
        self.create_user(admin_user)
        
        regular_user = UserCreate(
            username="john_doe",
            email="john@example.com",
            password="user123",
            full_name="John Doe",
            role=UserRole.USER
        )
        self.create_user(regular_user)
    
    def create_user(self, user_create: UserCreate) -> User:
        """Create a new user."""
        # Check if username or email already exists
        if self.get_user_by_username(user_create.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )
        
        if self.get_user_by_email(user_create.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create user with hashed password
        hashed_password = get_password_hash(user_create.password)
        user_in_db = UserInDB(
            id=self._next_id,
            username=user_create.username,
            email=user_create.email,
            full_name=user_create.full_name,
            role=user_create.role,
            is_active=user_create.is_active,
            hashed_password=hashed_password,
            created_at=datetime.utcnow()
        )
        
        self._users.append(user_in_db)
        self._next_id += 1
        
        # Return user without password
        return User(**user_in_db.dict(exclude={"hashed_password"}))
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        for user in self._users:
            if user.id == user_id:
                return User(**user.dict(exclude={"hashed_password"}))
        return None
    
    def get_user_by_username(self, username: str) -> Optional[UserInDB]:
        """Get user by username (internal use with password)."""
        for user in self._users:
            if user.username == username:
                return user
        return None
    
    def get_user_by_email(self, email: str) -> Optional[UserInDB]:
        """Get user by email (internal use with password)."""
        for user in self._users:
            if user.email == email:
                return user
        return None
    
    def authenticate_user(self, username: str, password: str) -> Optional[UserInDB]:
        """Authenticate user with username and password."""
        user = self.get_user_by_username(username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
    
    def get_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all users with pagination."""
        users = self._users[skip:skip + limit]
        return [User(**user.dict(exclude={"hashed_password"})) for user in users]
    
    def update_user(self, user_id: int, user_update: UserUpdate) -> Optional[User]:
        """Update user information."""
        for i, user in enumerate(self._users):
            if user.id == user_id:
                update_data = user_update.dict(exclude_unset=True)
                update_data["updated_at"] = datetime.utcnow()
                
                # Update user
                updated_user = user.copy(update=update_data)
                self._users[i] = updated_user
                
                return User(**updated_user.dict(exclude={"hashed_password"}))
        return None
    
    def delete_user(self, user_id: int) -> bool:
        """Delete user by ID."""
        for i, user in enumerate(self._users):
            if user.id == user_id:
                del self._users[i]
                return True
        return False


# Global user service instance
user_service = UserService()
