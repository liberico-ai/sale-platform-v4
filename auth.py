"""Authentication module for IBS HI Sale Platform.

Implements X-API-Key based 3-tier authorization (ADMIN, MANAGER, VIEWER)
plus a per-user identity layer backed by ``sale_user_roles.api_key``.

The legacy ``require_auth / require_write / require_admin`` dependencies
still return the tier string so existing routers keep working unchanged.
New code should depend on :func:`get_current_user` to receive the full
``UserContext`` (tier + linked user row, when one exists) so audit logs
can record the actual operator instead of ``None``.
"""

from dataclasses import dataclass
from typing import Optional

from fastapi import HTTPException, Header, Request

import structlog

logger = structlog.get_logger(__name__)

# Support both module and direct execution
try:
    from . import config
    from .database import query
except ImportError:
    import config
    from database import query


@dataclass
class UserContext:
    """Resolved auth context for the current request.

    ``key_tier`` always reflects the tier from ``config.API_KEYS``.
    The remaining fields are populated when the X-API-Key matches a row
    in ``sale_user_roles`` (via the ``api_key`` column). For dev/legacy
    keys with no linked user, they stay ``None`` and the API still
    works — just without per-user audit attribution.
    """

    key_tier: str
    user_id: Optional[str] = None
    user_email: Optional[str] = None
    user_name: Optional[str] = None
    department: Optional[str] = None

    @property
    def is_authenticated_user(self) -> bool:
        return self.user_id is not None

    @property
    def actor(self) -> str:
        """String suitable for audit_log.changed_by — prefers user_id."""
        return self.user_id or f"key:{self.key_tier}"


def _resolve_tier(api_key: str) -> Optional[str]:
    if not api_key:
        return None
    return config.API_KEYS.get(api_key)


# Map sale_user_roles.role → API tier name used by config.API_KEYS.
_ROLE_TO_TIER = {
    "ADMIN": "ADMIN",
    "MANAGER": "MANAGER",
    "MEMBER": "VIEWER",  # MEMBER is the read-only baseline
}


def sync_user_api_keys() -> int:
    """Merge ``sale_user_roles.api_key`` rows into ``config.API_KEYS``.

    Called once at startup so DB-defined per-user keys are accepted by
    the existing tier-based auth dependencies. Idempotent — safe to call
    multiple times. Returns the number of keys synced.
    """
    try:
        rows = query(
            """
            SELECT api_key, role, user_name
            FROM sale_user_roles
            WHERE api_key IS NOT NULL AND is_active = 1
            """
        )
    except Exception as e:
        logger.warning("user_key_sync_skipped", error=str(e))
        return 0

    count = 0
    for row in rows:
        key = row.get("api_key")
        role = (row.get("role") or "").upper()
        tier = _ROLE_TO_TIER.get(role, "VIEWER")
        if not key:
            continue
        config.API_KEYS[key] = tier
        config.API_KEY_LABELS[key] = f"{tier} ({row.get('user_name')})"
        count += 1

    if count:
        logger.info("user_api_keys_synced", count=count)
    return count


def _resolve_user(api_key: str) -> Optional[dict]:
    """Look up the sale_user_roles row linked to ``api_key``.

    Returns ``None`` when the column is missing (legacy DB, pre-migration)
    or no row matches. Never raises.
    """
    if not api_key:
        return None
    try:
        return query(
            """
            SELECT id, user_name, email, department, role
            FROM sale_user_roles
            WHERE api_key = ? AND is_active = 1
            LIMIT 1
            """,
            [api_key],
            one=True,
        )
    except Exception as e:
        # Old DBs without the api_key column — fall through silently.
        logger.debug("user_lookup_failed", error=str(e))
        return None


async def require_auth(x_api_key: Optional[str] = Header(None)) -> str:
    """Dependency: Require any valid API key (ADMIN, MANAGER, or VIEWER).

    Returns the tier string for backwards compatibility. New code should
    prefer :func:`get_current_user`.
    """
    if not x_api_key:
        raise HTTPException(status_code=401, detail="Missing X-API-Key header")

    tier = _resolve_tier(x_api_key)
    if not tier:
        logger.warning("auth_failed", reason="invalid_key")
        raise HTTPException(status_code=401, detail="Invalid API key")

    return tier


async def require_write(x_api_key: Optional[str] = Header(None)) -> str:
    """Dependency: Require ADMIN or MANAGER tier API key (write access)."""
    tier = await require_auth(x_api_key)

    if tier not in ["ADMIN", "MANAGER"]:
        logger.warning("auth_insufficient", required="ADMIN|MANAGER", got=tier)
        raise HTTPException(
            status_code=403,
            detail=f"Insufficient permissions. Required: ADMIN or MANAGER, got: {tier}"
        )

    return tier


async def require_admin(x_api_key: Optional[str] = Header(None)) -> str:
    """Dependency: Require ADMIN tier API key (admin-only access)."""
    tier = await require_auth(x_api_key)

    if tier != "ADMIN":
        logger.warning("auth_insufficient", required="ADMIN", got=tier)
        raise HTTPException(
            status_code=403,
            detail=f"Admin access required. You have: {tier}"
        )

    return tier


async def get_current_user(request: Request) -> UserContext:
    """Dependency: Resolve full UserContext from the X-API-Key header.

    Routers that need per-user audit attribution depend on this instead of
    ``require_auth``. Validates the key (401 if invalid) and looks up the
    linked ``sale_user_roles`` row when one exists.
    """
    api_key = request.headers.get("X-API-Key", "")
    if not api_key:
        raise HTTPException(status_code=401, detail="Missing X-API-Key header")

    tier = _resolve_tier(api_key)
    if not tier:
        logger.warning("auth_failed", reason="invalid_key")
        raise HTTPException(status_code=401, detail="Invalid API key")

    user = _resolve_user(api_key)
    if user:
        return UserContext(
            key_tier=tier,
            user_id=user["id"],
            user_email=user.get("email"),
            user_name=user.get("user_name"),
            department=user.get("department"),
        )

    return UserContext(key_tier=tier)


async def get_current_writer(request: Request) -> UserContext:
    """Same as :func:`get_current_user` but enforces write tier."""
    user = await get_current_user(request)
    if user.key_tier not in ("ADMIN", "MANAGER"):
        raise HTTPException(
            status_code=403,
            detail=f"Insufficient permissions. Required: ADMIN or MANAGER, got: {user.key_tier}",
        )
    return user


async def get_current_admin(request: Request) -> UserContext:
    """Same as :func:`get_current_user` but enforces admin tier."""
    user = await get_current_user(request)
    if user.key_tier != "ADMIN":
        raise HTTPException(
            status_code=403,
            detail=f"Admin access required. You have: {user.key_tier}",
        )
    return user
