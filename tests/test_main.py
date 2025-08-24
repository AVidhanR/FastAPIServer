"""
Basic tests for the FastAPI application.
"""
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestBasicEndpoints:
    """Test basic endpoints that don't require authentication."""
    
    def test_root_endpoint(self):
        """Test the root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
    
    def test_api_info(self):
        """Test the API info endpoint."""
        response = client.get("/api/v1")
        assert response.status_code == 200
        data = response.json()
        assert "endpoints" in data
        assert "documentation" in data
    
    def test_health_check(self):
        """Test the health check endpoint."""
        response = client.get("/api/v1/misc/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
    
    def test_ping(self):
        """Test the ping endpoint."""
        response = client.get("/api/v1/misc/ping")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "pong"
    
    def test_echo_get(self):
        """Test the echo GET endpoint."""
        message = "Hello World"
        response = client.get(f"/api/v1/misc/echo?message={message}")
        assert response.status_code == 200
        data = response.json()
        assert data["original_message"] == message
    
    def test_products_list(self):
        """Test getting list of products."""
        response = client.get("/api/v1/products/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0  # Should have sample products
    
    def test_product_search(self):
        """Test product search."""
        response = client.get("/api/v1/products/search?q=macbook")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


class TestAuthentication:
    """Test authentication endpoints."""
    
    def test_login_success(self):
        """Test successful login."""
        response = client.post(
            "/api/v1/auth/token",
            data={"username": "admin", "password": "admin123"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    def test_login_invalid_credentials(self):
        """Test login with invalid credentials."""
        response = client.post(
            "/api/v1/auth/token",
            data={"username": "invalid", "password": "invalid"}
        )
        assert response.status_code == 401
    
    def test_register_user(self):
        """Test user registration."""
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123",
            "full_name": "Test User"
        }
        response = client.post("/api/v1/auth/register", json=user_data)
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == user_data["username"]
        assert data["email"] == user_data["email"]
        assert "hashed_password" not in data  # Password should not be returned
    
    def test_get_current_user(self):
        """Test getting current user information."""
        # First, login to get token
        login_response = client.post(
            "/api/v1/auth/token",
            data={"username": "admin", "password": "admin123"}
        )
        token = login_response.json()["access_token"]
        
        # Then, get current user
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "admin"


class TestProtectedEndpoints:
    """Test endpoints that require authentication."""
    
    @pytest.fixture
    def auth_headers(self):
        """Get authentication headers."""
        login_response = client.post(
            "/api/v1/auth/token",
            data={"username": "admin", "password": "admin123"}
        )
        token = login_response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}
    
    def test_get_users_authenticated(self, auth_headers):
        """Test getting users with authentication."""
        response = client.get("/api/v1/users/", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
    
    def test_get_users_unauthenticated(self):
        """Test getting users without authentication."""
        response = client.get("/api/v1/users/")
        assert response.status_code == 401
    
    def test_upload_info_public(self):
        """Test that upload info is public."""
        response = client.get("/api/v1/upload/info")
        assert response.status_code == 200
        data = response.json()
        assert "max_file_size_mb" in data
        assert "allowed_extensions" in data


if __name__ == "__main__":
    pytest.main([__file__])
