"""
User role models for IBS HI Sale Platform.
Defines schemas for user management and access control.
"""

from pydantic import BaseModel
from typing import Optional, List


class UserRoleCreate(BaseModel):
    """Request schema for creating a new user."""
    user_name: str
    email: str
    department: str
    role: str = "MEMBER"
    permissions: Optional[List[str]] = None

    class Config:
        json_schema_extra = {
            "example": {
                "user_name": "Hiệu",
                "email": "hieu@example.com",
                "department": "TCKT",
                "role": "MEMBER",
                "permissions": ["view_all_emails", "create_task"],
            }
        }


class UserRoleUpdate(BaseModel):
    """Request schema for updating a user."""
    user_name: Optional[str] = None
    email: Optional[str] = None
    department: Optional[str] = None
    role: Optional[str] = None
    permissions: Optional[List[str]] = None
    is_active: Optional[bool] = None

    class Config:
        json_schema_extra = {
            "example": {
                "role": "MANAGER",
                "is_active": True,
                "permissions": ["view_all_emails", "create_task", "manage_pipeline"],
            }
        }


class UserRoleResponse(BaseModel):
    """Response schema for user data."""
    id: str
    user_name: str
    email: str
    department: str
    role: str
    permissions: Optional[List[str]]
    is_active: bool
    joined_at: str
    deactivated_at: Optional[str]
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True
