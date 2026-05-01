"""
IBS HI Sale Platform - Router Module
Router initialization and exports for all API endpoints.
"""

from . import health
from . import auth_router
from . import customers
from . import opportunities
from . import emails
from . import tasks
from . import dashboard
from . import mailboxes
from . import users
from . import pm_integration
from . import contracts
from . import intelligence
from . import contacts
from . import quotations
from . import interactions
from . import follow_ups
from . import files
from . import notifications
from . import search
from . import inter_dept
from . import commissions
from . import reports
from . import templates
from . import io_router

__all__ = [
    "health",
    "auth_router",
    "customers",
    "opportunities",
    "emails",
    "tasks",
    "dashboard",
    "mailboxes",
    "users",
    "pm_integration",
    "contracts",
    "intelligence",
    "contacts",
    "quotations",
    "interactions",
    "follow_ups",
    "files",
    "notifications",
    "search",
    "inter_dept",
    "commissions",
    "reports",
    "templates",
    "io_router",
]
