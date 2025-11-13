"""Webhooks resource for the Tally API."""

from typing import TYPE_CHECKING, Iterator

from tally.models.webhook import (
    PaginatedWebhookEvents,
    PaginatedWebhooks,
    Webhook,
    WebhookCreated,
    WebhookEventType,
    WebhookHeader,
)

if TYPE_CHECKING:
    from tally.client import TallyClient


class WebhooksResource:
    """Resource for managing Tally webhooks."""

    def __init__(self, client: "TallyClient") -> None:
        """Initialize the Webhooks resource.

        Args:
            client: The TallyClient instance
        """
        self._client = client

    def all(self, page: int = 1, limit: int = 25) -> PaginatedWebhooks:
        """Get all webhooks with pagination.

        Returns a paginated list of all webhooks across your accessible forms
        and workspaces.

        Args:
            page: Page number for pagination (default: 1, min: 1)
            limit: Number of webhooks per page (default: 25, max: 100)

        Returns:
            PaginatedWebhooks object containing webhooks and pagination info

        Example:
            ```python
            from tally import Tally

            client = Tally(api_key="tly-xxxx")

            # Get first page
            result = client.webhooks.all()
            print(f"Page {result.page} - Total: {result.total_count} webhooks")

            for webhook in result.webhooks:
                print(f"Webhook: {webhook.url}")
                print(f"  Form ID: {webhook.form_id}")
                print(f"  Enabled: {webhook.is_enabled}")

            # Get next page with custom limit
            if result.has_more:
                next_page = client.webhooks.all(page=2, limit=50)
            ```
        """
        params = {"page": page, "limit": limit}
        data = self._client.request("GET", "/webhooks", params=params)
        return PaginatedWebhooks.from_dict(data)

    def __iter__(self) -> Iterator[Webhook]:
        """Iterate through all webhooks across all pages.

        Automatically fetches all pages and yields each webhook.

        Yields:
            Webhook objects one at a time

        Example:
            ```python
            from tally import Tally

            client = Tally(api_key="tly-xxxx")

            # Iterate through all webhooks automatically
            for webhook in client.webhooks:
                print(f"Webhook: {webhook.url}")
                print(f"  Enabled: {webhook.is_enabled}")
            ```
        """
        page = 1
        while True:
            result = self.all(page=page)

            for webhook in result.webhooks:
                yield webhook

            if not result.has_more:
                break

            page += 1

    def create(
        self,
        form_id: str,
        url: str,
        event_types: list[WebhookEventType] | list[str] | None = None,
        signing_secret: str | None = None,
        http_headers: list[WebhookHeader] | list[dict[str, str]] | None = None,
        external_subscriber: str | None = None,
    ) -> WebhookCreated:
        """Create a new webhook for a form.

        Creates a new webhook to receive form events.

        Args:
            form_id: The ID of the form to create the webhook for
            url: The URL to send webhook events to
            event_types: Types of events to receive. Can be:
                - List of WebhookEventType enums: [WebhookEventType.FORM_RESPONSE]
                - List of strings: ["FORM_RESPONSE"]
                - None (defaults to ["FORM_RESPONSE"])
            signing_secret: Optional secret used to sign webhook payloads
            http_headers: Optional custom HTTP headers. Can be:
                - List of WebhookHeader objects
                - List of dicts with 'name' and 'value' keys
            external_subscriber: Optional identifier for the external subscriber

        Returns:
            WebhookCreated object with webhook creation response

        Example:
            ```python
            from tally import Tally, WebhookEventType

            client = Tally(api_key="tly-xxxx")

            # Simple webhook with string event types
            webhook = client.webhooks.create(
                form_id="form_123",
                url="https://example.com/webhook",
                event_types=["FORM_RESPONSE"]
            )

            # Using enum types
            webhook = client.webhooks.create(
                form_id="form_123",
                url="https://example.com/webhook",
                event_types=[WebhookEventType.FORM_RESPONSE]
            )

            # With custom headers and signing secret
            webhook = client.webhooks.create(
                form_id="form_123",
                url="https://example.com/webhook",
                signing_secret="my-secret",
                http_headers=[
                    {"name": "X-Custom-Header", "value": "custom-value"}
                ],
                external_subscriber="my-app"
            )
            ```
        """
        # Convert event types to strings
        if event_types is None:
            event_types_list = ["FORM_RESPONSE"]
        else:
            event_types_list = [
                et.value if isinstance(et, WebhookEventType) else et
                for et in event_types
            ]

        # Build payload
        payload = {
            "formId": form_id,
            "url": url,
            "eventTypes": event_types_list,
        }

        if signing_secret is not None:
            payload["signingSecret"] = signing_secret

        if http_headers is not None:
            # Convert WebhookHeader objects to dicts
            headers_list = []
            for header in http_headers:
                if isinstance(header, WebhookHeader):
                    headers_list.append({"name": header.name, "value": header.value})
                else:
                    headers_list.append(header)
            payload["httpHeaders"] = headers_list

        if external_subscriber is not None:
            payload["externalSubscriber"] = external_subscriber

        data = self._client.request("POST", "/webhooks", json=payload)
        return WebhookCreated.from_dict(data)

    def update(
        self,
        webhook_id: str,
        form_id: str,
        url: str,
        event_types: list[WebhookEventType] | list[str],
        is_enabled: bool,
        signing_secret: str | None = None,
        http_headers: list[WebhookHeader] | list[dict[str, str]] | None = None,
    ) -> None:
        """Update an existing webhook configuration.

        Updates all webhook settings. All required fields must be provided.

        Args:
            webhook_id: The ID of the webhook to update
            form_id: The ID of the form the webhook is for
            url: The URL to send webhook events to
            event_types: Types of events to receive. Can be:
                - List of WebhookEventType enums: [WebhookEventType.FORM_RESPONSE]
                - List of strings: ["FORM_RESPONSE"]
            is_enabled: Whether the webhook is enabled
            signing_secret: Optional secret used to sign webhook payloads
            http_headers: Optional custom HTTP headers. Can be:
                - List of WebhookHeader objects
                - List of dicts with 'name' and 'value' keys

        Example:
            ```python
            from tally import Tally

            client = Tally(api_key="tly-xxxx")

            # Update webhook
            client.webhooks.update(
                webhook_id="wh_123",
                form_id="form_456",
                url="https://example.com/new-webhook",
                event_types=["FORM_RESPONSE"],
                is_enabled=True,
                signing_secret="new-secret"
            )
            print("Webhook updated successfully")
            ```
        """
        # Convert event types to strings
        event_types_list = [
            et.value if isinstance(et, WebhookEventType) else et for et in event_types
        ]

        # Build payload
        payload = {
            "formId": form_id,
            "url": url,
            "eventTypes": event_types_list,
            "isEnabled": is_enabled,
        }

        if signing_secret is not None:
            payload["signingSecret"] = signing_secret

        if http_headers is not None:
            # Convert WebhookHeader objects to dicts
            headers_list = []
            for header in http_headers:
                if isinstance(header, WebhookHeader):
                    headers_list.append({"name": header.name, "value": header.value})
                else:
                    headers_list.append(header)
            payload["httpHeaders"] = headers_list

        self._client.request("PATCH", f"/webhooks/{webhook_id}", json=payload)

    def delete(self, webhook_id: str) -> None:
        """Delete a webhook.

        Deletes a webhook. If this is the last webhook for a form, the webhooks
        integration will also be marked as deleted.

        Args:
            webhook_id: The ID of the webhook to delete

        Raises:
            NotFoundError: If the webhook is not found

        Example:
            ```python
            from tally import Tally

            client = Tally(api_key="tly-xxxx")
            client.webhooks.delete("wh_123")
            print("Webhook deleted successfully")
            ```
        """
        self._client.request("DELETE", f"/webhooks/{webhook_id}")

    def get_events(self, webhook_id: str, page: int = 1) -> PaginatedWebhookEvents:
        """Get webhook delivery events.

        Returns a paginated list of webhook delivery events for a specific webhook,
        including delivery status, response codes, and retry information.

        Args:
            webhook_id: The ID of the webhook
            page: Page number for pagination (default: 1)

        Returns:
            PaginatedWebhookEvents object containing events and pagination info

        Raises:
            NotFoundError: If the webhook is not found

        Example:
            ```python
            from tally import Tally

            client = Tally(api_key="tly-xxxx")

            # Get first page of events
            result = client.webhooks.get_events("wh_123")
            print(f"Total events: {result.total_number_of_events}")

            for event in result.events:
                print(f"Event: {event.id}")
                print(f"  Status: {event.delivery_status.value}")
                print(f"  HTTP Status: {event.status_code}")
                print(f"  Retries: {event.retry}")

            # Get next page
            if result.has_more:
                next_page = client.webhooks.get_events("wh_123", page=2)
            ```
        """
        params = {"page": page}
        data = self._client.request(
            "GET", f"/webhooks/{webhook_id}/events", params=params
        )
        return PaginatedWebhookEvents.from_dict(data)

    def retry_event(self, webhook_id: str, event_id: str) -> None:
        """Retry sending a failed webhook event.

        Retries sending a failed webhook event. This will attempt to deliver the
        webhook payload again to the configured endpoint.

        Note: Failed webhook events are automatically retried up to 5 times with
        exponential backoff intervals (5 minutes, 30 minutes, 1 hour, 6 hours, 24 hours)
        before being permanently dropped.

        Args:
            webhook_id: The ID of the webhook
            event_id: The ID of the webhook event to retry

        Raises:
            NotFoundError: If the webhook or event is not found

        Example:
            ```python
            from tally import Tally

            client = Tally(api_key="tly-xxxx")

            # Retry a failed event
            client.webhooks.retry_event("wh_123", "evt_456")
            print("Event retry initiated successfully")
            ```
        """
        self._client.request("POST", f"/webhooks/{webhook_id}/events/{event_id}")
