"""
Users Router
Manages platform users, roles, departments, and user lifecycle (onboard/offboard).
"""

from fastapi import APIRouter, Query, HTTPException
from typing import Optional
from pydantic import BaseModel
from ..database import query, execute
from datetime import datetime
import uuid

router = APIRouter(prefix="/users", tags=["Users"])


class UserCreate(BaseModel):
    """Model for creating a new user."""
    user_name: str
    email: str
    department: str
    role: str = "MEMBER"
    permissions: Optional[list] = None


class UserUpdate(BaseModel):
    """Model for updating a user."""
    role: Optional[str] = None
    department: Optional[str] = None
    is_active: Optional[bool] = None
    deactivated_at: Optional[str] = None


@router.get("")
async def list_users(
    department: Optional[str] = Query(None, description="Filter by department"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    """
    List platform users with their roles and departments.
    Supports filtering by department and active status.
    
    Args:
        department: Optional department filter (SALE, KTKH, KT, QLDA, SX, TCKT, QAQC)
        is_active: Optional active status filter
        limit: Number of results to return (1-200)
        offset: Number of results to skip
        
    Returns:
        dict: Total count, items list, limit, and offset
    """
    where = []
    params = []
    
    if department:
        where.append("department = ?")
        params.append(department)
    
    if is_active is not None:
        where.append("is_active = ?")
        params.append(1 if is_active else 0)
    
    where_sql = " AND ".join(where) if where else "1=1"
    
    total = query(
        f"SELECT COUNT(*) as cnt FROM sale_user_roles WHERE {where_sql}",
        params
    )[0]["cnt"]
    
    items = query(f"""
        SELECT id, user_name, email, department, role, is_active, 
               joined_at, deactivated_at, created_at, updated_at
        FROM sale_user_roles
        WHERE {where_sql}
        ORDER BY created_at DESC
        LIMIT ? OFFSET ?
    """, params + [limit, offset])
    
    return {"total": total, "items": items, "limit": limit, "offset": offset}


@router.post("")
async def add_user(user: UserCreate):
    """
    Add a new user and onboard to the platform.
    
    Args:
        user: User creation data (user_name, email, department, role)
        
    Returns:
        dict: Created user ID and status
    """
    user_id = str(uuid.uuid4())
    now = datetime.now().isoformat()
    
    # Check if user already exists
    existing = query(
        "SELECT * FROM sale_user_roles WHERE email = ?",
        [user.email],
        one=True
    )
    
    if existing:
        raise HTTPException(status_code=409, detail="User already exists")
    
    permissions_json = None
    if user.permissions:
        import json
        permissions_json = json.dumps(user.permissions)
    
    execute("""
        INSERT INTO sale_user_roles
            (id, user_name, email, department, role, permissions, is_active,
             joined_at, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, 1, ?, ?, ?)
    """, [user_id, user.user_name, user.email, user.department, user.role,
          permissions_json, now, now, now])
    
    return {
        "id": user_id,
        "email": user.email,
        "name": user.user_name,
        "role": user.role,
        "department": user.department,
        "status": "ok",
        "message": f"User onboarded: {user.user_name}"
    }


@router.patch("/{user_id}")
async def update_user(user_id: str, update: UserUpdate):
    """
    Update user role, department, or deactivate (offboard).
    
    Args:
        user_id: User ID (UUID)
        update: Update data (role, department, is_active, deactivated_at)
        
    Returns:
        dict: Updated user ID and status
        
    Raises:
        HTTPException: 404 if user not found
    """
    existing = query(
        "SELECT * FROM sale_user_roles WHERE id = ?",
        [user_id],
        one=True
    )
    
    if not existing:
        raise HTTPException(status_code=404, detail="User not found")
    
    sets = []
    params = []
    
    if update.role is not None:
        sets.append("role = ?")
        params.append(update.role)
    
    if update.department is not None:
        sets.append("department = ?")
        params.append(update.department)
    
    if update.is_active is not None:
        sets.append("is_active = ?")
        params.append(1 if update.is_active else 0)
        
        # If deactivating, set deactivated_at
        if not update.is_active and update.deactivated_at is None:
            sets.append("deactivated_at = ?")
            params.append(datetime.now().isoformat())
    
    if update.deactivated_at is not None:
        sets.append("deactivated_at = ?")
        params.append(update.deactivated_at)
    
    sets.append("updated_at = ?")
    params.append(datetime.now().isoformat())
    params.append(user_id)
    
    execute(f"UPDATE sale_user_roles SET {', '.join(sets)} WHERE id = ?", params)
    
    return {"id": user_id, "status": "ok"}
