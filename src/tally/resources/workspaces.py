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

    def create(self, name: str) -> Workspace:
        """Create a new workspace.

        Creates a new workspace and assigns the authenticated user as a member.
        Requires a Pro subscription.

        Args:
            name: The name of the workspace

        Returns:
            Workspace object with the created workspace

        Raises:
            ForbiddenError: If user doesn't have a Pro subscription

        Example:
            ```python
            from tally import Tally

            client = Tally(api_key="tly-xxxx")
            workspace = client.workspaces.create(name="My New Workspace")
            print(f"Created workspace: {workspace.name} (ID: {workspace.id})")
            ```
        """
        data = self._client.request("POST", "/workspaces", json={"name": name})
        return Workspace.from_dict(data)

    def get(self, workspace_id: str) -> Workspace:
        """Fetch a single workspace by its ID.

        Returns a workspace with associated members and pending invites.

        Args:
            workspace_id: The ID of the workspace to retrieve

        Returns:
            Workspace object with members and invites

        Raises:
            NotFoundError: If the workspace is not found

        Example:
            ```python
            from tally import Tally

            client = Tally(api_key="tly-xxxx")
            workspace = client.workspaces.get("ws_123")
            print(f"Workspace: {workspace.name}")
            print(f"Members: {len(workspace.members)}")
            ```
        """
        data = self._client.request("GET", f"/workspaces/{workspace_id}")
        return Workspace.from_dict(data)

    def update(self, workspace_id: str, name: str) -> None:
        """Update a workspace's information.

        Updates a workspace's name by its ID.

        Args:
            workspace_id: The ID of the workspace to update
            name: The new name for the workspace

        Raises:
            NotFoundError: If the workspace is not found

        Example:
            ```python
            from tally import Tally

            client = Tally(api_key="tly-xxxx")
            client.workspaces.update("ws_123", name="Updated Workspace Name")
            print("Workspace updated successfully")
            ```
        """
        # ? actually i dont know if the API returns the updated workspace (the API docs dont say anything about it)
        self._client.request(
            "PATCH", f"/workspaces/{workspace_id}", json={"name": name}
        )

    def delete(self, workspace_id: str) -> None:
        """Delete a workspace.

        Deletes a workspace and all its associated forms. The workspace and forms
        are moved to trash and can be restored later. Forms in DRAFT or PUBLISHED
        state will be marked as DELETED.

        Args:
            workspace_id: The ID of the workspace to delete

        Raises:
            NotFoundError: If the workspace is not found

        Example:
            ```python
            from tally import Tally

            client = Tally(api_key="tly-xxxx")
            client.workspaces.delete("ws_123")
            print("Workspace deleted successfully")
            ```
        """
        self._client.request("DELETE", f"/workspaces/{workspace_id}")
