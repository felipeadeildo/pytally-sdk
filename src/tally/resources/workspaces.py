"""Workspaces resource for the Tally API."""

from typing import TYPE_CHECKING, Iterator

from tally.models.workspace import PaginatedWorkspaces, Workspace

if TYPE_CHECKING:
    from tally.client import TallyClient


class WorkspacesResource:
    """Resource for managing Tally workspaces."""

    def __init__(self, client: "TallyClient") -> None:
        """Initialize the Workspaces resource.

        Args:
            client: The TallyClient instance
        """
        self._client = client

    # ? possibly there's limit query string param
    def list(self, page: int = 1) -> PaginatedWorkspaces:
        """List workspaces with pagination.

        Returns a paginated array of workspace objects with associated users
        and pending invites.

        Args:
            page: Page number for pagination (default: 1)

        Returns:
            PaginatedWorkspaces object containing workspaces and pagination info

        Example:
            ```python
            from tally import Tally

            client = Tally(api_key="tly-xxxx")

            # Get first page
            result = client.workspaces.list()
            print(f"Page {result.page} of {result.total} workspaces")

            for workspace in result.items:
                print(f"Workspace: {workspace.name}")
                print(f"  Members: {len(workspace.members)}")
                print(f"  Invites: {len(workspace.invites)}")

            # Get next page if available
            if result.has_more:
                next_page = client.workspaces.list(page=result.page + 1)
            ```
        """
        data = self._client.request("GET", "/workspaces", params={"page": page})
        return PaginatedWorkspaces.from_dict(data)

    def __iter__(self) -> Iterator[Workspace]:
        """Iterate through all workspaces across all pages.

        Automatically fetches all pages and yields each workspace.

        Yields:
            Workspace objects one at a time

        Example:
            ```python
            from tally import Tally

            client = Tally(api_key="tly-xxxx")

            # Iterate through all workspaces automatically
            for workspace in client.workspaces:
                print(f"Workspace: {workspace.name}")
                print(f"  Members: {len(workspace.members)}")
            ```
        """
        page = 1
        while True:
            result = self.list(page=page)

            for workspace in result.items:
                yield workspace

            if not result.has_more:
                break

            page += 1
