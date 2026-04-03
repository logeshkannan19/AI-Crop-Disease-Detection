"""
Logging Configuration
====================
Centralized logging setup for the application.
"""

import logging
import sys
from typing import Any

from backend.app.core.config import settings


def setup_logging() -> logging.Logger:
    """
    Configure and return the application logger.
    
    Returns:
        logging.Logger: Configured logger instance
    """
    # Create logger
    logger = logging.getLogger("agriscan")
    
    # Set level from settings
    level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
    logger.setLevel(level)
    
    # Create console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    
    # Create formatter
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(handler)
    
    return logger


# Create logger instance
logger = setup_logging()


def log_request(method: str, path: str, status_code: int, duration: float) -> None:
    """Log HTTP request details."""
    logger.info(f"{method} {path} - {status_code} - {duration:.3f}s")


def log_error(error: Any, context: str = "") -> None:
    """Log error with context."""
    logger.error(f"Error{': ' + context if context else ''} - {str(error)}")


def log_info(message: str) -> None:
    """Log info message."""
    logger.info(message)