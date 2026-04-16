"""IBS HI Sale Platform v4 - Workers module.

Background workers run on scheduled intervals via APScheduler:
- gmail_worker: Sync Gmail every 5 minutes
- sla_worker: Check SLA + escalate every 15 minutes
- stale_worker: Detect stale deals daily at 8:00 AM
- pm_sync_worker: Poll PM changes every 10 minutes
"""

from .gmail_worker import sync_gmail
from .sla_worker import check_sla, get_sla_report
from .stale_worker import detect_stale_deals, reactivate_deal

# pm_sync_worker imported separately when PM integration is enabled
# from .pm_sync_worker import sync_from_pm

__all__ = [
    "sync_gmail",
    "check_sla",
    "get_sla_report",
    "detect_stale_deals",
    "reactivate_deal",
]
