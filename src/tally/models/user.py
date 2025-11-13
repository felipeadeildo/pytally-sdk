"""User models for the Tally API."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class SubscriptionPlan(str, Enum):
    """Tally subscription plans."""

    FREE = "FREE"
    PRO = "PRO"
    BUSINESS = "BUSINESS"


@dataclass
class User:
    """Represents a Tally user."""

    id: str
    first_name: str
    last_name: str
    full_name: str
    email: str
    avatar_url: str | None
    organization_id: str
    is_deleted: bool
    has_two_factor_enabled: bool
    created_at: datetime
    updated_at: datetime
    subscription_plan: SubscriptionPlan | None = None

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        """Create a User instance from API response data."""
        return cls(
            id=data["id"],
            first_name=data["firstName"],
            last_name=data["lastName"],
            full_name=data["fullName"],
            email=data["email"],
            avatar_url=data.get("avatarUrl"),
            organization_id=data["organizationId"],
            is_deleted=data["isDeleted"],
            has_two_factor_enabled=data["hasTwoFactorEnabled"],
            created_at=datetime.fromisoformat(data["createdAt"].replace("Z", "+00:00")),
            updated_at=datetime.fromisoformat(data["updatedAt"].replace("Z", "+00:00")),
            subscription_plan=SubscriptionPlan(data["subscriptionPlan"])
            if "subscriptionPlan" in data
            else None,
        )
