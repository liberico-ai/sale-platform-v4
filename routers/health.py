"""
Health Check Router
Provides system health status and version information.
"""

from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from .. import config

router = APIRouter(tags=["Health"])


@router.get("/")
async def root():
    """Redirect to dashboard UI."""
    return RedirectResponse(url="/static/index.html")


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
