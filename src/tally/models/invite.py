"""Invite models for the Tally API."""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Invite:
    """Represents a Tally organization invite."""

    id: str
    organization_id: str
    email: str
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_dict(cls, data: dict) -> "Invite":
        """Create an Invite instance from API response data."""
        return cls(
            id=data["id"],
            organization_id=data["organizationId"],
            email=data["email"],
            created_at=datetime.fromisoformat(data["createdAt"].replace("Z", "+00:00")),
            updated_at=datetime.fromisoformat(data["updatedAt"].replace("Z", "+00:00")),
        )
