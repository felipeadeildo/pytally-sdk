"""Workspace models for the Tally API."""

from dataclasses import dataclass
from datetime import datetime

from tally.models.user import User


@dataclass
class WorkspaceInvite:
    """Represents a workspace invite."""

    id: str
    email: str
    workspace_ids: list[str]
    created_by_user_id: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @classmethod
    def from_dict(cls, data: dict) -> "WorkspaceInvite":
        """Create a WorkspaceInvite instance from API response data."""
        return cls(
            id=data["id"],
            email=data["email"],
            workspace_ids=data.get("workspaceIds", []),
            created_by_user_id=data.get("createdByUserId"),
            created_at=datetime.fromisoformat(data["createdAt"].replace("Z", "+00:00"))
            if "createdAt" in data
            else None,
            updated_at=datetime.fromisoformat(data["updatedAt"].replace("Z", "+00:00"))
            if "updatedAt" in data
            else None,
        )


@dataclass
class Workspace:
    """Represents a Tally workspace."""

    id: str
    name: str
    members: list[User]
    invites: list[WorkspaceInvite]
    created_by_user_id: str
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_dict(cls, data: dict) -> "Workspace":
        """Create a Workspace instance from API response data."""
        return cls(
            id=data["id"],
            name=data["name"],
            members=[User.from_dict(member) for member in data.get("members", [])],
            invites=[
                WorkspaceInvite.from_dict(invite) for invite in data.get("invites", [])
            ],
            created_by_user_id=data["createdByUserId"],
            created_at=datetime.fromisoformat(data["createdAt"].replace("Z", "+00:00")),
            updated_at=datetime.fromisoformat(data["updatedAt"].replace("Z", "+00:00")),
        )


@dataclass
class PaginatedWorkspaces:
    """Represents a paginated response of workspaces."""

    items: list[Workspace]
    page: int
    limit: int
    total: int
    has_more: bool

    @classmethod
    def from_dict(cls, data: dict) -> "PaginatedWorkspaces":
        """Create a PaginatedWorkspaces instance from API response data."""
        return cls(
            items=[Workspace.from_dict(item) for item in data.get("items", [])],
            page=data["page"],
            limit=data["limit"],
            total=data["total"],
            has_more=data["hasMore"],
        )
