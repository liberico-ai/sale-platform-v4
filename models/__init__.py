"""
Pydantic models for IBS HI Sale Platform.
Defines request/response schemas for all entities.
"""

from .enums import (
    OpportunityStage,
    TaskStatus,
    EmailType,
    QuotationStatus,
    FollowUpType,
    FollowUpStatus,
    NotificationType,
    CommissionStatus,
    CustomerStatus,
    ContractStatus,
    SettlementStatus,
    InvoiceStatus,
)
from .customer import CustomerCreate, CustomerUpdate, CustomerResponse
from .opportunity import OpportunityCreate, OpportunityUpdate, OpportunityResponse
from .email import EmailClassify, EmailLinkOpp, EmailResponse
from .task import TaskCreate, TaskUpdate, TaskResponse
from .mailbox import MailboxCreate, MailboxUpdate, MailboxResponse
from .user_role import UserRoleCreate, UserRoleUpdate
from .dashboard import PipelineKPI, TaskStats, EmailStats
from .pm_bridge import PMTaskCreate, DraftReplyRequest
from .contact import (
    CustomerContactCreate,
    CustomerContactUpdate,
    CustomerContactResponse,
)
from .interaction import (
    CustomerInteractionCreate,
    CustomerInteractionUpdate,
    CustomerInteractionResponse,
)
from .quotation import (
    QuotationCreate,
    QuotationUpdate,
    QuotationRevise,
    QuotationResponse,
    QuotationHistoryResponse,
    QuotationRevisionResponse,
)
from .contract import (
    ActiveContractResponse,
    ContractMilestoneResponse,
    SettlementResponse,
    ChangeOrderResponse,
)
from .intelligence import MarketSignalResponse, ProductOpportunityResponse

__all__ = [
    # Enums
    "OpportunityStage",
    "TaskStatus",
    "EmailType",
    "QuotationStatus",
    "FollowUpType",
    "FollowUpStatus",
    "NotificationType",
    "CommissionStatus",
    "CustomerStatus",
    "ContractStatus",
    "SettlementStatus",
    "InvoiceStatus",
    # Customer
    "CustomerCreate",
    "CustomerUpdate",
    "CustomerResponse",
    "OpportunityCreate",
    "OpportunityUpdate",
    "OpportunityResponse",
    "EmailClassify",
    "EmailLinkOpp",
    "EmailResponse",
    "TaskCreate",
    "TaskUpdate",
    "TaskResponse",
    "MailboxCreate",
    "MailboxUpdate",
    "MailboxResponse",
    "UserRoleCreate",
    "UserRoleUpdate",
    "PipelineKPI",
    "TaskStats",
    "EmailStats",
    "PMTaskCreate",
    "DraftReplyRequest",
    "CustomerContactCreate",
    "CustomerContactUpdate",
    "CustomerContactResponse",
    "CustomerInteractionCreate",
    "CustomerInteractionUpdate",
    "CustomerInteractionResponse",
    "QuotationCreate",
    "QuotationUpdate",
    "QuotationRevise",
    "QuotationResponse",
    "QuotationHistoryResponse",
    "QuotationRevisionResponse",
    "ActiveContractResponse",
    "ContractMilestoneResponse",
    "SettlementResponse",
    "ChangeOrderResponse",
    "MarketSignalResponse",
    "ProductOpportunityResponse",
]
