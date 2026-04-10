"""
Prediction API Routes
=====================
Endpoints for plant disease prediction, batch processing, and history.
"""

import os
import uuid
from pathlib import Path

from fastapi import APIRouter, File, Form, HTTPException, UploadFile, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional

from backend.app.core.config import settings
from backend.app.core.logging import logger
from backend.app.models.schemas import (
    PredictionResponse,
    HealthResponse,
    ClassInfo,
    ErrorResponse
)
from backend.app.services.ml_service import classifier

router = APIRouter(prefix="/api", tags=["prediction"])

ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"}


def validate_file(file: UploadFile) -> None:
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
    return JSONResponse(
        status_code=200,
        content={
            "status": "healthy",
            "model_loaded": classifier.model_loaded,
            "model_version": "2.0.0",
            "model_type": getattr(classifier, 'model_type', 'CNN')
        }
    )


@router.post("/predict", response_model=PredictionResponse)
async def predict_disease(
    file: UploadFile = File(...),
    user_id: Optional[str] = Form(None)
) -> JSONResponse:
    try:
        validate_file(file)
        
        upload_dir = Path(settings.UPLOAD_DIR)
        upload_dir.mkdir(parents=True, exist_ok=True)
        
        file_ext = Path(file.filename).suffix.lower()
        unique_filename = f"{uuid.uuid4()}{file_ext}"
        file_path = upload_dir / unique_filename
        
        content = await file.read()
        
        if len(content) > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail=f"File too large. Max: {settings.MAX_FILE_SIZE / (1024*1024)}MB"
            )
        
        with open(file_path, "wb") as f:
            f.write(content)
        
        result = classifier.predict(str(file_path))
        
        try:
            os.remove(file_path)
        except Exception:
            pass
        
        if not result.get("success", False):
            raise HTTPException(
                status_code=500,
                detail=result.get("error", "Prediction failed")
            )
        
        if user_id:
            try:
                from backend.app.api.dashboard.routes import load_history, save_history
                from datetime import datetime
                
                history = load_history()
                history.append({
                    "user_id": user_id,
                    "disease": result.get("disease"),
                    "confidence": result.get("confidence", 0) / 100,
                    "timestamp": datetime.utcnow().isoformat()
                })
                save_history(history)
            except Exception as e:
                logger.warning(f"Failed to record history: {e}")
        
        return JSONResponse(status_code=200, content=result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@router.post("/predict/batch")
async def predict_batch(files: List[UploadFile] = File(...)) -> JSONResponse:
    try:
        results = []
        upload_dir = Path(settings.UPLOAD_DIR)
        upload_dir.mkdir(parents=True, exist_ok=True)
        
        for file in files:
            validate_file(file)
            
            file_ext = Path(file.filename).suffix.lower()
            unique_filename = f"{uuid.uuid4()}{file_ext}"
            file_path = upload_dir / unique_filename
            
            content = await file.read()
            
            if len(content) > settings.MAX_FILE_SIZE:
                results.append({
                    "filename": file.filename,
                    "success": False,
                    "error": "File too large"
                })
                continue
            
            with open(file_path, "wb") as f:
                f.write(content)
            
            result = classifier.predict(str(file_path))
            
            try:
                os.remove(file_path)
            except Exception:
                pass
            
            results.append({
                "filename": file.filename,
                **result
            })
        
        return JSONResponse(status_code=200, content={
            "success": True,
            "results": results,
            "total": len(files),
            "processed": len([r for r in results if r.get("success")])
        })
        
    except Exception as e:
        logger.error(f"Batch prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/classes", response_model=ClassInfo)
async def get_classes() -> JSONResponse:
    class_info = classifier.get_classes()
    return JSONResponse(status_code=200, content=class_info)


@router.get("/crops")
async def get_crops() -> JSONResponse:
    crops = classifier.get_crops()
    return JSONResponse(status_code=200, content=crops)


@router.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "status_code": exc.status_code}
    )


@router.exception_handler(Exception)
async def general_exception_handler(request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": str(exc)}
    )
