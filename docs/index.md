# PyTally SDK

Unofficial Python SDK for the [Tally.so](https://tally.so) API.

[![PyPI version](https://badge.fury.io/py/pytally-sdk.svg)](https://badge.fury.io/py/pytally-sdk)
[![Python Versions](https://img.shields.io/pypi/pyversions/pytally-sdk.svg)](https://pypi.org/project/pytally-sdk/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

## Introduction

PyTally SDK is a Python library that provides a simple and intuitive interface to interact with the Tally.so API. It handles authentication, request/response processing, pagination, and error handling, allowing you to focus on building your application.

### Features

- 🔐 **Bearer Token Authentication** - Secure API key-based authentication
- 📦 **Full Type Hints** - Complete type annotations for better IDE support
- 🔄 **Automatic Pagination** - Built-in iterators for paginated resources
- ⚡ **Pythonic API** - Clean, resource-based interface
- 🛡️ **Comprehensive Error Handling** - Specific exceptions for different error types
- 🔧 **Context Manager Support** - Automatic resource cleanup
- 📊 **API Versioning** - Support for date-based API versioning

### What's Implemented

Currently, the SDK covers the following Tally API resources:

- ✅ **Users** - Get current user information
- ✅ **Organizations** - Manage users and invites
- ✅ **Forms** - Create, update, and manage forms and submissions
- ✅ **Workspaces** - List and manage workspaces
- ✅ **Webhooks** - Configure and monitor webhook integrations

!!! info "Official API Documentation"
    For complete API details and specifications, refer to the [Official Tally API Documentation](https://developers.tally.so/api-reference/introduction).

## Installation

### Using pip

```bash
pip install pytally-sdk
```

### Using uv

[uv](https://github.com/astral-sh/uv) is a fast Python package installer and resolver:

```bash
uv add pytally-sdk
```

### Requirements

- Python 3.11 or higher
- `httpx` library (automatically installed)

## Quickstart

Get started with PyTally SDK in just a few lines of code:

### Basic Usage

```python
from tally import Tally

# Initialize the client with your API key
client = Tally(api_key="tly_your_api_key_here")

# Get current user information
user = client.users.me()
print(f"Hello, {user.full_name}!")
print(f"Email: {user.email}")
print(f"Plan: {user.subscription_plan.value}")
```

### Using Context Manager

The recommended approach for automatic resource cleanup:

```python
from tally import Tally

with Tally(api_key="tly_your_api_key_here") as client:
    # Get current user
    user = client.users.me()
    print(f"Organization ID: {user.organization_id}")

    # List all forms
    for form in client.forms:
        print(f"Form: {form.name} (ID: {form.id})")
```

### Working with Forms

```python
from tally import Tally

client = Tally(api_key="tly_your_api_key_here")

# List forms with pagination
forms = client.forms.all(page=1, limit=10)
print(f"Found {len(forms.data)} forms")

# Get a specific form
form = client.forms.get(form_id="wXYz123")
print(f"Form: {form.name}")
print(f"Status: {form.status}")
print(f"Submissions: {form.submission_count}")

# List form submissions
submissions = client.forms.list_submissions(
    form_id="wXYz123",
    filter="all",
    page=1,
    limit=25
)

for submission in submissions.data:
    print(f"Submission ID: {submission.submission_id}")
    print(f"Created: {submission.created_at}")
```

### Setting up Webhooks

```python
from tally import Tally

client = Tally(api_key="tly_your_api_key_here")

# Create a webhook
webhook = client.webhooks.create(
    url="https://your-app.com/webhooks/tally",
    event_types=["form.submitted"],
    form_ids=["wXYz123"],
    name="My Webhook"
)

print(f"Webhook created: {webhook.id}")
print(f"Secret: {webhook.secret}")

# List webhook events
events = client.webhooks.get_events(webhook_id=webhook.id)
for event in events.data:
    print(f"Event: {event.event_type} - {event.status}")
```

## API Versioning

The Tally API uses date-based versioning. You can specify a specific API version when initializing the client:

```python
from tally import Tally

client = Tally(
    api_key="tly_your_api_key_here",
    api_version="2025-02-01"  # Optional: specify API version
)
```

If not specified, the client will use the version tied to your API key.

## Error Handling

The SDK provides specific exceptions for different error scenarios:

```python
from tally import Tally, UnauthorizedError, RateLimitError, NotFoundError

client = Tally(api_key="tly_your_api_key_here")

try:
    form = client.forms.get(form_id="invalid_id")
except UnauthorizedError:
    print("Invalid API key!")
except NotFoundError:
    print("Form not found!")
except RateLimitError as e:
    print(f"Rate limit exceeded. Try again later.")
    print(f"Status code: {e.status_code}")
```

For more details, see the [Error Handling](error-handling.md) guide.

## Configuration Options

The [`TallyClient`](api-reference/users.md#initialization) accepts the following configuration options:

```python
from tally import Tally

client = Tally(
    api_key="tly_your_api_key_here",       # Required: Your Tally API key
    api_version="2025-02-01",              # Optional: API version (default: key version)
    timeout=30.0,                          # Optional: Request timeout in seconds (default: 30.0)
    base_url="https://api.tally.so"       # Optional: Custom base URL (default: https://api.tally.so)
)
```

## Next Steps

- 🔑 [Get your API Key](api-keys.md) - Learn how to obtain API keys from Tally
- 📖 [API Reference](api-reference/users.md) - Explore all available methods
- ⚠️ [Error Handling](error-handling.md) - Learn about exception handling

## Links

- [PyPI Package](https://pypi.org/project/pytally-sdk/)
- [GitHub Repository](https://github.com/felipeadeildo/pytally)
- [Official Tally API Documentation](https://developers.tally.so/api-reference/introduction)
- [Issue Tracker](https://github.com/felipeadeildo/pytally/issues)

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](https://github.com/felipeadeildo/pytally/blob/main/LICENSE) file for details.

!!! warning "Disclaimer"
    This is an unofficial SDK and is not affiliated with or endorsed by Tally. Tally and the Tally logo are trademarks of Tally B.V.
