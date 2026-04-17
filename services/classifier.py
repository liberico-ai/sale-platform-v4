"""Email classifier with 10 rule-based types for IBS HI Sale Platform.

Classifies emails by weighted scoring of subject, body, and attachment patterns.
Also matches customer domain to sale_customers table.
"""

import re
from typing import Dict, Optional, Tuple, Any, List

# Email classification rules with weighted scoring
CLASSIFIER_RULES = [
    {
        "type": "RFQ",
        "subject_patterns": ["rfq", "quotation", "inquiry", "báo giá", "request for", "price for"],
        "body_patterns": ["please quote", "kindly provide", "request for quotation"],
        "attachment_types": [".pdf", ".dwg", ".xlsx", ".xls"],
        "weight": 1.0,
    },
    {
        "type": "TECHNICAL",
        "subject_patterns": ["re:", "fw:", "drawing", "specification", "clarification"],
        "attachment_types": [".dwg", ".pdf", ".step", ".igs"],
        "requires_existing_thread": True,
        "weight": 0.8,
    },
    {
        "type": "NEGOTIATION",
        "subject_patterns": ["revision", "discount", "counter", "best price", "điều chỉnh"],
        "body_patterns": ["reduce", "lower price", "final offer", "phản hồi giá"],
        "weight": 0.9,
    },
    {
        "type": "CONTRACT",
        "subject_patterns": ["po", "purchase order", "contract", "hợp đồng", "award"],
        "body_patterns": ["pleased to award", "purchase order attached"],
        "weight": 1.0,
    },
    {
        "type": "PAYMENT",
        "subject_patterns": ["invoice", "payment", "remittance", "thanh toán"],
        "body_patterns": ["payment confirmation", "bank transfer"],
        "weight": 0.9,
    },
    {
        "type": "FOLLOWUP",
        "subject_patterns": ["follow up", "reminder", "status", "update"],
        "weight": 0.7,
    },
    {
        "type": "INTERNAL",
        "subject_patterns": ["internal", "nội bộ"],
        "body_patterns": ["internal note"],
        "weight": 0.6,
    },
    {
        "type": "VENDOR",
        "subject_patterns": ["vendor", "registration", "qualification", "supplier"],
        "weight": 0.7,
    },
    {
        "type": "COMPLAINT",
        "subject_patterns": ["complaint", "claim", "khiếu nại", "defect", "ncr", "non-conformance"],
        "body_patterns": ["not acceptable", "reject", "failed inspection", "quality issue"],
        "weight": 0.9,
    },
]

# Fallback rule
FALLBACK_RULE = {
    "type": "GENERAL",
    "weight": 0.5,
}


def classify_email(parsed_email: Dict[str, Any]) -> Tuple[str, float]:
    """Classify email by matching rule patterns.

    Scores are calculated by:
    - Subject pattern match: +2 points per match
    - Body pattern match: +1 point per match
    - Attachment type match: +1 point per match
    - Final score = raw_score * rule_weight, normalized to 0-1

    Args:
        parsed_email: Dict with keys: subject, body_text, attachment_names, etc.

    Returns:
        Tuple of (email_type, confidence) where confidence is 0.0-1.0.
    """
    subject = parsed_email.get("subject", "").lower()
    body = parsed_email.get("body_text", "").lower()
    attachments = parsed_email.get("attachment_names", [])

    scores = {}

    for rule in CLASSIFIER_RULES:
        score = 0

        # Subject pattern matching
        for pattern in rule.get("subject_patterns", []):
            if pattern.lower() in subject:
                score += 2

        # Body pattern matching
        for pattern in rule.get("body_patterns", []):
            if pattern.lower() in body:
                score += 1

        # Attachment type matching
        if rule.get("attachment_types"):
            for att in attachments:
                if any(att.lower().endswith(ext) for ext in rule["attachment_types"]):
                    score += 1

        if score > 0:
            # Apply weight and normalize
            weighted_score = score * rule.get("weight", 0.5)
            scores[rule["type"]] = weighted_score

    # Domain-based scoring for INTERNAL emails
    from_address = parsed_email.get("from_address", "").lower()
    if "@ibs.com.vn" in from_address:
        current_internal_score = scores.get("INTERNAL", 0)
        scores["INTERNAL"] = current_internal_score + (3 * 0.6)

    # Determine best match
    if not scores:
        return (FALLBACK_RULE["type"], FALLBACK_RULE["weight"])

    best_type = max(scores, key=scores.get)
    max_score = scores[best_type]
    confidence = min(max_score / 5.0, 1.0)  # Normalize to 0-1 range

    return (best_type, round(confidence, 2))


def match_customer(from_address: str, customers: List[Dict[str, Any]] = None) -> Optional[str]:
    """Match email sender to customer by domain.

    Extracts domain from from_address and searches for customer with matching
    email domain in sale_customers table.

    Args:
        from_address: Email address to match (e.g., 'john@acme.com').
        customers: List of customer dicts with 'email_domain' and 'id' fields.
                   If None, will be loaded from database.

    Returns:
        Customer ID (string) if match found, None otherwise.
    """
    if not from_address or "@" not in from_address:
        return None

    domain = from_address.split("@")[1].lower()

    # If customers not provided, try to load from database
    if customers is None:
        try:
            from ..database import query
            customers = query(
                "SELECT id, email_domain FROM sale_customers WHERE email_domain IS NOT NULL",
            )
        except Exception:
            # Database not available, skip matching
            return None

    if not customers:
        return None

    # Exact domain match
    for cust in customers:
        if cust.get("email_domain", "").lower() == domain:
            return str(cust.get("id"))

    # Partial domain match (e.g., 'acme.com' matches '@acme.com' and '@subsidiary.acme.com')
    for cust in customers:
        cust_domain = cust.get("email_domain", "").lower()
        if cust_domain and (domain == cust_domain or domain.endswith("." + cust_domain)):
            return str(cust.get("id"))

    return None


def extract_email_domain(email_address: str) -> Optional[str]:
    """Extract domain from email address.

    Args:
        email_address: Email address (e.g., 'john@acme.com').

    Returns:
        Domain string (e.g., 'acme.com') or None if invalid.
    """
    if not email_address or "@" not in email_address:
        return None
    return email_address.split("@")[1].lower()


def score_confidence(raw_score: float, rule_weight: float = 1.0) -> float:
    """Convert raw rule score to confidence percentage.

    Args:
        raw_score: Raw accumulation of pattern matches.
        rule_weight: Weight multiplier for rule type.

    Returns:
        Confidence as float 0.0-1.0.
    """
    weighted = raw_score * rule_weight
    normalized = min(weighted / 5.0, 1.0)
    return round(normalized, 2)
