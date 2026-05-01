"""Search Router — global UNION search across major entities.

Hits sale_customers, sale_customer_contacts, sale_opportunities,
sale_quotation_history, sale_emails. Returns a flat
[{entity_type, entity_id, title, subtitle, match_field}] list,
limited per entity to keep responses bounded.
"""

from typing import Optional

from fastapi import APIRouter, HTTPException, Query

import structlog

try:
    from ..database import query
except ImportError:
    from database import query

logger = structlog.get_logger(__name__)

router = APIRouter(prefix="/search", tags=["Search"])


@router.get("")
async def global_search(
    q: str = Query(..., min_length=2, description="Free-text search (min 2 chars)"),
    entity_type: Optional[str] = Query(
        None,
        description="Restrict to one type: customer, contact, opportunity, quotation, email",
    ),
    per_type_limit: int = Query(20, ge=1, le=50),
):
    """Search across major entity tables.

    Example: GET /search?q=braden → matches customers named Braden,
    contacts at Braden, opportunities/quotations referencing Braden, etc.
    """
    like = f"%{q}%"
    types_wanted = (
        {entity_type}
        if entity_type
        else {"customer", "contact", "opportunity", "quotation", "email"}
    )

    results: list[dict] = []
    counts: dict[str, int] = {}

    if "customer" in types_wanted:
        rows = query(
            """
            SELECT id, name, code, country
            FROM sale_customers
            WHERE name LIKE ? OR code LIKE ? OR business_description LIKE ?
            ORDER BY
                CASE WHEN code = ? THEN 0
                     WHEN code LIKE ? THEN 1
                     ELSE 2 END,
                name ASC
            LIMIT ?
            """,
            [like, like, like, q, like, per_type_limit],
        )
        counts["customer"] = len(rows)
        for r in rows:
            results.append({
                "entity_type": "customer",
                "entity_id": r["id"],
                "title": r.get("name"),
                "subtitle": " · ".join(filter(None, [r.get("code"), r.get("country")])),
                "match_field": "name|code|description",
            })

    if "contact" in types_wanted:
        rows = query(
            """
            SELECT ct.id, ct.name, ct.email, ct.phone, ct.position,
                   c.name AS customer_name
            FROM sale_customer_contacts ct
            LEFT JOIN sale_customers c ON c.id = ct.customer_id
            WHERE ct.name LIKE ? OR ct.email LIKE ? OR ct.phone LIKE ?
            ORDER BY ct.is_primary DESC, ct.name ASC
            LIMIT ?
            """,
            [like, like, like, per_type_limit],
        )
        counts["contact"] = len(rows)
        for r in rows:
            sub = " · ".join(filter(None, [r.get("position"), r.get("customer_name")]))
            results.append({
                "entity_type": "contact",
                "entity_id": r["id"],
                "title": r.get("name"),
                "subtitle": sub or r.get("email"),
                "match_field": "name|email|phone",
            })

    if "opportunity" in types_wanted:
        rows = query(
            """
            SELECT id, project_name, customer_name, stage, product_group
            FROM sale_opportunities
            WHERE project_name LIKE ? OR scope_en LIKE ? OR scope_vn LIKE ?
               OR customer_name LIKE ? OR pl_hd LIKE ?
            ORDER BY last_activity_date DESC
            LIMIT ?
            """,
            [like, like, like, like, like, per_type_limit],
        )
        counts["opportunity"] = len(rows)
        for r in rows:
            sub = " · ".join(filter(None, [
                r.get("customer_name"), r.get("stage"), r.get("product_group"),
            ]))
            results.append({
                "entity_type": "opportunity",
                "entity_id": r["id"],
                "title": r.get("project_name"),
                "subtitle": sub,
                "match_field": "project|scope|customer",
            })

    if "quotation" in types_wanted:
        rows = query(
            """
            SELECT id, quotation_no, project_name, customer_name, status, value_usd
            FROM sale_quotation_history
            WHERE project_name LIKE ? OR customer_name LIKE ?
               OR customer_code LIKE ? OR scope_of_work LIKE ?
            ORDER BY date_offer DESC
            LIMIT ?
            """,
            [like, like, like, like, per_type_limit],
        )
        counts["quotation"] = len(rows)
        for r in rows:
            usd = r.get("value_usd")
            value_str = f"${usd:,.0f}" if usd else None
            sub = " · ".join(filter(None, [
                r.get("customer_name"), r.get("status"), value_str,
            ]))
            results.append({
                "entity_type": "quotation",
                "entity_id": r["id"],
                "title": f"#{r.get('quotation_no')} — {r.get('project_name')}",
                "subtitle": sub,
                "match_field": "project|customer|scope",
            })

    if "email" in types_wanted:
        rows = query(
            """
            SELECT id, subject, from_address, snippet, email_type
            FROM sale_emails
            WHERE subject LIKE ? OR snippet LIKE ? OR from_address LIKE ?
            ORDER BY received_at DESC
            LIMIT ?
            """,
            [like, like, like, per_type_limit],
        )
        counts["email"] = len(rows)
        for r in rows:
            results.append({
                "entity_type": "email",
                "entity_id": r["id"],
                "title": r.get("subject") or "(no subject)",
                "subtitle": " · ".join(filter(None, [
                    r.get("from_address"), r.get("email_type"),
                ])),
                "match_field": "subject|snippet|from",
            })

    return {
        "query": q,
        "total": sum(counts.values()),
        "counts_by_type": counts,
        "results": results,
    }
