"""
Integration tests for Package Sorting API.
"""

import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient

from src.api import app


@pytest.fixture
def client():
    """Test client fixture."""
    return TestClient(app)


@pytest.fixture
async def async_client():
    """Async test client fixture."""
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client


class TestSortEndpoint:
    """Test cases for /sort endpoint."""

    def test_sort_standard_package(self, client):
        """Test sorting standard package."""
        response = client.post("/sort", json={
            "width": 10.0,
            "height": 10.0,
            "length": 10.0,
            "mass": 5.0
        })

        assert response.status_code == 200
        data = response.json()
        assert data["stack"] == "STANDARD"

    def test_sort_special_bulky_package(self, client):
        """Test sorting bulky package."""
        response = client.post("/sort", json={
            "width": 150.0,
            "height": 10.0,
            "length": 10.0,
            "mass": 5.0
        })

        assert response.status_code == 200
        data = response.json()
        assert data["stack"] == "SPECIAL"

    def test_sort_special_heavy_package(self, client):
        """Test sorting heavy package."""
        response = client.post("/sort", json={
            "width": 10.0,
            "height": 10.0,
            "length": 10.0,
            "mass": 20.0
        })

        assert response.status_code == 200
        data = response.json()
        assert data["stack"] == "SPECIAL"

    def test_sort_rejected_package(self, client):
        """Test sorting rejected package."""
        response = client.post("/sort", json={
            "width": 150.0,
            "height": 10.0,
            "length": 10.0,
            "mass": 20.0
        })

        assert response.status_code == 200
        data = response.json()
        assert data["stack"] == "REJECTED"

    def test_invalid_input_negative_width(self, client):
        """Test validation error for negative width."""
        response = client.post("/sort", json={
            "width": -10.0,
            "height": 10.0,
            "length": 10.0,
            "mass": 5.0
        })

        assert response.status_code == 422  # Validation error

    def test_invalid_input_zero_mass(self, client):
        """Test validation error for zero mass."""
        response = client.post("/sort", json={
            "width": 10.0,
            "height": 10.0,
            "length": 10.0,
            "mass": 0.0
        })

        assert response.status_code == 422  # Validation error

    def test_invalid_json(self, client):
        """Test error for invalid JSON."""
        response = client.post("/sort", data="invalid json")

        assert response.status_code == 422  # Validation error

    def test_missing_fields(self, client):
        """Test validation error for missing fields."""
        response = client.post("/sort", json={
            "width": 10.0,
            "height": 10.0
            # missing length and mass
        })

        assert response.status_code == 422  # Validation error


class TestHealthEndpoint:
    """Test cases for /health endpoint."""

    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"


@pytest.mark.asyncio
class TestAsyncEndpoints:
    """Test async endpoints."""

    async def test_async_sort(self, async_client):
        """Test async sorting."""
        response = await async_client.post("/sort", json={
            "width": 10.0,
            "height": 10.0,
            "length": 10.0,
            "mass": 5.0
        })

        assert response.status_code == 200
        data = response.json()
        assert data["stack"] == "STANDARD"

    async def test_async_health(self, async_client):
        """Test async health check."""
        response = await async_client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"