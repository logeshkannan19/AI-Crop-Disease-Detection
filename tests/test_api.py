"""
API Integration Tests
=====================
"""

import pytest
from httpx import AsyncClient
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.mark.asyncio
async def test_health_endpoint():
    """Test health check endpoint."""
    from backend.app.main import app
    
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/health")
        
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "model_loaded" in data


@pytest.mark.asyncio
async def test_root_endpoint():
    """Test root endpoint returns API info."""
    from backend.app.main import app
    
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/")
        
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "version" in data


@pytest.mark.asyncio
async def test_classes_endpoint():
    """Test get classes endpoint."""
    from backend.app.main import app
    
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/classes")
        
    assert response.status_code == 200
    data = response.json()
    assert "classes" in data
    assert "treatments" in data


@pytest.mark.asyncio
async def test_predict_no_file():
    """Test predict endpoint with no file."""
    from backend.app.main import app
    
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/predict")
        
    assert response.status_code == 422  # Validation error


@pytest.mark.asyncio
async def test_predict_invalid_extension():
    """Test predict endpoint with invalid file type."""
    from backend.app.main import app
    
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/predict",
            files={"file": ("test.txt", b"test", "text/plain")}
        )
        
    assert response.status_code == 400


if __name__ == "__main__":
    pytest.main([__file__, "-v"])