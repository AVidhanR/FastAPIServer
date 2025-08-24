"""
FastAPI Demo Server
A comprehensive backend server showcasing various API types and features.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.core.config import settings
from app.api import auth, users, products, files, misc

# Create FastAPI instance
app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create uploads directory if it doesn't exist
os.makedirs("uploads", exist_ok=True)

# Mount static files for file downloads
app.mount("/files", StaticFiles(directory="uploads"), name="files")

# Include API routers
app.include_router(
    auth.router,
    prefix=f"{settings.api_v1_prefix}/auth",
    tags=["Authentication"]
)

app.include_router(
    users.router,
    prefix=f"{settings.api_v1_prefix}/users",
    tags=["User Management"]
)

app.include_router(
    products.router,
    prefix=f"{settings.api_v1_prefix}/products",
    tags=["Product Management"]
)

app.include_router(
    files.router,
    prefix=f"{settings.api_v1_prefix}/upload",
    tags=["File Upload"]
)

app.include_router(
    misc.router,
    prefix=f"{settings.api_v1_prefix}/misc",
    tags=["Miscellaneous"]
)


@app.get("/")
async def root():
    """
    Root endpoint.
    
    Welcome message with basic API information.
    """
    return {
        "message": "Welcome to FastAPI Demo Server!",
        "version": settings.app_version,
        "docs_url": "/docs",
        "redoc_url": "/redoc",
        "api_prefix": settings.api_v1_prefix
    }


@app.get("/api/v1")
async def api_info():
    """
    API information endpoint.
    
    Returns information about available API endpoints.
    """
    return {
        "message": "FastAPI Demo Server API v1",
        "endpoints": {
            "authentication": f"{settings.api_v1_prefix}/auth",
            "users": f"{settings.api_v1_prefix}/users",
            "products": f"{settings.api_v1_prefix}/products",
            "file_upload": f"{settings.api_v1_prefix}/upload",
            "miscellaneous": f"{settings.api_v1_prefix}/misc"
        },
        "documentation": {
            "swagger_ui": "/docs",
            "redoc": "/redoc"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
