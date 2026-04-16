# ADR-001: Python/FastAPI cho Sale Platform (L2)

**Status:** Accepted  
**Date:** 2026-04-16  
**Decision Makers:** Chairman (Arch Lead)

## Context

Liberico Engineering Hard Rule #4 quy định:
> "Python chỉ cho data pipeline — không viết business logic"

Sale Platform v4/v5 là hệ thống Level 2 (departmental) phục vụ phòng SALE của IBS HI,
bao gồm business logic cho email classification, task routing, SLA monitoring, và pipeline management.

## Decision

**Chấp nhận ngoại lệ:** Sale Platform L2 được viết bằng Python/FastAPI.

## Rationale

1. **Team capability** — Builder (Toàn) và team IBS HI đã quen Python hơn Node.js/TypeScript
2. **Scope hẹp** — Đây là departmental tool (L2), không phải platform-level service (L1)
3. **Tight timeline** — Phase 1 MVP target Apr-Jun 2026
4. **No cross-platform dependencies** — Sale Platform không expose data cho platform khác ngoài ibshi1 (qua REST API, đúng pattern cho phép)
5. **Data pipeline affinity** — Email sync, Gmail integration, classification bản chất gần data pipeline

## Constraints

- Giao tiếp với ibshi1 (L1) CHỈ qua REST API — không direct DB access
- Tuân thủ tất cả Engineering Rules khác (DB schema, security, audit, etc.)
- Nếu Sale Platform scale thành L1 hoặc multi-tenant → phải rewrite sang Node.js/TypeScript

## Consequences

- Python code PHẢI tuân thủ:
  - Type hints bắt buộc
  - Structured logging (structlog)
  - Pydantic cho validation
  - Async/await cho I/O operations
- Không import Node.js modules — giao tiếp qua REST API

## References

- Liberico Engineering Rules: Hard Rule #4
- CLAUDE.md: Sale Platform v4 architecture
