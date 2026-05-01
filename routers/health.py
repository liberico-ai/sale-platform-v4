"""
Health Check Router
Provides system health status and version information.
"""

from fastapi import APIRouter

try:
    from .. import config
except ImportError:
    import config

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health_check():
    """
    Health check endpoint - returns system status and configuration.
    
    Returns:
        dict: Status information including version and database type.
    """
    return {
        "status": "ok",
        "version": "1.0.0",
        "db_type": config.DB_TYPE,
    }
