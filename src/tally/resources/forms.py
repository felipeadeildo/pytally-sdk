"""Forms resource for the Tally API."""

from typing import TYPE_CHECKING, Any, Iterator

from tally.models.form import (
    Form,
    FormBlock,
    FormCreated,
    FormDetails,
    FormSettings,
    FormStatus,
    PaginatedForms,
)

if TYPE_CHECKING:
    from tally.client import TallyClient


class FormsResource:
    """Resource for managing Tally forms."""

    def __init__(self, client: "TallyClient") -> None:
        """Initialize the Forms resource.

        Args:
            client: The TallyClient instance
        """
        self._client = client

    def all(
        self,
        page: int = 1,
        limit: int = 50,
        workspace_ids: list[str] | None = None,
    ) -> PaginatedForms:
        """Get all forms with pagination.

        Returns a paginated list of form objects.

        Args:
            page: Page number for pagination (default: 1, min: 1)
            limit: Number of forms per page (default: 50, max: 500)
            workspace_ids: Filter forms by specific workspace IDs (optional)

        Returns:
            PaginatedForms object containing forms and pagination info

        Example:
            ```python
            from tally import Tally

            client = Tally(api_key="tly-xxxx")

            # Get first page
            result = client.forms.all()
            print(f"Page {result.page} of {result.total} forms")

            for form in result.items:
                print(f"Form: {form.name}")
                print(f"  Status: {form.status.value}")
                print(f"  Submissions: {form.number_of_submissions}")
                print(f"  Closed: {form.is_closed}")

            # Get next page with custom limit
            if result.has_more:
                next_page = client.forms.all(page=2, limit=100)

            # Filter by workspace IDs
            workspace_forms = client.forms.all(workspace_ids=["ws_123", "ws_456"])
            ```
        """
        params: dict[str, str | int | list[str]] = {"page": page, "limit": limit}

        if workspace_ids is not None:
            params["workspaceIds"] = workspace_ids

        data = self._client.request("GET", "/forms", params=params)
        return PaginatedForms.from_dict(data)

    def get(self, form_id: str) -> FormDetails:
        """Get a single form by ID with all its blocks and settings.

        Returns the complete form structure including all blocks, settings,
        and configuration details.

        Args:
            form_id: The ID of the form to retrieve

        Returns:
            FormDetails object containing the complete form with blocks and settings

        Raises:
            NotFoundError: If the form doesn't exist or you don't have access
            UnauthorizedError: If authentication credentials are invalid

        Example:
            ```python
            from tally import Tally

            client = Tally(api_key="tly-xxxx")

            # Get a form by ID
            form = client.forms.get("form_abc123")

            print(f"Form: {form.name}")
            print(f"Status: {form.status.value}")
            print(f"Workspace: {form.workspace_id}")
            print(f"Submissions: {form.number_of_submissions}")
            print(f"Is Closed: {form.is_closed}")

            # Access settings
            print(f"Language: {form.settings.language}")
            print(f"Has Progress Bar: {form.settings.has_progress_bar}")
            print(f"Save for Later: {form.settings.save_for_later}")

            # Access blocks
            print(f"Total blocks: {len(form.blocks)}")
            for block in form.blocks:
                print(f"  Block {block.uuid}: {block.type}")
                print(f"    Group: {block.group_type}")
                if block.payload:
                    print(f"    Payload: {block.payload}")

            # Access payments if configured
            if form.payments:
                for payment in form.payments:
                    print(f"Payment: {payment.amount} {payment.currency}")
            ```
        """
        data = self._client.request("GET", f"/forms/{form_id}")
        return FormDetails.from_dict(data)

    def create(
        self,
        status: FormStatus | str,
        blocks: list[FormBlock] | list[dict[str, Any]],
        workspace_id: str | None = None,
        template_id: str | None = None,
        settings: FormSettings | dict[str, Any] | None = None,
    ) -> FormCreated:
        """Create a new form.

        Creates a new form, optionally based on a template or within a specific workspace.

        Args:
            status: Initial status of the form (BLANK, DRAFT, PUBLISHED, DELETED)
            blocks: Array of form block objects defining the form structure
            workspace_id: ID of the workspace to create the form in (optional)
            template_id: ID of the template to base the form on (optional)
            settings: Form settings configuration (optional)

        Returns:
            FormCreated object with the created form details

        Raises:
            BadRequestError: If the request parameters are invalid

        Example:
            ```python
            from tally import Tally
            from tally.models import FormStatus, FormBlock, BlockType, FormSettings

            client = Tally(api_key="tly-xxxx")

            # Create a simple form with type-safe objects
            blocks = [
                FormBlock(
                    uuid="3c90c3cc-0d44-4b50-8888-8dd25736052a",
                    type=BlockType.FORM_TITLE,
                    group_uuid="3c90c3cc-0d44-4b50-8888-8dd25736052a",
                    group_type=BlockType.FORM_TITLE,
                    payload={"html": "<h1>My Form</h1>"}
                )
            ]

            settings = FormSettings(
                is_closed=False,
                save_for_later=True,
                has_progress_bar=True
            )

            form = client.forms.create(
                status=FormStatus.DRAFT,
                blocks=blocks,
                workspace_id="ws_123",
                settings=settings
            )

            print(f"Created form: {form.id}")
            print(f"Status: {form.status.value}")

            # Or use simple dicts for flexibility
            form = client.forms.create(
                status="DRAFT",
                blocks=[{
                    "uuid": "3c90c3cc-0d44-4b50-8888-8dd25736052a",
                    "type": "FORM_TITLE",
                    "groupUuid": "3c90c3cc-0d44-4b50-8888-8dd25736052a",
                    "groupType": "FORM_TITLE",
                    "payload": {"html": "<h1>My Form</h1>"}
                }],
                settings={
                    "isClosed": False,
                    "saveForLater": True
                }
            )
            ```
        """
        body: dict[str, Any] = {
            "status": status.value if isinstance(status, FormStatus) else status,
            "blocks": [
                block.to_dict() if isinstance(block, FormBlock) else block
                for block in blocks
            ],
        }

        if workspace_id is not None:
            body["workspaceId"] = workspace_id

        if template_id is not None:
            body["templateId"] = template_id

        if settings is not None:
            body["settings"] = (
                settings.to_dict() if isinstance(settings, FormSettings) else settings
            )

        data = self._client.request("POST", "/forms", json=body)
        return FormCreated.from_dict(data)

    def update(
        self,
        form_id: str,
        name: str | None = None,
        status: FormStatus | str | None = None,
        blocks: list[FormBlock] | list[dict[str, Any]] | None = None,
        settings: FormSettings | dict[str, Any] | None = None,
    ) -> Form:
        """Update an existing form.

        Updates one or more properties of an existing form. All parameters except
        form_id are optional - only provide the fields you want to update.

        Args:
            form_id: The ID of the form to update
            name: New name for the form (optional)
            status: New status for the form (BLANK, DRAFT, PUBLISHED, DELETED) (optional)
            blocks: Updated array of form blocks (optional)
            settings: Updated form settings (optional)

        Returns:
            Form object with the updated form details

        Example:
            ```python
            from tally import Tally
            from tally.models import FormStatus, FormSettings

            client = Tally(api_key="tly-xxxx")

            # Update form name only
            form = client.forms.update(
                form_id="form_abc123",
                name="Updated Form Name"
            )

            # Update status to published
            form = client.forms.update(
                form_id="form_abc123",
                status=FormStatus.PUBLISHED
            )

            # Update multiple fields at once
            form = client.forms.update(
                form_id="form_abc123",
                name="New Name",
                status="PUBLISHED",
                settings=FormSettings(
                    is_closed=True,
                    close_message_title="Form Closed",
                    close_message_description="Thank you for your interest"
                )
            )

            # Update with dict for flexibility
            form = client.forms.update(
                form_id="form_abc123",
                settings={
                    "isClosed": False,
                    "hasProgressBar": True,
                    "saveForLater": True
                }
            )
            ```
        """
        body: dict[str, Any] = {}

        if name is not None:
            body["name"] = name

        if status is not None:
            body["status"] = status.value if isinstance(status, FormStatus) else status

        if blocks is not None:
            body["blocks"] = [
                block.to_dict() if isinstance(block, FormBlock) else block
                for block in blocks
            ]

        if settings is not None:
            body["settings"] = (
                settings.to_dict() if isinstance(settings, FormSettings) else settings
            )

        data = self._client.request("PATCH", f"/forms/{form_id}", json=body)
        return Form.from_dict(data)

    def delete(self, form_id: str) -> None:
        """Delete a form by its ID.

        Deletes a form and moves it to the trash. This operation is reversible
        from the Tally web interface.

        Args:
            form_id: The ID of the form to delete

        Example:
            ```python
            from tally import Tally

            client = Tally(api_key="tly-xxxx")

            client.forms.delete("form_abc123")
            ```
        """
        self._client.request("DELETE", f"/forms/{form_id}")

    def __iter__(self) -> Iterator[Form]:
        """Iterate through all forms across all pages.

        Automatically fetches all pages and yields each form.

        Yields:
            Form objects one at a time

        Example:
            ```python
            from tally import Tally

            client = Tally(api_key="tly-xxxx")

            # Iterate through all forms automatically
            for form in client.forms:
                print(f"Form: {form.name}")
                print(f"  Status: {form.status.value}")
                print(f"  Submissions: {form.number_of_submissions}")
            ```
        """
        page = 1
        while True:
            result = self.all(page=page)

            for form in result.items:
                yield form

            if not result.has_more:
                break

            page += 1
