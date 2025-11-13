"""Users resource for the Tally API."""

from typing import TYPE_CHECKING

from tally.models import User

if TYPE_CHECKING:
    from tally.client import TallyClient


class UsersResource:
    """Resource for managing Tally users."""

    def __init__(self, client: "TallyClient") -> None:
        """Initialize the Users resource.

        Args:
            client: The TallyClient instance
        """
        self._client = client

    def me(self) -> User:
        """Get information about the current authenticated user.

        Returns:
            User object with current user information

        Example:
            ```python
            from tally import Tally

            client = Tally(api_key="tly-xxxx")
            user = client.users.me()
            print(f"Hello, {user.full_name}!")
            ```
        """
        data = self._client.request("GET", "/users/me")
        return User.from_dict(data)
