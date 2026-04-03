"""Backend API module."""

from backend.app.api.prediction import router as prediction_router

__all__ = ["prediction_router"]