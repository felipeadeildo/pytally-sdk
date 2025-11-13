"""Organizations resource for the Tally API."""

from typing import TYPE_CHECKING

from tally.models import User

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
            UnauthorizedError: If the API key is invalid or missing
            NotFoundError: If the organization is not found
            TallyAPIError: If the API returns an error
            TallyConnectionError: If there's a connection error
            TallyTimeoutError: If the request times out

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
            UnauthorizedError: If the API key is invalid or missing
            ForbiddenError: If you don't have permission to remove this user
            NotFoundError: If the organization or user is not found
            TallyAPIError: If the API returns an error
            TallyConnectionError: If there's a connection error
            TallyTimeoutError: If the request times out

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
