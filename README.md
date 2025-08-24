# FastAPI Demo Server

A comprehensive FastAPI backend server demonstration showcasing various types of APIs, authentication, file uploads, and best practices.

## Features

- 🔐 **JWT Authentication** - Secure token-based authentication
- 👥 **User Management** - Complete CRUD operations for users
- 📦 **Product Management** - Product catalog with search and filtering
- 📁 **File Upload** - Single and multiple file upload capabilities
- 🔍 **Search & Filtering** - Advanced search and filtering options
- 📚 **API Documentation** - Auto-generated Swagger/OpenAPI docs
- 🛡️ **Role-based Access Control** - Admin and user roles
- 🌐 **CORS Support** - Cross-origin resource sharing
- ✅ **Input Validation** - Pydantic models for data validation
- 🏗️ **Clean Architecture** - Well-organized folder structure

## Project Structure

```
FastAPIServer/
├── app/
│   ├── api/              # API endpoints
│   │   ├── auth.py       # Authentication endpoints
│   │   ├── users.py      # User management endpoints
│   │   ├── products.py   # Product management endpoints
│   │   ├── files.py      # File upload endpoints
│   │   └── misc.py       # Miscellaneous endpoints
│   ├── core/             # Core functionality
│   │   ├── config.py     # Application configuration
│   │   └── security.py   # Security utilities
│   ├── models/           # Pydantic models
│   │   └── __init__.py   # Data models and schemas
│   └── services/         # Business logic
│       ├── user_service.py    # User business logic
│       └── product_service.py # Product business logic
├── tests/                # Test files
├── uploads/              # File upload directory
├── main.py              # Application entry point
├── pyproject.toml       # Project configuration
└── README.md           # This file
```

## Installation

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd FastAPIServer
   ```

2. **Install dependencies:**

   ```bash
   pip install -e .
   ```

   Or install with development dependencies:

   ```bash
   pip install -e ".[dev]"
   ```

## Running the Server

### Development Mode

```bash
python main.py
```

### Production Mode

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

The server will be available at:

- **API**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Authentication (`/api/v1/auth`)

| Method | Endpoint    | Description               | Auth Required |
| ------ | ----------- | ------------------------- | ------------- |
| POST   | `/token`    | Login to get access token | No            |
| POST   | `/register` | Register new user         | No            |
| GET    | `/me`       | Get current user info     | Yes           |

**Example - Login:**

```bash
curl -X POST "http://localhost:8000/api/v1/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"
```

**Example - Register:**

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "email": "user@example.com",
    "password": "password123",
    "full_name": "New User"
  }'
```

### User Management (`/api/v1/users`)

| Method | Endpoint     | Description     | Auth Required | Admin Only |
| ------ | ------------ | --------------- | ------------- | ---------- |
| GET    | `/`          | List all users  | Yes           | No         |
| GET    | `/{user_id}` | Get user by ID  | Yes           | No         |
| POST   | `/`          | Create new user | Yes           | Yes        |
| PUT    | `/{user_id}` | Update user     | Yes           | Self/Admin |
| DELETE | `/{user_id}` | Delete user     | Yes           | Yes        |

**Example - Get all users:**

```bash
curl -X GET "http://localhost:8000/api/v1/users/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Product Management (`/api/v1/products`)

| Method | Endpoint         | Description       | Auth Required | Admin Only |
| ------ | ---------------- | ----------------- | ------------- | ---------- |
| GET    | `/`              | List products     | No            | No         |
| GET    | `/search?q=term` | Search products   | No            | No         |
| GET    | `/{product_id}`  | Get product by ID | No            | No         |
| POST   | `/`              | Create product    | Yes           | Yes        |
| PUT    | `/{product_id}`  | Update product    | Yes           | Yes        |
| DELETE | `/{product_id}`  | Delete product    | Yes           | Yes        |

**Query Parameters for GET `/`:**

- `skip`: Number of items to skip (pagination)
- `limit`: Number of items to return (max 100)
- `category`: Filter by category (electronics, clothing, books, home, sports)
- `in_stock`: Filter by stock status (true/false)

**Example - Get products:**

```bash
curl -X GET "http://localhost:8000/api/v1/products/?category=electronics&in_stock=true"
```

**Example - Search products:**

```bash
curl -X GET "http://localhost:8000/api/v1/products/search?q=macbook"
```

### File Upload (`/api/v1/upload`)

| Method | Endpoint    | Description            | Auth Required |
| ------ | ----------- | ---------------------- | ------------- |
| POST   | `/single`   | Upload single file     | Yes           |
| POST   | `/multiple` | Upload multiple files  | Yes           |
| GET    | `/info`     | Get upload constraints | No            |

**Supported File Types:** jpg, jpeg, png, gif, pdf, txt, docx, xlsx
**Maximum File Size:** 10MB
**Maximum Files per Request:** 5 files

**Example - Upload single file:**

```bash
curl -X POST "http://localhost:8000/api/v1/upload/single" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -F "file=@/path/to/your/file.pdf"
```

### Miscellaneous (`/api/v1/misc`)

| Method | Endpoint                 | Description             |
| ------ | ------------------------ | ----------------------- |
| GET    | `/health`                | Health check            |
| GET    | `/ping`                  | Simple ping test        |
| GET    | `/time`                  | Get server time         |
| GET    | `/echo?message=hello`    | Echo message            |
| POST   | `/echo`                  | Echo JSON data          |
| GET    | `/random-quote`          | Get random quote        |
| GET    | `/weather?city=London`   | Get weather (mock data) |
| GET    | `/slow?delay=5`          | Slow endpoint (testing) |
| GET    | `/error?status_code=404` | Trigger error (testing) |

## Default Users

The application creates default users for testing:

| Username | Password | Role  | Email             |
| -------- | -------- | ----- | ----------------- |
| admin    | admin123 | admin | admin@example.com |
| john_doe | user123  | user  | john@example.com  |

## Authentication Flow

1. **Register** a new user or use default credentials
2. **Login** to get an access token:
   ```bash
   POST /api/v1/auth/token
   {
     "username": "admin",
     "password": "admin123"
   }
   ```
3. **Use the token** in subsequent requests:
   ```bash
   Authorization: Bearer YOUR_ACCESS_TOKEN
   ```

## Data Models

### User Model

```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "full_name": "John Doe",
  "role": "user",
  "is_active": true,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": null
}
```

### Product Model

```json
{
  "id": 1,
  "name": "MacBook Pro",
  "description": "Apple MacBook Pro 16-inch with M2 chip",
  "price": 2499.99,
  "category": "electronics",
  "in_stock": true,
  "stock_quantity": 10,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": null
}
```

## Error Handling

The API uses standard HTTP status codes:

- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `422` - Validation Error
- `500` - Internal Server Error

Error responses follow this format:

```json
{
  "detail": "Error message description"
}
```

## Development

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black app/ tests/
```

### Linting

```bash
flake8 app/ tests/
```

## Configuration

The application can be configured using environment variables or a `.env` file:

```env
# Application settings
APP_NAME=FastAPI Demo Server
DEBUG=true

# Security
SECRET_KEY=your-super-secret-key-change-this-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080
```

## Production Deployment

For production deployment:

1. Set `DEBUG=false`
2. Use a strong `SECRET_KEY`
3. Configure proper CORS origins
4. Use a production WSGI server like Gunicorn
5. Set up a reverse proxy (nginx)
6. Use a proper database instead of in-memory storage
7. Implement proper logging and monitoring

### Docker Deployment (Example)

```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY . /app

RUN pip install -e .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## API Testing with curl

### Complete workflow example:

```bash
# 1. Health check
curl http://localhost:8000/api/v1/misc/health

# 2. Login to get token
TOKEN=$(curl -X POST "http://localhost:8000/api/v1/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123" | jq -r .access_token)

# 3. Get current user info
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/v1/auth/me

# 4. List products
curl http://localhost:8000/api/v1/products/

# 5. Create a new product (admin only)
curl -X POST "http://localhost:8000/api/v1/products/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "New Product",
    "description": "A great product",
    "price": 99.99,
    "category": "electronics",
    "stock_quantity": 5
  }'

# 6. Upload a file
curl -X POST "http://localhost:8000/api/v1/upload/single" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@README.md"
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Run tests and linting
6. Submit a pull request

## License

This project is for demonstration purposes. Feel free to use it as a starting point for your FastAPI projects.

## Support

For questions or issues, please create an issue in the repository or refer to the [FastAPI documentation](https://fastapi.tiangolo.com/).
