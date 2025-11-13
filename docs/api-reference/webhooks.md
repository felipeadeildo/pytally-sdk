# Webhooks

The Webhooks resource provides methods to create, manage, and monitor webhook integrations.

## Initialization

```python
from tally import Tally

client = Tally(api_key="tly_your_api_key_here")
```

## List Webhooks

Retrieve a paginated list of webhooks.

### Method

```python
client.webhooks.all(
    page: int = 1,
    limit: int = 25
) -> PaginatedWebhooks
```

### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `page` | `int` | No | `1` | Page number for pagination |
| `limit` | `int` | No | `25` | Items per page (max: 100) |

### Returns

[`PaginatedWebhooks`](#paginatedwebhooks-model) object containing:

- `data`: List of [`Webhook`](#webhook-model) objects
- `page`: Current page number
- `total_pages`: Total number of pages

### Example

```python
from tally import Tally

client = Tally(api_key="tly_your_api_key_here")

# Get first page of webhooks
webhooks = client.webhooks.all(page=1, limit=10)

print(f"Page {webhooks.page} of {webhooks.total_pages}")
for webhook in webhooks.data:
    print(f"Webhook: {webhook.name}")
    print(f"  URL: {webhook.url}")
    print(f"  Events: {', '.join(webhook.event_types)}")
```

### Iteration Support

The webhooks resource supports automatic pagination through iteration:

```python
from tally import Tally

client = Tally(api_key="tly_your_api_key_here")

# Iterate through all webhooks automatically
for webhook in client.webhooks:
    print(f"Webhook: {webhook.name} -> {webhook.url}")
```

### Official Reference

[List Webhooks](https://developers.tally.so/api-reference/endpoint/webhooks/get)

---

## Create Webhook

Create a new webhook to receive events.

### Method

```python
client.webhooks.create(
    url: str,
    event_types: list[str],
    form_ids: list[str] | None = None,
    name: str | None = None,
    headers: list[dict[str, str]] | None = None
) -> WebhookCreated
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `url` | `str` | Yes | The webhook endpoint URL |
| `event_types` | `list[str]` | Yes | List of event types to subscribe to |
| `form_ids` | `list[str]` | No | Filter events to specific form IDs |
| `name` | `str` | No | Descriptive name for the webhook |
| `headers` | `list[dict]` | No | Custom HTTP headers for webhook requests |

**Event Types:**

- `form.submitted` - Triggered when a form is submitted
- `form.updated` - Triggered when a form is updated
- `form.deleted` - Triggered when a form is deleted

### Returns

[`WebhookCreated`](#webhookcreated-model) object containing:

- `id`: Webhook ID
- `secret`: Webhook secret for signature verification
- Other webhook details

### Example

```python
from tally import Tally

client = Tally(api_key="tly_your_api_key_here")

# Create a webhook for form submissions
webhook = client.webhooks.create(
    url="https://your-app.com/webhooks/tally",
    event_types=["form.submitted"],
    form_ids=["wXYz123", "aBc456"],
    name="Production Webhook"
)

print(f"Webhook created: {webhook.id}")
print(f"Secret: {webhook.secret}")
print("Store this secret securely for signature verification!")
```

### Example with Custom Headers

```python
from tally import Tally

client = Tally(api_key="tly_your_api_key_here")

# Create webhook with custom authentication header
webhook = client.webhooks.create(
    url="https://your-app.com/webhooks/tally",
    event_types=["form.submitted"],
    name="Authenticated Webhook",
    headers=[
        {"key": "Authorization", "value": "Bearer your-token"},
        {"key": "X-Custom-Header", "value": "custom-value"}
    ]
)

print(f"Webhook created with custom headers: {webhook.id}")
```

### Errors

| Exception | Status Code | Description |
|-----------|-------------|-------------|
| [`BadRequestError`](../error-handling.md#badrequesterror-400) | 400 | Invalid URL or event types |

### Official Reference

[Create Webhook](https://developers.tally.so/api-reference/endpoint/webhooks/post)

---

## Update Webhook

Update an existing webhook's configuration.

### Method

```python
client.webhooks.update(
    webhook_id: str,
    url: str | None = None,
    event_types: list[str] | None = None,
    form_ids: list[str] | None = None,
    name: str | None = None,
    headers: list[dict[str, str]] | None = None,
    is_enabled: bool | None = None
) -> None
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `webhook_id` | `str` | Yes | The webhook ID |
| `url` | `str` | No | New webhook URL |
| `event_types` | `list[str]` | No | New event types |
| `form_ids` | `list[str]` | No | New form ID filters |
| `name` | `str` | No | New webhook name |
| `headers` | `list[dict]` | No | New custom headers |
| `is_enabled` | `bool` | No | Enable/disable the webhook |

### Returns

`None` (successful update returns no content)

### Example

```python
from tally import Tally

client = Tally(api_key="tly_your_api_key_here")

# Update webhook URL
client.webhooks.update(
    webhook_id="whk_abc123",
    url="https://new-endpoint.com/webhooks"
)

print("Webhook updated successfully")
```

### Example: Disable Webhook

```python
from tally import Tally

client = Tally(api_key="tly_your_api_key_here")

# Temporarily disable a webhook
client.webhooks.update(
    webhook_id="whk_abc123",
    is_enabled=False
)

print("Webhook disabled")
```

### Official Reference

[Update Webhook](https://developers.tally.so/api-reference/endpoint/webhooks/patch)

---

## Delete Webhook

Delete a webhook permanently.

### Method

```python
client.webhooks.delete(webhook_id: str) -> None
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `webhook_id` | `str` | Yes | The webhook ID |

### Returns

`None` (successful deletion returns no content)

### Example

```python
from tally import Tally

client = Tally(api_key="tly_your_api_key_here")

# Delete a webhook
client.webhooks.delete(webhook_id="whk_abc123")

print("Webhook deleted successfully")
```

### Official Reference

[Delete Webhook](https://developers.tally.so/api-reference/endpoint/webhooks/delete)

---

## Get Webhook Events

Retrieve delivery events for a webhook.

### Method

```python
client.webhooks.get_events(
    webhook_id: str,
    page: int = 1
) -> PaginatedWebhookEvents
```

### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `webhook_id` | `str` | Yes | - | The webhook ID |
| `page` | `int` | No | `1` | Page number for pagination |

### Returns

[`PaginatedWebhookEvents`](#paginatedwebhookevents-model) object containing:

- `data`: List of [`WebhookEvent`](#webhookevent-model) objects
- `page`: Current page number
- `total_pages`: Total number of pages

### Example

```python
from tally import Tally

client = Tally(api_key="tly_your_api_key_here")

# Get webhook events
events = client.webhooks.get_events(webhook_id="whk_abc123", page=1)

for event in events.data:
    print(f"Event: {event.event_type}")
    print(f"  Status: {event.status}")
    print(f"  Response: {event.response_status_code}")
    print(f"  Timestamp: {event.created_at}")
```

### Official Reference

[List Webhook Events](https://developers.tally.so/api-reference/endpoint/webhooks/events/get)

---

## Retry Webhook Event

Retry a failed webhook event delivery.

### Method

```python
client.webhooks.retry_event(
    webhook_id: str,
    event_id: str
) -> None
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `webhook_id` | `str` | Yes | The webhook ID |
| `event_id` | `str` | Yes | The event ID to retry |

### Returns

`None` (retry is queued, no immediate response)

### Example

```python
from tally import Tally

client = Tally(api_key="tly_your_api_key_here")

# Get failed events
events = client.webhooks.get_events(webhook_id="whk_abc123")

# Retry failed events
for event in events.data:
    if event.status == "failed":
        client.webhooks.retry_event(
            webhook_id="whk_abc123",
            event_id=event.id
        )
        print(f"Retrying event {event.id}")
```

### Official Reference

[Retry Webhook Event](https://developers.tally.so/api-reference/endpoint/webhooks/events/retry)

---

## Models

### Webhook Model

::: tally.models.webhook.Webhook
    options:
      show_source: false
      heading_level: 4
      members: []

**Example:**

```python
Webhook(
    id="whk_abc123",
    url="https://your-app.com/webhooks",
    event_types=["form.submitted"],
    form_ids=["wXYz123"],
    name="Production Webhook",
    is_enabled=True,
    created_at="2024-01-15T10:30:00Z"
)
```

### WebhookCreated Model

::: tally.models.webhook.WebhookCreated
    options:
      show_source: false
      heading_level: 4
      members: []

**Example:**

```python
WebhookCreated(
    id="whk_abc123",
    secret="whsec_abc123def456...",
    url="https://your-app.com/webhooks"
)
```

### WebhookEvent Model

::: tally.models.webhook.WebhookEvent
    options:
      show_source: false
      heading_level: 4
      members: []

**Example:**

```python
WebhookEvent(
    id="evt_abc123",
    event_type="form.submitted",
    status="delivered",
    response_status_code=200,
    created_at="2024-01-15T10:30:00Z"
)
```

### WebhookEventType

::: tally.models.webhook.WebhookEventType
    options:
      show_source: false
      heading_level: 4

**Values:**

- `FORM_SUBMITTED`: Form submission event
- `FORM_UPDATED`: Form update event
- `FORM_DELETED`: Form deletion event

### PaginatedWebhooks Model

::: tally.models.webhook.PaginatedWebhooks
    options:
      show_source: false
      heading_level: 4
      members: []

### PaginatedWebhookEvents Model

::: tally.models.webhook.PaginatedWebhookEvents
    options:
      show_source: false
      heading_level: 4
      members: []

## Complete Example

```python
from tally import Tally, BadRequestError

client = Tally(api_key="tly_your_api_key_here")

# Create a webhook
try:
    webhook = client.webhooks.create(
        url="https://your-app.com/webhooks/tally",
        event_types=["form.submitted"],
        form_ids=["wXYz123"],
        name="My Webhook",
        headers=[
            {"key": "Authorization", "value": "Bearer your-token"}
        ]
    )
    print(f"Webhook created: {webhook.id}")
    print(f"Secret: {webhook.secret}")
except BadRequestError as e:
    print(f"Failed to create webhook: {e.message}")

# List all webhooks
print("\nAll webhooks:")
for webhook in client.webhooks:
    status = "enabled" if webhook.is_enabled else "disabled"
    print(f"  - {webhook.name} ({status})")
    print(f"    Events: {', '.join(webhook.event_types)}")

# Monitor webhook events
webhook_id = "whk_abc123"
events = client.webhooks.get_events(webhook_id=webhook_id)

print(f"\nWebhook events for {webhook_id}:")
failed_count = 0
for event in events.data:
    print(f"  - {event.event_type}: {event.status}")
    if event.status == "failed":
        failed_count += 1

# Retry failed events
if failed_count > 0:
    print(f"\nRetrying {failed_count} failed events...")
    for event in events.data:
        if event.status == "failed":
            client.webhooks.retry_event(
                webhook_id=webhook_id,
                event_id=event.id
            )

# Disable webhook temporarily
client.webhooks.update(
    webhook_id=webhook_id,
    is_enabled=False
)
print("\nWebhook disabled")
```

## Use Cases

### Set Up Form Submission Notifications

```python
from tally import Tally

client = Tally(api_key="tly_your_api_key_here")

# Create webhook for all form submissions
webhook = client.webhooks.create(
    url="https://your-app.com/api/form-submissions",
    event_types=["form.submitted"],
    name="Form Submissions Webhook"
)

print(f"Webhook URL: {webhook.url}")
print(f"Webhook Secret: {webhook.secret}")
print("\nUse this secret to verify webhook signatures in your app!")
```

### Monitor Webhook Health

```python
from tally import Tally
from collections import Counter

client = Tally(api_key="tly_your_api_key_here")

# Check webhook delivery status
for webhook in client.webhooks:
    events = client.webhooks.get_events(webhook_id=webhook.id)
    
    # Count event statuses
    status_counts = Counter(event.status for event in events.data)
    
    print(f"\nWebhook: {webhook.name}")
    print(f"  Delivered: {status_counts.get('delivered', 0)}")
    print(f"  Failed: {status_counts.get('failed', 0)}")
    print(f"  Pending: {status_counts.get('pending', 0)}")
    
    # Alert if too many failures
    if status_counts.get('failed', 0) > 10:
        print(f"  ⚠️ High failure rate detected!")
```

## Next Steps

- [Forms](forms.md) - Manage forms that trigger webhooks
- [Error Handling](../error-handling.md) - Handle webhook errors
- [Users](users.md) - Get user information