"""
NAS File Link models for IBS HI Sale Platform.
Defines schemas for linking NAS file paths to platform entities.
"""

from pydantic import BaseModel
from typing import Optional


class NasFileCreate(BaseModel):
    """Request schema for creating a NAS file link."""
    entity_type: str
    entity_id: str
    nas_path: str
    file_name: str
    file_type: Optional[str] = "OTHER"
    description: Optional[str] = ""

    class Config:
        json_schema_extra = {
            "example": {
                "entity_type": "opportunity",
                "entity_id": "opp-001",
                "nas_path": "//nas/sales/quotes/2026/project-alpha.pdf",
                "file_name": "project-alpha.pdf",
                "file_type": "QUOTE",
                "description": "Final quotation for Project Alpha",
            }
        }


class NasFileResponse(BaseModel):
    """Response schema for NAS file link data."""
    id: str
    entity_type: str
    entity_id: str
    nas_path: str
    file_name: str
    file_type: Optional[str]
    description: Optional[str]
    created_at: str

    class Config:
        from_attributes = True
