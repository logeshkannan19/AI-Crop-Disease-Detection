"""
Prediction API Routes
=====================
Endpoints for plant disease prediction.
"""

import os
import uuid
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse

from backend.app.core.config import settings
from backend.app.core.logging import logger
from backend.app.models.schemas import (
    PredictionResponse,
    HealthResponse,
    ClassInfo,
    ErrorResponse
)
from backend.app.services.ml_service import classifier

# Create router
router = APIRouter(prefix="/api", tags=["prediction"])

# Allowed file extensions
ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"}


def validate_file(file: UploadFile) -> None:
    """Validate uploaded file."""
    if not file:
        raise HTTPException(status_code=400, detail="No file provided")
    
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        )


@router.get("/health", response_model=HealthResponse)
async def health_check() -> JSONResponse:
    """
    Health check endpoint.
    
    Returns the service status and model loading state.
    """
    return JSONResponse(
        status_code=200,
        content={
            "status": "healthy",
            "model_loaded": classifier.model_loaded,
            "model_version": "1.0.0"
        }
    )


@router.post("/predict", response_model=PredictionResponse)
async def predict_disease(file: UploadFile = File(...)) -> JSONResponse:
    """
    Predict disease from an uploaded plant leaf image.
    
    Args:
        file: Image file upload
        
    Returns:
        Prediction results with disease name, confidence, and treatment
    """
    try:
        # Validate file
        validate_file(file)
        
        # Create upload directory
        upload_dir = Path(settings.UPLOAD_DIR)
        upload_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate unique filename
        file_ext = Path(file.filename).suffix.lower()
        unique_filename = f"{uuid.uuid4()}{file_ext}"
        file_path = upload_dir / unique_filename
        
        # Save uploaded file
        content = await file.read()
        
        # Check file size
        if len(content) > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail=f"File too large. Maximum size: {settings.MAX_FILE_SIZE / (1024*1024)}MB"
            )
        
        with open(file_path, "wb") as f:
            f.write(content)
        
        logger.info(f"File saved: {file_path}")
        
        # Make prediction
        result = classifier.predict(str(file_path))
        
        # Clean up uploaded file
        try:
            os.remove(file_path)
            logger.info(f"File cleaned up: {file_path}")
        except Exception as e:
            logger.warning(f"Failed to clean up file: {e}")
        
        if not result.get("success", False):
            raise HTTPException(
                status_code=500,
                detail=result.get("error", "Prediction failed")
            )
        
        return JSONResponse(
            status_code=200,
            content=result
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/classes", response_model=ClassInfo)
async def get_classes() -> JSONResponse:
    """
    Get list of supported disease classes and treatments.
    
    Returns:
        Dictionary with class names and treatment recommendations
    """
    class_info = classifier.get_classes()
    return JSONResponse(
        status_code=200,
        content=class_info
    )


# Error handlers
@router.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    """Handle HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code
        }
    )


@router.exception_handler(Exception)
async def general_exception_handler(request, exc: Exception):
    """Handle general exceptions."""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc)
        }
    )