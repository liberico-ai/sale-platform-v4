"""Authentication module for IBS HI Sale Platform.

Implements X-API-Key based 3-tier authorization (ADMIN, MANAGER, VIEWER).
"""

from fastapi import HTTPException, Header
from typing import Optional

import structlog

logger = structlog.get_logger(__name__)

# Support both module and direct execution
try:
    from . import config
except ImportError:
    import config


async def require_auth(x_api_key: Optional[str] = Header(None)) -> str:
    """Dependency: Require any valid API key (ADMIN, MANAGER, or VIEWER).

    Args:
        x_api_key: API key from X-API-Key header.

    Returns:
        API key tier (ADMIN, MANAGER, or VIEWER).

    Raises:
        HTTPException: 401 if no key provided or invalid key.
    """
    if not x_api_key:
        raise HTTPException(status_code=401, detail="Missing X-API-Key header")

    tier = config.API_KEYS.get(x_api_key)
    if not tier:
        logger.warning("auth_failed", reason="invalid_key")
        raise HTTPException(status_code=401, detail="Invalid API key")

    return tier


async def require_write(x_api_key: Optional[str] = Header(None)) -> str:
    """Dependency: Require ADMIN or MANAGER tier API key (write access).

    Args:
        x_api_key: API key from X-API-Key header.

    Returns:
        API key tier (ADMIN or MANAGER).

    Raises:
        HTTPException: 401 if no key provided or invalid key.
        HTTPException: 403 if key is VIEWER tier.
    """
    tier = await require_auth(x_api_key)

    if tier not in ["ADMIN", "MANAGER"]:
        logger.warning("auth_insufficient", required="ADMIN|MANAGER", got=tier)
        raise HTTPException(
            status_code=403,
            detail=f"Insufficient permissions. Required: ADMIN or MANAGER, got: {tier}"
        )

    return tier


async def require_admin(x_api_key: Optional[str] = Header(None)) -> str:
    """Dependency: Require ADMIN tier API key (admin-only access).

    Args:
        x_api_key: API key from X-API-Key header.

    Returns:
        API key tier (ADMIN).

    Raises:
        HTTPException: 401 if no key provided or invalid key.
        HTTPException: 403 if key is not ADMIN tier.
    """
    tier = await require_auth(x_api_key)

    if tier != "ADMIN":
        logger.warning("auth_insufficient", required="ADMIN", got=tier)
        raise HTTPException(
            status_code=403,
            detail=f"Admin access required. You have: {tier}"
        )

    return tier
