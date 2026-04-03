"""
Core Configuration Module
=========================
Handles environment variables and application settings.
"""

import os
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # ML Model
    MODEL_PATH: str = "ml/model/plant_disease_model.keras"
    IMAGE_SIZE: int = 128

    # Upload
    UPLOAD_DIR: str = "backend/app/uploads"
    MAX_FILE_SIZE: int = 16 * 1024 * 1024  # 16MB

    # CORS
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:5173"

    # Logging
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        case_sensitive = True

    @property
    def cors_origins_list(self) -> list[str]:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()