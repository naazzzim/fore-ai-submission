from pydantic import BaseModel, Field
from typing import Optional


class HealthResponse(BaseModel):
    """Health check response model"""
    status: str = Field(..., description="Health status")


class ErrorResponse(BaseModel):
    """Error response model"""
    detail: str = Field(..., description="Error detail")
    error_code: Optional[str] = Field(None, description="Error code")
