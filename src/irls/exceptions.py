"""Custom exceptions for IRLS SDK."""

from typing import Any, Dict, Optional


class IRLSError(Exception):
    """Base exception for IRLS SDK."""

    pass


class SensorNotFoundError(IRLSError):
    """Raised when sensor is not found (404)."""

    def __init__(self, sensor_slug: str, message: Optional[str] = None) -> None:
        self.sensor_slug = sensor_slug
        self.message = message or f"Sensor '{sensor_slug}' not found"
        super().__init__(self.message)


class SensorDisabledError(IRLSError):
    """Raised when sensor is disabled (403)."""

    def __init__(self, sensor_slug: str, message: Optional[str] = None) -> None:
        self.sensor_slug = sensor_slug
        self.message = message or f"Sensor '{sensor_slug}' is disabled"
        super().__init__(self.message)


class APIDisabledError(IRLSError):
    """Raised when the IRLS API is disabled (404)."""

    def __init__(self, message: Optional[str] = None) -> None:
        self.message = message or "IRLS API is disabled"
        super().__init__(self.message)


class ValidationError(IRLSError):
    """Raised when request validation fails (422)."""

    def __init__(self, message: str, errors: Optional[Dict[str, Any]] = None) -> None:
        self.message = message
        self.errors = errors or {}
        super().__init__(self.message)

    def __str__(self) -> str:
        if self.errors:
            error_details = ", ".join(
                f"{field}: {', '.join(msgs)}" for field, msgs in self.errors.items()
            )
            return f"{self.message} - {error_details}"
        return self.message


class RequestError(IRLSError):
    """Raised when an HTTP request fails."""

    def __init__(
        self, message: str, status_code: Optional[int] = None, response_text: Optional[str] = None
    ) -> None:
        self.message = message
        self.status_code = status_code
        self.response_text = response_text
        super().__init__(self.message)

    def __str__(self) -> str:
        if self.status_code:
            return f"{self.message} (HTTP {self.status_code})"
        return self.message
