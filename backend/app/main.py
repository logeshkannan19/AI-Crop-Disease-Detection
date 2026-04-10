"""
AgriScan AI - Main Application Entry Point
==========================================
FastAPI backend for AI-powered crop disease detection.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.core.config import settings
from backend.app.core.logging import logger
from backend.app.api.prediction import router as prediction_router
from backend.app.api.auth.routes import router as auth_router
from backend.app.api.dashboard.routes import router as dashboard_router
from backend.app.services.ml_service import classifier


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan handler.
    
    Handles startup and shutdown events.
    """
    # Startup
    logger.info("=" * 60)
    logger.info("Starting AgriScan AI Backend")
    logger.info(f"Model loaded: {classifier.model_loaded}")
    logger.info(f"Server: {settings.HOST}:{settings.PORT}")
    logger.info("=" * 60)
    
    yield
    
    # Shutdown
    logger.info("Shutting down AgriScan AI Backend")


# Create FastAPI application
app = FastAPI(
    title="AgriScan AI API",
    description="AI-Powered Crop Disease Detection System",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(prediction_router)
app.include_router(auth_router)
app.include_router(dashboard_router)


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "AgriScan AI API",
        "version": "1.0.0",
        "description": "AI-Powered Crop Disease Detection System",
        "docs": "/docs",
        "endpoints": {
            "health": "/api/health",
            "predict": "/api/predict (POST)",
            "classes": "/api/classes (GET)"
        }
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "backend.app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True
    )