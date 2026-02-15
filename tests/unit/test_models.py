"""
Unit tests for Pydantic models.
"""

import pytest
from pydantic import ValidationError
from src.models import PackageRequest, PackageResponse, HealthResponse


class TestPackageRequest:
    """Test cases for PackageRequest model."""

    def test_valid_request(self):
        """Test valid package request."""
        request = PackageRequest(width=10.0, height=10.0, length=10.0, mass=5.0)
        assert request.width == 10.0
        assert request.height == 10.0
        assert request.length == 10.0
        assert request.mass == 5.0

    def test_invalid_negative_values(self):
        """Test rejection of negative values."""
        with pytest.raises(ValidationError):
            PackageRequest(width=-10.0, height=10.0, length=10.0, mass=5.0)

        with pytest.raises(ValidationError):
            PackageRequest(width=10.0, height=-10.0, length=10.0, mass=5.0)

        with pytest.raises(ValidationError):
            PackageRequest(width=10.0, height=10.0, length=-10.0, mass=5.0)

        with pytest.raises(ValidationError):
            PackageRequest(width=10.0, height=10.0, length=10.0, mass=-5.0)

    def test_invalid_zero_values(self):
        """Test rejection of zero values."""
        with pytest.raises(ValidationError):
            PackageRequest(width=0.0, height=10.0, length=10.0, mass=5.0)

        with pytest.raises(ValidationError):
            PackageRequest(width=10.0, height=0.0, length=10.0, mass=5.0)

        with pytest.raises(ValidationError):
            PackageRequest(width=10.0, height=10.0, length=0.0, mass=5.0)

        with pytest.raises(ValidationError):
            PackageRequest(width=10.0, height=10.0, length=10.0, mass=0.0)


class TestPackageResponse:
    """Test cases for PackageResponse model."""

    def test_valid_responses(self):
        """Test valid package responses."""
        response = PackageResponse(stack="STANDARD")
        assert response.stack == "STANDARD"

        response = PackageResponse(stack="SPECIAL")
        assert response.stack == "SPECIAL"

        response = PackageResponse(stack="REJECTED")
        assert response.stack == "REJECTED"

    def test_invalid_stack_value(self):
        """Test rejection of invalid stack values."""
        with pytest.raises(ValidationError):
            PackageResponse(stack="INVALID")

        with pytest.raises(ValidationError):
            PackageResponse(stack="standard")  # lowercase

        with pytest.raises(ValidationError):
            PackageResponse(stack="")


class TestHealthResponse:
    """Test cases for HealthResponse model."""

    def test_valid_response(self):
        """Test valid health response."""
        response = HealthResponse(status="healthy")
        assert response.status == "healthy"

    def test_empty_status(self):
        """Test rejection of empty status."""
        with pytest.raises(ValidationError):
            HealthResponse(status="")