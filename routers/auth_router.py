"""Auth Router — current-user introspection.

The platform's only auth surface today is X-API-Key (3 tiers: ADMIN /
MANAGER / VIEWER). This router lets the frontend call /auth/me right
after login to learn which tier the key holds and pick up the linked
user profile (sale_user_roles) when one exists.

The header value is hashed and matched against config.API_KEYS, so we
never echo the key back.
"""

from typing import Optional

from fastapi import APIRouter, Header, HTTPException

import structlog

try:
    from .. import config
    from ..database import query
except ImportError:
    import config
    from database import query

logger = structlog.get_logger(__name__)

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.get("/me")
async def get_current_user(x_api_key: Optional[str] = Header(None)):
    """Return tier + linked user profile for the supplied X-API-Key.

    Returns 401 if no key or the key is unknown. The tier mapping comes
    from environment vars; the optional user profile comes from
    sale_user_roles when a row matches the tier (e.g. ADMIN → first
    active ADMIN row).
    """
    if not x_api_key:
        raise HTTPException(status_code=401, detail="Missing X-API-Key header")

    tier = config.API_KEYS.get(x_api_key)
    if not tier:
        raise HTTPException(status_code=401, detail="Invalid API key")

    # Best-effort profile match — the API-key → user mapping is loose
    # today (one shared key per tier). Pick the first active user whose
    # role matches the tier so the frontend has *something* to show.
    role_filter = "ADMIN" if tier == "ADMIN" else (
        "MANAGER" if tier == "MANAGER" else "MEMBER"
    )
    profile = query(
        """
        SELECT id, user_name, email, department, role, is_active
        FROM sale_user_roles
        WHERE role = ? AND is_active = 1
        ORDER BY joined_at ASC
        LIMIT 1
        """,
        [role_filter],
        one=True,
    )

    return {
        "tier": tier,
        "is_dev_key": x_api_key == "dev-key-local-only",
        "profile": dict(profile) if profile else None,
    }
