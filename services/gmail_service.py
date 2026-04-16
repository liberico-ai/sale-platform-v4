"""Gmail API wrapper for IBS HI Sale Platform.

Handles OAuth 2.0 authentication, message listing, parsing, and sending.
Tokens stored per-mailbox in tokens/{email}/ directory.

HARD RULE: send_message() creates DRAFT only — never auto-sends to customers.
"""

import base64
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Any

import structlog

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

logger = structlog.get_logger(__name__)

# Gmail API scopes
SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.modify",
]


class GmailService:
    """Gmail API wrapper with OAuth 2.0 flow and per-mailbox token storage."""

    def __init__(
        self,
        credentials_path: Optional[str] = None,
        tokens_dir: Optional[str] = None,
    ):
        """Initialize Gmail service.

        Args:
            credentials_path: Path to Google OAuth credentials JSON file.
            tokens_dir: Directory to store per-mailbox tokens.
        """
        try:
            from . import config
        except ImportError:
            import config

        self.credentials_path = credentials_path or config.GMAIL_CREDENTIALS_PATH
        self.tokens_dir = Path(tokens_dir or config.GMAIL_TOKENS_DIR)
        self.tokens_dir.mkdir(parents=True, exist_ok=True)

    def authenticate(self, email_address: str) -> Optional[Credentials]:
        """Authenticate user via OAuth 2.0 flow.

        Args:
            email_address: Email address to authenticate.

        Returns:
            Authenticated Credentials object, or None if auth fails.
        """
        token_file = self.tokens_dir / f"{email_address}.json"

        try:
            # Check for existing token
            if token_file.exists():
                creds = Credentials.from_authorized_user_file(str(token_file), SCOPES)
                if creds and creds.valid:
                    return creds
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                    with open(token_file, "w") as f:
                        f.write(creds.to_json())
                    logger.info("gmail_token_refreshed", email=email_address)
                    return creds

            # Create new token via OAuth flow (requires user interaction)
            if not os.path.exists(self.credentials_path):
                logger.error("gmail_credentials_missing",
                             path=self.credentials_path)
                return None

            flow = InstalledAppFlow.from_client_secrets_file(
                self.credentials_path, SCOPES
            )
            creds = flow.run_local_server(port=0)

            # Save token
            with open(token_file, "w") as f:
                f.write(creds.to_json())
            logger.info("gmail_token_created", email=email_address)

            return creds
        except Exception as e:
            logger.error("gmail_auth_failed", email=email_address, error=str(e))
            return None

    def get_service(self, email_address: str) -> Optional[Any]:
        """Get authenticated Gmail API service for a mailbox.

        Args:
            email_address: Email address to authenticate.

        Returns:
            Gmail API service object, or None if auth fails.
        """
        creds = self.authenticate(email_address)
        if not creds:
            return None
        return build("gmail", "v1", credentials=creds)

    def list_messages(
        self,
        service: Any,
        after_date: Optional[str] = None,
        max_results: int = 100,
    ) -> List[Dict[str, Any]]:
        """List new messages from Gmail.

        Args:
            service: Gmail API service object.
            after_date: ISO format date string.
            max_results: Max messages to return.

        Returns:
            List of message objects with ID and thread ID.
        """
        try:
            q = "is:unread"
            if after_date:
                q += f' after:{after_date.split("T")[0].replace("-", "/")}'

            results = service.users().messages().list(
                userId="me", q=q, maxResults=max_results
            ).execute()

            return results.get("messages", [])
        except HttpError as error:
            logger.error("gmail_list_error", error=str(error))
            return []

    def get_message(self, service: Any, msg_id: str) -> Optional[Dict[str, Any]]:
        """Get full message content.

        Args:
            service: Gmail API service object.
            msg_id: Message ID.

        Returns:
            Full message object or None if error.
        """
        try:
            message = service.users().messages().get(
                userId="me", id=msg_id, format="full"
            ).execute()
            return message
        except HttpError as error:
            logger.error("gmail_get_error", msg_id=msg_id, error=str(error))
            return None

    def parse_message(self, raw_msg: Dict[str, Any]) -> Dict[str, Any]:
        """Parse raw Gmail message into structured format.

        Args:
            raw_msg: Full message object from Gmail API.

        Returns:
            Parsed email dict with standard fields.
        """
        msg_id = raw_msg.get("id")
        thread_id = raw_msg.get("threadId")
        headers = raw_msg.get("payload", {}).get("headers", [])
        parts = raw_msg.get("payload", {}).get("parts", [])

        # Extract headers
        header_dict = {h["name"]: h["value"] for h in headers}
        from_addr = header_dict.get("From", "")
        to_addrs = header_dict.get("To", "")
        cc_addrs = header_dict.get("Cc", "")
        subject = header_dict.get("Subject", "")
        date_str = header_dict.get("Date", "")

        # Parse From
        from_name = ""
        from_address = ""
        if "<" in from_addr and ">" in from_addr:
            from_name = from_addr.split("<")[0].strip().strip('"')
            from_address = from_addr.split("<")[1].split(">")[0]
        else:
            from_address = from_addr

        # Parse To/Cc
        to_addresses = [e.strip() for e in to_addrs.split(",") if e.strip()]
        cc_addresses = [e.strip() for e in cc_addrs.split(",") if e.strip()]

        # Extract body
        body_text = ""
        has_attachments = False
        attachment_names = []

        # Handle single-part message
        payload = raw_msg.get("payload", {})
        if not parts and payload.get("mimeType") == "text/plain":
            data = payload.get("body", {}).get("data", "")
            if data:
                body_text = base64.urlsafe_b64decode(data).decode("utf-8")

        # Handle multi-part message
        for part in parts:
            if part.get("mimeType") == "text/plain":
                data = part.get("body", {}).get("data", "")
                if data:
                    body_text = base64.urlsafe_b64decode(data).decode("utf-8")
            if part.get("filename"):
                has_attachments = True
                attachment_names.append(part["filename"])

        # Parse received timestamp
        received_at = None
        try:
            from email.utils import parsedate_to_datetime
            received_at = parsedate_to_datetime(date_str).isoformat()
        except Exception:
            received_at = datetime.utcnow().isoformat()

        return {
            "gmail_id": msg_id,
            "thread_id": thread_id,
            "from_address": from_address,
            "from_name": from_name,
            "to_addresses": to_addresses,
            "cc_addresses": cc_addresses,
            "subject": subject,
            "snippet": raw_msg.get("snippet", ""),
            "body_text": body_text,
            "has_attachments": has_attachments,
            "attachment_names": attachment_names,
            "received_at": received_at,
        }

    def create_draft(
        self,
        service: Any,
        to: str,
        subject: str,
        body: str,
        reply_to_id: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """Create a DRAFT email — NEVER auto-sends.

        Per Hard Rule: all customer-facing emails require manual review.

        Args:
            service: Gmail API service object.
            to: Recipient email address.
            subject: Email subject.
            body: Email body (plain text).
            reply_to_id: If set, reply to this message ID.

        Returns:
            Draft object or None if error.
        """
        try:
            from email.mime.text import MIMEText

            msg = MIMEText(body)
            msg["to"] = to
            msg["subject"] = subject

            if reply_to_id:
                original = self.get_message(service, reply_to_id)
                if original:
                    msg["In-Reply-To"] = reply_to_id
                    msg["References"] = reply_to_id

            raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
            draft_body = {"message": {"raw": raw}}
            if reply_to_id and original:
                draft_body["message"]["threadId"] = original.get("threadId")

            result = service.users().drafts().create(
                userId="me", body=draft_body
            ).execute()

            logger.info("gmail_draft_created",
                        to=to, subject=subject,
                        draft_id=result.get("id"))
            return result
        except HttpError as error:
            logger.error("gmail_draft_error", to=to, error=str(error))
            return None
