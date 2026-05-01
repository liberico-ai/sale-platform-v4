"""Main FastAPI application for IBS HI Sale Platform Phase 1.

Handles Email + Pipeline + Task management with PM integration.
"""

import os

import structlog
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from apscheduler.schedulers.background import BackgroundScheduler

logger = structlog.get_logger(__name__)

# Support both module and direct execution
try:
    from . import config
    from .database import init_db, close_db_connection, close_all_connections
    from .auth import require_auth, require_write, require_admin
    from .routers import (
        health, auth_router,
        customers, opportunities, emails, tasks,
        dashboard, mailboxes, users, pm_integration,
        contracts, intelligence,
        contacts, quotations, interactions,
        follow_ups, files, notifications, search,
        inter_dept, commissions, reports, templates,
    )
except ImportError:
    import config
    from database import init_db, close_db_connection, close_all_connections
    from auth import require_auth, require_write, require_admin
    from routers import (
        health, auth_router,
        customers, opportunities, emails, tasks,
        dashboard, mailboxes, users, pm_integration,
        contracts, intelligence,
        contacts, quotations, interactions,
        follow_ups, files, notifications, search,
        inter_dept, commissions, reports, templates,
    )

# Initialize scheduler (placeholder for now)
scheduler = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI lifespan context manager for startup and shutdown."""
    # Startup
    logger.info("platform_starting", port=config.SALE_PORT)

    # Initialize database
    db_ok = init_db()
    if not db_ok:
        logger.warning("database_init_issues")

    # Warn if running with dev fallback key
    if "dev-key-local-only" in config.API_KEYS:
        logger.warning("using_dev_api_key",
                        msg="Running with dev fallback key. Set API keys via env vars for production.")

    # Initialize scheduler with worker jobs
    if config.ENABLE_TASK_SCHEDULING:
        global scheduler
        scheduler = BackgroundScheduler()

        # Import workers
        try:
            from .workers.gmail_worker import sync_gmail
            from .workers.sla_worker import check_sla
            from .workers.stale_worker import detect_stale_deals
            from .workers.followup_worker import check_followups
        except ImportError:
            from workers.gmail_worker import sync_gmail
            from workers.sla_worker import check_sla
            from workers.stale_worker import detect_stale_deals
            from workers.followup_worker import check_followups

        # Gmail sync — every 5 minutes (if email sync enabled)
        if config.ENABLE_EMAIL_SYNC:
            scheduler.add_job(
                sync_gmail, "interval", minutes=5,
                id="gmail_sync", name="Gmail Sync",
                max_instances=1, replace_existing=True,
            )
            logger.info("worker_registered", worker="gmail_sync", interval="5min")

        # SLA check — every 15 minutes
        scheduler.add_job(
            check_sla, "interval", minutes=15,
            id="sla_check", name="SLA Check",
            max_instances=1, replace_existing=True,
        )
        logger.info("worker_registered", worker="sla_check", interval="15min")

        # Stale deal detection — daily at 8:00 AM
        scheduler.add_job(
            detect_stale_deals, "cron", hour=8, minute=0,
            id="stale_detection", name="Stale Deal Detection",
            max_instances=1, replace_existing=True,
        )
        logger.info("worker_registered", worker="stale_detection", schedule="daily_08:00")

        # Follow-up reminders — daily at 7:00 AM
        scheduler.add_job(
            check_followups, "cron", hour=7, minute=0,
            id="followup_check", name="Follow-up Reminders",
            max_instances=1, replace_existing=True,
        )
        logger.info("worker_registered", worker="followup_check", schedule="daily_07:00")

        scheduler.start()
        logger.info("scheduler_started", job_count=len(scheduler.get_jobs()))

    logger.info("platform_ready",
                host=config.API_HOST,
                port=config.SALE_PORT,
                db_type=config.DB_TYPE)

    yield

    # Shutdown
    logger.info("platform_shutting_down")

    # Stop scheduler
    if scheduler and scheduler.running:
        scheduler.shutdown()
        logger.info("scheduler_stopped")

    # Close database connections and pool
    close_all_connections()
    logger.info("database_closed")


# Create FastAPI app
app = FastAPI(
    title="IBS HI Sale Platform",
    version="1.0.0",
    description="Sale Platform Phase 1 — Email + Pipeline + Task Management",
    lifespan=lifespan
)

# Add CORS middleware
# Production: set CORS_ORIGINS env var (comma-separated)
# Development: defaults to allow all origins
_cors_origins_str = os.getenv("CORS_ORIGINS", "*")
if _cors_origins_str == "*":
    _cors_origins = ["*"]
else:
    _cors_origins = [o.strip() for o in _cors_origins_str.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define dependency shortcuts
auth_dep = [Depends(require_auth)]
write_dep = [Depends(require_write)]
admin_dep = [Depends(require_admin)]


# ═══════════════════════════════════════════════════════════════
# ROUTER REGISTRATION
# ═══════════════════════════════════════════════════════════════

# Public endpoints (no auth required)
app.include_router(health.router)

# Auth introspection — own auth check inside the route
app.include_router(auth_router.router, prefix="/api/v1")

# Read-access endpoints (any valid API key)
app.include_router(customers.router, prefix="/api/v1", dependencies=auth_dep)
app.include_router(opportunities.router, prefix="/api/v1", dependencies=auth_dep)
app.include_router(emails.router, prefix="/api/v1", dependencies=auth_dep)
app.include_router(tasks.router, prefix="/api/v1", dependencies=auth_dep)
app.include_router(dashboard.router, prefix="/api/v1", dependencies=auth_dep)
app.include_router(contracts.router, prefix="/api/v1", dependencies=auth_dep)
app.include_router(intelligence.router, prefix="/api/v1", dependencies=auth_dep)
app.include_router(contacts.router, prefix="/api/v1", dependencies=auth_dep)
app.include_router(quotations.router, prefix="/api/v1", dependencies=auth_dep)
app.include_router(interactions.router, prefix="/api/v1", dependencies=auth_dep)
app.include_router(follow_ups.router, prefix="/api/v1", dependencies=auth_dep)
app.include_router(files.router, prefix="/api/v1", dependencies=auth_dep)
app.include_router(notifications.router, prefix="/api/v1", dependencies=auth_dep)
app.include_router(search.router, prefix="/api/v1", dependencies=auth_dep)
app.include_router(inter_dept.router, prefix="/api/v1", dependencies=auth_dep)
app.include_router(commissions.router, prefix="/api/v1", dependencies=auth_dep)
app.include_router(reports.router, prefix="/api/v1", dependencies=auth_dep)
app.include_router(templates.router, prefix="/api/v1", dependencies=auth_dep)

# Write-access endpoints (ADMIN or MANAGER key)
app.include_router(mailboxes.router, prefix="/api/v1", dependencies=write_dep)
app.include_router(users.router, prefix="/api/v1", dependencies=write_dep)

# PM integration (read access, writes internally validated)
app.include_router(pm_integration.router, prefix="/api/v1", dependencies=auth_dep)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=config.API_HOST,
        port=config.SALE_PORT,
        reload=True,
        log_level=config.LOG_LEVEL.lower(),
    )
