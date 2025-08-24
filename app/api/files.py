"""
File upload API endpoints.
"""
import os
import uuid
from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status

from app.models import User, UploadResponse, FileInfo
from app.api.auth import get_current_active_user

router = APIRouter()

# Directory to store uploaded files (in production, use cloud storage)
UPLOAD_DIRECTORY = "uploads"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".pdf", ".txt", ".docx", ".xlsx"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


def validate_file(file: UploadFile) -> None:
    """Validate uploaded file."""
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No file name provided"
        )
    
    # Check file extension
    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        )


@router.post("/single", response_model=UploadResponse)
async def upload_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user)
):
    """
    Upload a single file.
    
    Upload a file to the server. Requires authentication.
    Maximum file size: 10MB.
    Allowed extensions: jpg, jpeg, png, gif, pdf, txt, docx, xlsx.
    """
    validate_file(file)
    
    # Read file content to check size
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File too large. Maximum size: {MAX_FILE_SIZE // 1024 // 1024}MB"
        )
    
    # Generate unique filename
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(UPLOAD_DIRECTORY, unique_filename)
    
    # Save file
    with open(file_path, "wb") as buffer:
        buffer.write(content)
    
    # Create file info
    file_info = FileInfo(
        filename=file.filename,
        content_type=file.content_type or "application/octet-stream",
        size=len(content),
        uploaded_at=datetime.utcnow()
    )
    
    return UploadResponse(
        message="File uploaded successfully",
        file_info=file_info,
        file_url=f"/files/{unique_filename}"
    )


@router.post("/multiple", response_model=List[UploadResponse])
async def upload_files(
    files: List[UploadFile] = File(...),
    current_user: User = Depends(get_current_active_user)
):
    """
    Upload multiple files.
    
    Upload multiple files to the server. Requires authentication.
    Maximum of 5 files per request.
    """
    if len(files) > 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Maximum 5 files allowed per request"
        )
    
    responses = []
    for file in files:
        try:
            validate_file(file)
            
            # Read file content
            content = await file.read()
            if len(content) > MAX_FILE_SIZE:
                responses.append(UploadResponse(
                    message=f"File {file.filename} too large",
                    file_info=FileInfo(
                        filename=file.filename or "unknown",
                        content_type="unknown",
                        size=len(content),
                        uploaded_at=datetime.utcnow()
                    )
                ))
                continue
            
            # Generate unique filename
            file_extension = os.path.splitext(file.filename)[1]
            unique_filename = f"{uuid.uuid4()}{file_extension}"
            file_path = os.path.join(UPLOAD_DIRECTORY, unique_filename)
            
            # Save file
            with open(file_path, "wb") as buffer:
                buffer.write(content)
            
            # Create file info
            file_info = FileInfo(
                filename=file.filename,
                content_type=file.content_type or "application/octet-stream",
                size=len(content),
                uploaded_at=datetime.utcnow()
            )
            
            responses.append(UploadResponse(
                message="File uploaded successfully",
                file_info=file_info,
                file_url=f"/files/{unique_filename}"
            ))
            
        except HTTPException as e:
            responses.append(UploadResponse(
                message=f"Error uploading {file.filename}: {e.detail}",
                file_info=FileInfo(
                    filename=file.filename or "unknown",
                    content_type="unknown",
                    size=0,
                    uploaded_at=datetime.utcnow()
                )
            ))
    
    return responses


@router.get("/info")
async def get_upload_info():
    """
    Get upload information.
    
    Returns information about file upload constraints.
    Public endpoint - no authentication required.
    """
    return {
        "max_file_size_mb": MAX_FILE_SIZE // 1024 // 1024,
        "allowed_extensions": list(ALLOWED_EXTENSIONS),
        "max_files_per_request": 5
    }
