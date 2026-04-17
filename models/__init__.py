"""
Pydantic models for IBS HI Sale Platform.
Defines request/response schemas for all entities.
"""

from .customer import CustomerCreate, CustomerUpdate
from .opportunity import OpportunityCreate, OpportunityUpdate
from .email import EmailClassify, EmailLinkOpp
from .task import TaskCreate, TaskUpdate
from .mailbox import MailboxCreate, MailboxUpdate
from .user_role import UserRoleCreate, UserRoleUpdate
from .dashboard import PipelineKPI, TaskStats, EmailStats
from .pm_bridge import PMTaskCreate, DraftReplyRequest
from .nas_file import NasFileCreate, NasFileResponse

__all__ = [
    "CustomerCreate",
    "CustomerUpdate",
    "OpportunityCreate",
    "OpportunityUpdate",
    "EmailClassify",
    "EmailLinkOpp",
    "TaskCreate",
    "TaskUpdate",
    "MailboxCreate",
    "MailboxUpdate",
    "UserRoleCreate",
    "UserRoleUpdate",
    "PipelineKPI",
    "TaskStats",
    "EmailStats",
    "PMTaskCreate",
    "DraftReplyRequest",
    "NasFileCreate",
    "NasFileResponse",
]
