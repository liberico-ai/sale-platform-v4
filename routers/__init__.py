"""
IBS HI Sale Platform - Router Module
Router initialization and exports for all API endpoints.
"""

from . import health
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

__all__ = [
    "health",
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
]
