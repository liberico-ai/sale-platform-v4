"""Files Router — sale_nas_file_links (1,112 records).

NAS-stored documents indexed via polymorphic FK (entity_type + entity_id).
Common entity_types: customer, opportunity, contract, milestone, project_code.
"""

import uuid
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel

import structlog

try:
    from ..database import query, execute
    from ..auth import require_write
except ImportError:
    from database import query, execute
    from auth import require_write

logger = structlog.get_logger(__name__)

router = APIRouter(prefix="/files", tags=["Files"])


class FileLinkCreate(BaseModel):
    """New NAS file link.

    Required: nas_path, entity_type, entity_id.
    file_type values: QUOTATION | CONTRACT | DRAWING | REPORT | INVOICE | OTHER.
    """
    nas_path: str
    entity_type: str           # customer | opportunity | contract | milestone | project_code
    entity_id: str
    file_name: Optional[str] = None
    file_type: Optional[str] = None
    description: Optional[str] = None


@router.get("")
async def list_files(
    entity_type: Optional[str] = Query(None),
    entity_id: Optional[str] = Query(None),
    file_type: Optional[str] = Query(None),
    customer_id: Optional[str] = Query(
        None,
        description="Convenience filter — equivalent to entity_type=customer&entity_id={customer_id}",
    ),
    opportunity_id: Optional[str] = Query(None),
    project_code: Optional[str] = Query(None),
    q: Optional[str] = Query(None, description="Free-text search over nas_path / file_name / description"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    """List NAS file links with composable filters."""
    where = []
    params: list = []

    if entity_type:
        where.append("entity_type = ?")
        params.append(entity_type)
    if entity_id:
        where.append("entity_id = ?")
        params.append(entity_id)
    if file_type:
        where.append("file_type = ?")
        params.append(file_type)
    if customer_id:
        where.append("(entity_type = 'customer' AND entity_id = ?)")
        params.append(customer_id)
    if opportunity_id:
        where.append("(entity_type = 'opportunity' AND entity_id = ?)")
        params.append(opportunity_id)
    if project_code:
        where.append("(entity_type = 'project_code' AND entity_id = ?)")
        params.append(project_code)
    if q:
        where.append("(nas_path LIKE ? OR file_name LIKE ? OR description LIKE ?)")
        like = f"%{q}%"
        params.extend([like, like, like])

    where_sql = " AND ".join(where) if where else "1=1"

    total = query(
        f"SELECT COUNT(*) as cnt FROM sale_nas_file_links WHERE {where_sql}",
        params,
    )[0]["cnt"]

    items = query(
        f"""
        SELECT * FROM sale_nas_file_links
        WHERE {where_sql}
        ORDER BY created_at DESC
        LIMIT ? OFFSET ?
        """,
        params + [limit, offset],
    )

    return {"total": total, "items": items, "limit": limit, "offset": offset}


@router.get("/{file_id}")
async def get_file(file_id: str):
    """Single NAS file link."""
    item = query(
        "SELECT * FROM sale_nas_file_links WHERE id = ?",
        [file_id],
        one=True,
    )
    if not item:
        raise HTTPException(status_code=404, detail="File link not found")
    return {"file": dict(item)}


@router.post("", dependencies=[Depends(require_write)])
async def create_file_link(payload: FileLinkCreate):
    """Index a new NAS file link.

    Validates that entity_id exists in the corresponding table when
    entity_type is one of the canonical FK targets.
    """
    if payload.entity_type == "customer":
        cust = query(
            "SELECT id FROM sale_customers WHERE id = ?",
            [payload.entity_id], one=True,
        )
        if not cust:
            raise HTTPException(status_code=404, detail="Customer not found")
    elif payload.entity_type == "opportunity":
        opp = query(
            "SELECT id FROM sale_opportunities WHERE id = ?",
            [payload.entity_id], one=True,
        )
        if not opp:
            raise HTTPException(status_code=404, detail="Opportunity not found")
    elif payload.entity_type == "contract":
        ct = query(
            "SELECT id FROM sale_active_contracts WHERE id = ?",
            [payload.entity_id], one=True,
        )
        if not ct:
            raise HTTPException(status_code=404, detail="Contract not found")
    # Other entity_types (project_code, milestone, freeform) — no FK check.

    file_id = str(uuid.uuid4())
    now = datetime.now().isoformat()

    file_name = payload.file_name
    if not file_name and payload.nas_path:
        # Pull tail of NAS path as fallback display name
        file_name = payload.nas_path.replace("\\", "/").rstrip("/").split("/")[-1]

    execute(
        """
        INSERT INTO sale_nas_file_links
            (id, entity_type, entity_id, nas_path, file_name, file_type,
             description, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [
            file_id, payload.entity_type, payload.entity_id,
            payload.nas_path, file_name, payload.file_type,
            payload.description, now,
        ],
    )

    logger.info(
        "file_link_created",
        file_id=file_id,
        entity_type=payload.entity_type,
        entity_id=payload.entity_id,
    )

    return {
        "id": file_id,
        "entity_type": payload.entity_type,
        "entity_id": payload.entity_id,
        "file_name": file_name,
        "status": "ok",
    }


@router.delete("/{file_id}", dependencies=[Depends(require_write)])
async def delete_file_link(file_id: str):
    """Remove a NAS file link. Does NOT delete the file on the NAS itself."""
    existing = query(
        "SELECT id FROM sale_nas_file_links WHERE id = ?",
        [file_id], one=True,
    )
    if not existing:
        raise HTTPException(status_code=404, detail="File link not found")

    execute("DELETE FROM sale_nas_file_links WHERE id = ?", [file_id])
    logger.info("file_link_deleted", file_id=file_id)
    return {"id": file_id, "status": "deleted"}
