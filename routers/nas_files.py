"""
NAS Files Router
Manages NAS file path links to platform entities (opportunities, customers, tasks, emails).
"""

from fastapi import APIRouter, Query, HTTPException
from ..database import query, execute
from ..models.nas_file import NasFileCreate, NasFileResponse
from datetime import datetime
import uuid

router = APIRouter(prefix="/nas-files", tags=["NAS Files"])

VALID_ENTITY_TYPES = ("opportunity", "customer", "task", "email")


@router.get("")
async def list_nas_files(
    entity_type: str = Query(..., description="Entity type (opportunity, customer, task, email)"),
    entity_id: str = Query(..., description="Entity ID (UUID)"),
):
    """
    List NAS file links filtered by entity_type and entity_id.
    Both query parameters are required.

    Args:
        entity_type: Type of entity (opportunity, customer, task, email)
        entity_id: ID of the entity

    Returns:
        list: List of NAS file link records
    """
    if entity_type not in VALID_ENTITY_TYPES:
        raise HTTPException(
            status_code=422,
            detail=f"Invalid entity_type '{entity_type}'. Must be one of: {', '.join(VALID_ENTITY_TYPES)}",
        )

    items = query(
        """
        SELECT * FROM sale_nas_file_links
        WHERE entity_type = ? AND entity_id = ?
        ORDER BY created_at DESC
        """,
        [entity_type, entity_id],
    )

    return items


@router.post("", status_code=201)
async def create_nas_file(payload: NasFileCreate):
    """
    Create a new NAS file link.

    Args:
        payload: NasFileCreate schema with entity_type, entity_id, nas_path, file_name, etc.

    Returns:
        dict: Created NAS file link record
    """
    if payload.entity_type not in VALID_ENTITY_TYPES:
        raise HTTPException(
            status_code=422,
            detail=f"Invalid entity_type '{payload.entity_type}'. Must be one of: {', '.join(VALID_ENTITY_TYPES)}",
        )

    new_id = str(uuid.uuid4())
    now = datetime.utcnow().isoformat()

    execute(
        """
        INSERT INTO sale_nas_file_links (id, entity_type, entity_id, nas_path, file_name, file_type, description, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [new_id, payload.entity_type, payload.entity_id, payload.nas_path, payload.file_name, payload.file_type, payload.description, now],
    )

    record = query(
        "SELECT * FROM sale_nas_file_links WHERE id = ?",
        [new_id],
        one=True,
    )

    return record


@router.get("/{file_id}")
async def get_nas_file(file_id: str):
    """
    Get a single NAS file link by ID.

    Args:
        file_id: NAS file link ID (UUID)

    Returns:
        dict: NAS file link record

    Raises:
        HTTPException: 404 if not found
    """
    record = query(
        "SELECT * FROM sale_nas_file_links WHERE id = ?",
        [file_id],
        one=True,
    )

    if not record:
        raise HTTPException(status_code=404, detail="NAS file link not found")

    return record


@router.delete("/{file_id}")
async def delete_nas_file(file_id: str):
    """
    Delete a NAS file link by ID.

    Args:
        file_id: NAS file link ID (UUID)

    Returns:
        dict: Confirmation message with deleted ID

    Raises:
        HTTPException: 404 if not found
    """
    record = query(
        "SELECT * FROM sale_nas_file_links WHERE id = ?",
        [file_id],
        one=True,
    )

    if not record:
        raise HTTPException(status_code=404, detail="NAS file link not found")

    execute(
        "DELETE FROM sale_nas_file_links WHERE id = ?",
        [file_id],
    )

    return {"message": "NAS file link removed", "id": file_id}
