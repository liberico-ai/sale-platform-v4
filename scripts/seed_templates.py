"""Seed 6 email templates into sale_email_templates table.

Usage:
    python seed_templates.py

Inserts templates with {{variable}} placeholders:
    {{customer_name}}, {{project_name}}, {{quotation_ref}}, {{sales_person}},
    {{project_status}}, {{completion_pct}}, etc.
"""

import uuid
from datetime import datetime
from typing import Dict, Any

# Email templates with placeholder variables
EMAIL_TEMPLATES = [
    {
        "template_type": "RFQ_ACK",
        "subject": "Re: Your Inquiry - Thank You",
        "body_template": """Dear {{customer_name}},

Thank you for your inquiry regarding {{project_name}}. We appreciate your interest in our services.

Our team is reviewing your requirements and will provide a detailed quotation within 2 business days.

If you have any urgent questions in the meantime, please feel free to contact us.

Best regards,
{{sales_person}}
IBS HI Sales Team""",
        "description": "Auto-acknowledgment for RFQ inquiries",
        "use_case": "Send automatically when high-confidence RFQ is received",
    },
    {
        "template_type": "FOLLOWUP_3D",
        "subject": "Follow-up: {{project_name}} Quotation",
        "body_template": """Dear {{customer_name}},

I hope this message finds you well. I wanted to follow up on the quotation for {{project_name}} 
that we submitted 3 days ago.

Did you receive our quotation? Do you have any questions or need any clarifications?

I'm happy to discuss the details at your convenience.

Best regards,
{{sales_person}}
IBS HI Sales Team""",
        "description": "3-day follow-up after quotation submission",
        "use_case": "Send 3 days after quotation if no response",
    },
    {
        "template_type": "FOLLOWUP_7D",
        "subject": "Follow-up: {{project_name}} - Status Update Requested",
        "body_template": """Dear {{customer_name}},

I hope you're doing well. I wanted to check in regarding the quotation for {{project_name}} 
that we provided last week (Reference: {{quotation_ref}}).

Have you had a chance to review our proposal? We're ready to discuss any modifications 
or provide additional information as needed.

Looking forward to hearing from you.

Best regards,
{{sales_person}}
IBS HI Sales Team""",
        "description": "7-day follow-up after quotation",
        "use_case": "Send 7 days after quotation if no response",
    },
    {
        "template_type": "FOLLOWUP_14D",
        "subject": "Urgent: {{project_name}} - Your Feedback Needed",
        "body_template": """Dear {{customer_name}},

I notice that we haven't heard back from you regarding the quotation for {{project_name}} 
(Reference: {{quotation_ref}}).

To help us move forward, could you please let me know:
1. Have you received our quotation?
2. Do you have any questions or concerns?
3. What is your timeline for making a decision?

I'm available to discuss this at any time that works for you.

Best regards,
{{sales_person}}
IBS HI Sales Team""",
        "description": "14-day follow-up - escalation needed",
        "use_case": "Send 14 days after quotation; flag as stale",
    },
    {
        "template_type": "FOLLOWUP_30D",
        "subject": "Final Notice: {{project_name}} - Decision Requested",
        "body_template": """Dear {{customer_name}},

This is our final follow-up regarding the quotation for {{project_name}} 
(Reference: {{quotation_ref}}).

We would appreciate your decision by end of this week so we can adjust our planning accordingly.

If you no longer require our services, please let us know so we can close this opportunity.

Thank you for your consideration.

Best regards,
{{sales_person}}
IBS HI Sales Team""",
        "description": "Final 30-day follow-up",
        "use_case": "Send 30 days after quotation; mark deal stale if no response",
    },
    {
        "template_type": "QUOTATION_COVER",
        "subject": "Quotation: {{project_name}} - {{quotation_ref}}",
        "body_template": """Dear {{customer_name}},

Please find attached our quotation for {{project_name}}.

Key Points:
- Project: {{project_name}}
- Reference: {{quotation_ref}}
- Valid for 15 days from submission date

Our team has carefully prepared this quotation based on your specifications. 
We are confident that we can deliver excellent quality and service.

Please review the attached document and don't hesitate to reach out with any questions.

We look forward to working with you!

Best regards,
{{sales_person}}
IBS HI Sales Team""",
        "description": "Cover letter for quotation submission",
        "use_case": "Send along with quotation document",
    },
]


def seed_email_templates() -> Dict[str, Any]:
    """Seed email templates into database.

    Returns:
        Report with counts and status.
    """
    try:
        from ..database import execute, query

        print("[seed_templates] Starting email template seed")

        # Check if already seeded
        existing = query(
            "SELECT COUNT(*) as cnt FROM sale_email_templates",
            one=True,
        )

        if existing and existing.get("cnt", 0) > 0:
            print(f"[seed_templates] {existing['cnt']} templates already exist, skipping")
            return {"skipped": True, "reason": f"{existing['cnt']} templates already exist"}

        # Insert templates
        inserted = 0
        for template in EMAIL_TEMPLATES:
            template_id = str(uuid.uuid4())
            execute(
                """INSERT INTO sale_email_templates
                   (id, template_type, subject, body_template, description,
                    use_case, created_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                [
                    template_id,
                    template["template_type"],
                    template["subject"],
                    template["body_template"],
                    template["description"],
                    template["use_case"],
                    datetime.utcnow().isoformat(),
                ],
            )
            inserted += 1
            print(f"[seed_templates] Inserted {template['template_type']}")

        # Log seed
        import json
        import_log_id = str(uuid.uuid4())
        execute(
            """INSERT INTO sale_import_log
               (id, import_type, source_file, imported_count, notes, created_at)
               VALUES (?, ?, ?, ?, ?, ?)""",
            [
                import_log_id,
                "EMAIL_TEMPLATES",
                "seed_templates.py",
                inserted,
                json.dumps({"templates": [t["template_type"] for t in EMAIL_TEMPLATES]}),
                datetime.utcnow().isoformat(),
            ],
        )

        report = {
            "imported_count": inserted,
            "templates": [t["template_type"] for t in EMAIL_TEMPLATES],
            "success": True,
        }

        print(f"[seed_templates] Template seed complete: {inserted} templates")
        return report

    except Exception as e:
        print(f"[seed_templates] Error: {e}")
        return {"error": str(e)}


if __name__ == "__main__":
    result = seed_email_templates()

    if "error" in result:
        print(f"\nERROR: {result['error']}")
        exit(1)

    if result.get("skipped"):
        print(f"\nSKIPPED: {result['reason']}")
        exit(0)

    print(f"\nTemplate Seed Summary:")
    print(f"  Inserted: {result.get('imported_count', 0)} templates")
    for tmpl in result.get("templates", []):
        print(f"    - {tmpl}")
