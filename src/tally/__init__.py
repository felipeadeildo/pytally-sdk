"""Unofficial Python SDK for the Tally.so API."""

from tally.client import TallyClient
from tally.exceptions import (
    BadRequestError,
    ForbiddenError,
    NotFoundError,
    RateLimitError,
    ServerError,
    TallyAPIError,
    TallyConnectionError,
    TallyError,
    TallyTimeoutError,
    UnauthorizedError,
)
from tally.models import Invite, SubscriptionPlan, User
from tally.resources import OrganizationsResource, UsersResource

__version__ = "0.1.0"

# Alias for convenience
Tally = TallyClient

__all__ = [
    # Main client
    "Tally",
    "TallyClient",
    # Resources
    "OrganizationsResource",
    "UsersResource",
    # Models
    "Invite",
    "User",
    "SubscriptionPlan",
    # Exceptions
    "TallyError",
    "TallyAPIError",
    "BadRequestError",
    "UnauthorizedError",
    "ForbiddenError",
    "NotFoundError",
    "RateLimitError",
    "ServerError",
    "TallyConnectionError",
    "TallyTimeoutError",
]
