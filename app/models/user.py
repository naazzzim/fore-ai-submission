from pydantic import BaseModel, Field
from typing import Optional


class User(BaseModel):
    """User model"""
    id: int = Field(..., description="User ID")
    username: str = Field(..., min_length=3, max_length=50, description="Username")
    email: str = Field(..., description="Email")
    is_active: bool = Field(default=True, description="User active status")


class UserCreate(BaseModel):
    """User creation model"""
    username: str = Field(..., min_length=3, max_length=50, description="Username")
    email: str = Field(..., description="Email")


class UserUpdate(BaseModel):
    """User update model"""
    username: Optional[str] = Field(None, min_length=3, max_length=50, description="Username")
    email: Optional[str] = Field(None, description="Email")
    is_active: Optional[bool] = Field(None, description="User active status")
