"""
Pydantic models for Package Sorting API.
"""

from pydantic import BaseModel, Field, validator
from typing import Literal


class PackageRequest(BaseModel):
    """Request model for package sorting."""
    width: float = Field(..., gt=0, description="Width in centimeters")
    height: float = Field(..., gt=0, description="Height in centimeters")
    length: float = Field(..., gt=0, description="Length in centimeters")
    mass: float = Field(..., gt=0, description="Mass in kilograms")


class PackageResponse(BaseModel):
    """Response model for package sorting."""
    stack: Literal["STANDARD", "SPECIAL", "REJECTED"] = Field(..., description="The stack where the package should be dispatched")


class HealthResponse(BaseModel):
    """Response model for health check."""
    status: str = Field(..., description="Health status")