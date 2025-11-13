"""Exceptions for the Tally API client."""

from typing import Any


class TallyError(Exception):
    """Base exception for all Tally API errors."""

    def __init__(self, message: str, status_code: int | None = None) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class TallyAPIError(TallyError):
    """Raised when the API returns an error response."""

    def __init__(
        self,
        message: str,
        status_code: int,
        response: dict[str, Any] | None = None,
        error_type: str | None = None,
        errors: list[dict[str, Any]] | None = None,
    ) -> None:
        super().__init__(message, status_code)
        self.response = response
        self.error_type = error_type
        self.errors = errors or []

    def __str__(self) -> str:
        """Return a formatted error message."""
        parts = [self.message]

        if self.error_type:
            parts.append(f"Error Type: {self.error_type}")

        if self.errors:
            parts.append("Details:")
            for error in self.errors:
                error_type = error.get("errorType", "UNKNOWN")
                error_msg = error.get("msg", "No message provided")
                parts.append(f"  - [{error_type}] {error_msg}")

        if self.status_code:
            parts.append(f"Status Code: {self.status_code}")

        return "\n".join(parts)


class BadRequestError(TallyAPIError):
    """Raised when the request is malformed or contains invalid parameters (400)."""


class UnauthorizedError(TallyAPIError):
    """Raised when authentication credentials are missing or invalid (401)."""


class ForbiddenError(TallyAPIError):
    """Raised when you don't have permission to access a resource (403)."""


class NotFoundError(TallyAPIError):
    """Raised when the requested resource doesn't exist (404)."""


class RateLimitError(TallyAPIError):
    """Raised when you've exceeded the allowed number of requests (429)."""


class ServerError(TallyAPIError):
    """Raised when something goes wrong on Tally's end (500)."""


class TallyConnectionError(TallyError):
    """Raised when there's a connection error to the Tally API."""


class TallyTimeoutError(TallyError):
    """Raised when a request to the Tally API times out."""
