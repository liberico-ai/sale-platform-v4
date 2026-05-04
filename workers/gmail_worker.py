"""Gmail sync worker for IBS HI Sale Platform.

Runs every 5 minutes via APScheduler.
Reads active mailboxes, fetches new emails, classifies them,
matches customers, and auto-creates tasks for high-confidence RFQs.

HARD RULE: RFQ acknowledgments are created as DRAFTS only — never auto-sent.
"""

import json
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional

import structlog

try:
    from ..database import query, execute
    from ..services.gmail_service import GmailService
    from ..services.classifier import classify_email, match_customer
    from ..services.notify import write_notification
except ImportError:
    from database import query, execute
    from services.gmail_service import GmailService
    from services.classifier import classify_email, match_customer
    from services.notify import write_notification

logger = structlog.get_logger(__name__)


def sync_gmail():
    """Sync new emails from Gmail to sale_emails table.

    Process:
    1. Get active mailboxes from sale_monitored_mailboxes
    2. For each mailbox, fetch new messages since last sync
    3. Parse and classify each message
    4. Match sender to customer by domain
    5. Insert to sale_emails table
    6. Auto-create tasks for high-confidence RFQs (confidence > 0.8)
    7. Create DRAFT acknowledgment for RFQs (never auto-send)
    """
    try:
        mailboxes = query("""
            SELECT id, email_address, department, owner_name, last_sync_at
            FROM sale_monitored_mailboxes
            WHERE is_active = 1 AND sync_enabled = 1 AND token_valid = 1
        """)

        if not mailboxes:
            logger.debug("gmail_sync_skip", reason="no_active_mailboxes")
            return

        logger.info("gmail_sync_start", mailbox_count=len(mailboxes))

        # Get all customers for domain matching
        customers = query(
            "SELECT id, email_domain FROM sale_customers WHERE email_domain IS NOT NULL"
        )

        gmail = GmailService()
        total_synced = 0

        for mailbox in mailboxes:
            count = _sync_mailbox(gmail, mailbox, customers)
            total_synced += count

        logger.info("gmail_sync_complete", total_emails=total_synced)

    except Exception as e:
        logger.error("gmail_sync_failed", error=str(e))


def _sync_mailbox(
    gmail: GmailService,
    mailbox: Dict[str, Any],
    customers: List[Dict[str, Any]],
) -> int:
    """Sync single mailbox. Returns number of emails synced."""
    email_address = mailbox["email_address"]
    dept = mailbox.get("department", "SALE")
    owner = mailbox.get("owner_name", "System")

    logger.info("gmail_mailbox_sync", email=email_address)

    try:
        service = gmail.get_service(email_address)
        if not service:
            logger.warning("gmail_auth_skip", email=email_address,
                           reason="token_invalid")
            # Mark token as invalid
            execute(
                "UPDATE sale_monitored_mailboxes SET token_valid = 0 WHERE id = ?",
                [mailbox["id"]]
            )
            return 0

        # Determine sync start
        last_sync = mailbox.get("last_sync_at")
        if not last_sync:
            last_email = query("""
                SELECT MAX(received_at) as ts FROM sale_emails
                WHERE mailbox_email = ?
            """, [email_address], one=True)
            last_sync = (last_email.get("ts") if last_email else None) or "2026-01-01"

        # Fetch messages
        messages = gmail.list_messages(service, after_date=last_sync, max_results=100)
        logger.info("gmail_messages_found",
                     email=email_address,
                     count=len(messages))

        synced = 0
        for msg in messages:
            if _process_message(gmail, service, msg, email_address, dept, owner, customers):
                synced += 1

        # Update sync timestamp
        execute(
            "UPDATE sale_monitored_mailboxes SET last_sync_at = ? WHERE id = ?",
            [datetime.utcnow().isoformat(), mailbox["id"]]
        )

        return synced

    except Exception as e:
        logger.error("gmail_mailbox_error", email=email_address, error=str(e))
        return 0


def _process_message(
    gmail: GmailService,
    service: Any,
    msg: Dict[str, Any],
    email_address: str,
    dept: str,
    owner: str,
    customers: List[Dict[str, Any]],
) -> bool:
    """Process single message. Returns True if successfully synced."""
    msg_id = msg.get("id")

    # Skip if already synced
    existing = query(
        "SELECT id FROM sale_emails WHERE gmail_id = ?",
        [msg_id], one=True
    )
    if existing:
        return False

    # Get full message
    raw_msg = gmail.get_message(service, msg_id)
    if not raw_msg:
        return False

    # Parse
    parsed = gmail.parse_message(raw_msg)

    # Classify
    email_type, confidence = classify_email(parsed)

    # Match customer
    customer_id = match_customer(parsed["from_address"], customers)

    # Insert to database
    email_record_id = str(uuid.uuid4())
    now = datetime.utcnow().isoformat()

    execute("""
        INSERT INTO sale_emails
            (id, gmail_id, thread_id, from_address, from_name,
             to_addresses, cc_addresses, subject, snippet, body_text,
             email_type, classification_confidence,
             has_attachments, attachment_names,
             received_at, synced_at, customer_id,
             mailbox_email, source_dept,
             is_read, is_actioned, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, 0, ?, ?)
    """, [
        email_record_id,
        parsed["gmail_id"], parsed["thread_id"],
        parsed["from_address"], parsed["from_name"],
        json.dumps(parsed["to_addresses"]),
        json.dumps(parsed["cc_addresses"]),
        parsed["subject"], parsed["snippet"], parsed["body_text"],
        email_type, confidence,
        1 if parsed["has_attachments"] else 0,
        json.dumps(parsed["attachment_names"]),
        parsed["received_at"], now,
        customer_id, email_address, dept,
        now, now,
    ])

    logger.info("email_synced",
                email_id=email_record_id,
                type=email_type,
                confidence=confidence,
                from_addr=parsed["from_address"])

    # Auto-actions for high-confidence RFQs
    if email_type == "RFQ" and confidence > 0.8:
        _create_rfq_task(email_record_id, parsed, customer_id, owner)
        _create_rfq_draft(gmail, service, email_record_id, parsed)
        # Notify the mailbox owner that an RFQ landed — they can act
        # immediately even before opening the inbox.
        if owner:
            write_notification(
                notification_type="EMAIL_RFQ",
                title=f"New RFQ: {parsed.get('subject') or '(no subject)'}",
                message=f"From {parsed.get('from_address') or 'unknown'} — task created",
                user_id=owner,
                entity_type="email",
                entity_id=email_record_id,
                severity="INFO",
            )

    # Log email activity
    execute("""
        INSERT INTO sale_email_activity_log
            (id, email_id, action_type, action_by, notes, created_at)
        VALUES (?, ?, 'RECEIVED', 'SYSTEM', ?, ?)
    """, [
        str(uuid.uuid4()), email_record_id,
        f"Auto-classified as {email_type} ({confidence * 100:.0f}%)",
        now
    ])

    return True


def _create_rfq_task(
    email_id: str,
    parsed_email: Dict[str, Any],
    customer_id: Optional[str],
    assigned_to: str,
):
    """Auto-create COST_ESTIMATE task from RFQ email."""
    try:
        task_id = str(uuid.uuid4())
        now = datetime.utcnow().isoformat()
        from_name = parsed_email.get("from_name") or parsed_email["from_address"]

        execute("""
            INSERT INTO sale_tasks
                (id, email_id, task_type, title, description,
                 from_dept, to_dept, assigned_to,
                 status, priority, created_at, updated_at)
            VALUES (?, ?, 'COST_ESTIMATE', ?, ?, 'SALE', 'TCKT', ?, 'PENDING', 'HIGH', ?, ?)
        """, [
            task_id, email_id,
            f"RFQ: {parsed_email['subject'][:100]}",
            f"Prepare quotation for RFQ from {from_name}:\n"
            f"Subject: {parsed_email['subject']}\n\n"
            f"{parsed_email['snippet'][:500]}",
            assigned_to, now, now
        ])

        logger.info("rfq_task_created", task_id=task_id, email_id=email_id)

    except Exception as e:
        logger.error("rfq_task_error", email_id=email_id, error=str(e))


def _create_rfq_draft(
    gmail: GmailService,
    service: Any,
    email_id: str,
    parsed_email: Dict[str, Any],
):
    """Create DRAFT RFQ acknowledgment — NEVER auto-sends.

    Per Hard Rule: all customer-facing emails must be reviewed before sending.
    """
    try:
        from_name = parsed_email.get("from_name", "Valued Customer")
        ack_subject = f"Re: {parsed_email['subject']}"
        ack_body = (
            f"Dear {from_name},\n\n"
            f"Thank you for your inquiry. We have received your RFQ and "
            f"our team is reviewing it carefully.\n\n"
            f"We will provide you with a detailed quotation within "
            f"5 business days.\n\n"
            f"Best regards,\nIBS HI Sales Team"
        )

        draft = gmail.create_draft(
            service,
            parsed_email["from_address"],
            ack_subject,
            ack_body,
            reply_to_id=parsed_email.get("gmail_id"),
        )

        if draft:
            logger.info("rfq_draft_created",
                         email_id=email_id,
                         to=parsed_email["from_address"],
                         draft_id=draft.get("id"))
        else:
            logger.warning("rfq_draft_failed", email_id=email_id)

    except Exception as e:
        logger.error("rfq_draft_error", email_id=email_id, error=str(e))
