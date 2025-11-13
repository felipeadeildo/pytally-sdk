"""Tally API client."""

from typing import Any

import httpx

from tally.exceptions import (
    BadRequestError,
    ForbiddenError,
    NotFoundError,
    RateLimitError,
    ServerError,
    TallyConnectionError,
    TallyTimeoutError,
    UnauthorizedError,
)
from tally.resources import OrganizationsResource, UsersResource, WorkspacesResource


class TallyClient:
    """Client for interacting with the Tally API."""

    BASE_URL = "https://api.tally.so"
    DEFAULT_TIMEOUT = 30.0

    def __init__(
        self,
        api_key: str,
        *,
        api_version: str | None = None,
        timeout: float = DEFAULT_TIMEOUT,
        base_url: str | None = None,
    ) -> None:
        """Initialize the Tally API client.

        Args:
            api_key: Your Tally API key (Bearer token)
            api_version: Optional API version (e.g., "2025-02-01")
            timeout: Request timeout in seconds
            base_url: Optional custom base URL (defaults to https://api.tally.so)
        """
        self.api_key = api_key
        self.api_version = api_version
        self.base_url = base_url or self.BASE_URL
        self.timeout = timeout

        self._client = httpx.Client(
            base_url=self.base_url,
            timeout=timeout,
            headers=self._get_headers(),
        )

        # Initialize resources
        self.users = UsersResource(self)
        self.organizations = OrganizationsResource(self)
        self.workspaces = WorkspacesResource(self)

    def _get_headers(self) -> dict[str, str]:
        """Get default headers for API requests."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        if self.api_version:
            headers["tally-version"] = self.api_version

        return headers

    def _handle_error(self, response: httpx.Response) -> None:
        """Handle HTTP error responses."""
        # Try to parse JSON error response
        error_data = None
        message = None
        error_type = None
        errors = None

        try:
            error_data = response.json()
            message = error_data.get("message", response.text)
            error_type = error_data.get("errorType")
            errors = error_data.get("errors", [])
        except Exception:
            # If JSON parsing fails, use raw text
            message = response.text or f"HTTP {response.status_code}"

        error_map = {
            400: BadRequestError,
            401: UnauthorizedError,
            403: ForbiddenError,
            404: NotFoundError,
            429: RateLimitError,
            500: ServerError,
        }

        error_class = error_map.get(response.status_code, ServerError)
        raise error_class(
            message=message,
            status_code=response.status_code,
            response=error_data,
            error_type=error_type,
            errors=errors,
        )

    def request(
        self,
        method: str,
        endpoint: str,
        *,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
    ) -> Any:
        """Make a request to the Tally API.

        Args:
            method: HTTP method (GET, POST, DELETE, etc.)
            endpoint: API endpoint (e.g., "/users/me")
            params: Optional query parameters
            json: Optional JSON body

        Returns:
            Response data (dictionary, list, or None for 204 responses)

        Raises:
            TallyAPIError: If the API returns an error
            TallyConnectionError: If there's a connection error
            TallyTimeoutError: If the request times out
        """
        try:
            response = self._client.request(
                method=method,
                url=endpoint,
                params=params,
                json=json,
            )

            if response.status_code >= 400:
                self._handle_error(response)

            # Handle 204 No Content responses
            if response.status_code == 204:
                return None

            return response.json()

        except httpx.TimeoutException as e:
            raise TallyTimeoutError(f"Request timed out: {e}") from e
        except httpx.ConnectError as e:
            raise TallyConnectionError(f"Connection error: {e}") from e
        except (
            BadRequestError,
            UnauthorizedError,
            ForbiddenError,
            NotFoundError,
            RateLimitError,
            ServerError,
        ):
            raise
        except Exception as e:
            raise TallyConnectionError(f"Unexpected error: {e}") from e

    def close(self) -> None:
        """Close the HTTP client."""
        self._client.close()

    def __enter__(self) -> "TallyClient":
        """Context manager entry."""
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Context manager exit."""
        self.close()
