"""
Data Models
===========
Pydantic models for request/response validation.
"""

from pydantic import BaseModel, Field
from typing import Optional


class PredictionRequest(BaseModel):
    """Request model for image prediction."""
    pass


class PredictionTopResult(BaseModel):
    """Individual prediction result."""
    disease: str = Field(..., description="Disease name")
    confidence: float = Field(..., description="Confidence score (0-1)")


class PredictionResponse(BaseModel):
    """Response model for disease prediction."""
    success: bool = Field(..., description="Whether prediction was successful")
    disease: str = Field(..., description="Detected disease name")
    disease_readable: str = Field(..., description="Human-readable disease name")
    confidence: float = Field(..., description="Confidence score (0-100)")
    treatment: str = Field(..., description="Recommended treatment")
    top_predictions: list[PredictionTopResult] = Field(
        default_factory=list,
        description="Top 3 predictions with confidence scores"
    )


class HealthResponse(BaseModel):
    """Response model for health check."""
    status: str = Field(..., description="Service status")
    model_loaded: bool = Field(..., description="Whether ML model is loaded")
    model_version: Optional[str] = Field(None, description="Model version")


class ClassInfo(BaseModel):
    """Model class information."""
    classes: list[str] = Field(..., description="List of supported disease classes")
    treatments: dict[str, str] = Field(..., description="Treatment recommendations by disease")


class ErrorResponse(BaseModel):
    """Error response model."""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")