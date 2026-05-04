"""Domain exceptions for IBS HI Sale Platform.

Provides a consistent error contract for the API layer:
    {error: true, code: <UPPER_SNAKE>, message: <human-readable>}

Subclasses cover the four user-facing error categories:
    - 404 EntityNotFoundError
    - 422 InvalidTransitionError
    - 409 DuplicateError
    - 400 ValidationError (free-form, optional)

Unhandled exceptions still bubble up to the global handler in main.py and
respond with 500 INTERNAL_ERROR.
"""

from typing import Any, Dict, Iterable, List, Optional


class SalePlatformError(Exception):
    """Base exception for the platform's domain errors.

    Carries an HTTP status code, a machine-readable code, and a message.
    Optional ``details`` is merged into the JSON body for context.
    """

    def __init__(
        self,
        status_code: int,
        code: str,
        message: str,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.code = code
        self.message = message
        self.details = details or {}


class EntityNotFoundError(SalePlatformError):
    """Entity lookup miss → HTTP 404."""

    def __init__(self, entity: str, entity_id: str) -> None:
        super().__init__(
            status_code=404,
            code="NOT_FOUND",
            message=f"{entity} '{entity_id}' not found",
            details={"entity": entity, "entity_id": entity_id},
        )


class InvalidTransitionError(SalePlatformError):
    """Invalid state machine transition → HTTP 422.

    ``allowed`` lists the legal target states from the current state so the
    client can render guidance instead of guessing.
    """

    def __init__(
        self,
        entity: str,
        current: str,
        target: str,
        allowed: Iterable[str],
    ) -> None:
        allowed_list: List[str] = list(allowed)
        super().__init__(
            status_code=422,
            code="INVALID_TRANSITION",
            message=(
                f"Invalid {entity} transition: {current} → {target}. "
                f"Allowed: {', '.join(allowed_list) or '(none)'}"
            ),
            details={
                "entity": entity,
                "current": current,
                "target": target,
                "allowed": allowed_list,
            },
        )


class DuplicateError(SalePlatformError):
    """Uniqueness violation → HTTP 409."""

    def __init__(self, entity: str, field: str, value: Any) -> None:
        super().__init__(
            status_code=409,
            code="DUPLICATE",
            message=f"{entity} with {field}='{value}' already exists",
            details={"entity": entity, "field": field, "value": str(value)},
        )


class ValidationError(SalePlatformError):
    """Domain-level validation failure → HTTP 400."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(
            status_code=400,
            code="VALIDATION_ERROR",
            message=message,
            details=details or {},
        )
