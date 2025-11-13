"""Organizations resource for the Tally API."""

from typing import TYPE_CHECKING

from tally.models import Invite, User

if TYPE_CHECKING:
    from tally.client import TallyClient


class OrganizationsResource:
    """Resource for managing Tally organizations."""

    def __init__(self, client: "TallyClient") -> None:
        """Initialize the Organizations resource.

        Args:
            client: The TallyClient instance
        """
        self._client = client

    def list_users(self, organization_id: str) -> list[User]:
        """List all users in an organization.

        Args:
            organization_id: The ID of the organization

        Returns:
            List of User objects in the organization

        Raises:
            NotFoundError: If the organization is not found

        Example:
            ```python
            from tally import Tally

            client = Tally(api_key="tly-xxxx")
            users = client.organizations.list_users("org_123")
            for user in users:
                print(f"{user.full_name} - {user.email}")
            ```
        """
        data = self._client.request("GET", f"/organizations/{organization_id}/users")
        # ? Despite the docs, the API doesn't return the "subscriptionPlan" field for users
        # ? so i made it optional on the User model
        # ? https://developers.tally.so/api-reference/endpoint/organizations/users/get#response-subscription-plan
        return [User.from_dict(user_data) for user_data in data]

    def remove_user(self, organization_id: str, user_id: str) -> None:
        """Remove a user from an organization.

        Only the organization creator can remove other members, or users can remove
        themselves.

        Args:
            organization_id: The ID of the organization
            user_id: The ID of the user to remove from the organization

        Raises:
            ForbiddenError: If you don't have permission to remove this user
            NotFoundError: If the organization or user is not found

        Example:
            ```python
            from tally import Tally

            client = Tally(api_key="tly-xxxx")
            client.organizations.remove_user("org_123", "user_456")
            print("User removed successfully")
            ```
        """
        self._client.request(
            "DELETE", f"/organizations/{organization_id}/users/{user_id}"
        )

    def list_invites(self, organization_id: str) -> list[Invite]:
        """List all invites in an organization.

        Args:
            organization_id: The ID of the organization

        Returns:
            List of Invite objects in the organization

        Raises:
            NotFoundError: If the organization is not found

        Example:
            ```python
            from tally import Tally

            client = Tally(api_key="tly-xxxx")
            invites = client.organizations.list_invites("org_123")
            for invite in invites:
                print(f"{invite.email} - invited at {invite.created_at}")
            ```
        """
        data = self._client.request("GET", f"/organizations/{organization_id}/invites")
        return [Invite.from_dict(invite_data) for invite_data in data]

    def create_invites(
        self,
        organization_id: str,
        workspace_ids: list[str] | str,
        emails: list[str] | str,
    ) -> None:
        """Create invites for users to join specific workspaces.

        Invites users to join specific workspaces within your organization. Existing
        users will be added to workspaces and new users will receive invitation emails.

        Args:
            organization_id: The ID of the organization
            workspace_ids: Workspace ID(s) to invite users to. Can be:
                - A single workspace ID as string: "ws_456"
                - Multiple workspace IDs as list: ["ws_456", "ws_789"]
            emails: Email address(es) to invite. Can be:
                - Comma-separated string: "user1@example.com, user2@example.com"
                - Semicolon-separated string: "user1@example.com; user2@example.com"
                - List of emails: ["user1@example.com", "user2@example.com"]

        Raises:
            BadRequestError: If the request contains invalid parameters
            ForbiddenError: If you don't have permission to create invites
            NotFoundError: If the organization or workspaces are not found

        Example:
            ```python
            from tally import Tally

            client = Tally(api_key="tly-xxxx")
            client.organizations.create_invites(
                organization_id="org_123",
                workspace_ids=["ws_456", "ws_789"],
                emails="user1@example.com, user2@example.com"
            )
            print("Invites created successfully")
            ```
        """
        if isinstance(workspace_ids, str):
            workspace_ids = [workspace_ids]
        if isinstance(emails, list):
            # * This could be ";" instead of ","
            emails = ",".join(emails)

        self._client.request(
            "POST",
            f"/organizations/{organization_id}/invites",
            json={
                "workspaceIds": workspace_ids,
                "emails": emails,
            },
        )

    def cancel_invite(self, organization_id: str, invite_id: str) -> None:
        """Cancel a pending invitation to join workspaces.

        Cancels a pending invitation to join workspaces within your organization.
        Only the user who created the invite can cancel it.

        Args:
            organization_id: The ID of the organization
            invite_id: The ID of the invite to cancel

        Raises:
            ForbiddenError: If you don't have permission to cancel this invite
            NotFoundError: If the organization or invite is not found

        Example:
            ```python
            from tally import Tally

            client = Tally(api_key="tly-xxxx")
            client.organizations.cancel_invite("org_123", "inv_456")
            print("Invite cancelled successfully")
            ```
        """
        self._client.request(
            "DELETE", f"/organizations/{organization_id}/invites/{invite_id}"
        )
