# Users

The Users resource provides methods to retrieve information about the authenticated user.

## Initialization

Before using any resource, initialize the [`TallyClient`](../index.md#configuration-options):

```python
from tally import Tally

client = Tally(api_key="tly_your_api_key_here")
```

## Get Current User

Retrieve information about the authenticated user.

### Method

```python
client.users.me() -> User
```

### Returns

[`User`](#user-model) object containing:

- `id` (str): User ID
- `email` (str): User email address
- `full_name` (str): User's full name
- `organization_id` (str): Associated organization ID
- `subscription_plan` ([`SubscriptionPlan`](#subscriptionplan)): Current subscription plan
- `created_at` (str): Account creation timestamp

### Example

```python
from tally import Tally

client = Tally(api_key="tly_your_api_key_here")

# Get current user information
user = client.users.me()

print(f"User ID: {user.id}")
print(f"Name: {user.full_name}")
print(f"Email: {user.email}")
print(f"Organization: {user.organization_id}")
print(f"Plan: {user.subscription_plan.value}")
print(f"Member since: {user.created_at}")
```

### Errors

| Exception | Status Code | Description |
|-----------|-------------|-------------|
| [`UnauthorizedError`](../error-handling.md#unauthorizederror-401) | 401 | Invalid or missing API key |
| [`TallyConnectionError`](../error-handling.md#tallyconnectionerror) | - | Network connection error |
| [`TallyTimeoutError`](../error-handling.md#tallytimeouterror) | - | Request timeout |

### Example with Error Handling

```python
from tally import Tally, UnauthorizedError, TallyAPIError

client = Tally(api_key="tly_your_api_key_here")

try:
    user = client.users.me()
    print(f"Welcome, {user.full_name}!")
except UnauthorizedError:
    print("Invalid API key. Please check your credentials.")
except TallyAPIError as e:
    print(f"API error: {e.message}")
```

## Models

### User Model

::: tally.models.user.User
    options:
      show_source: false
      heading_level: 4
      members: []

**Example:**

```python
User(
    id="usr_abc123",
    email="john@example.com",
    full_name="John Doe",
    organization_id="org_xyz789",
    subscription_plan=SubscriptionPlan.PRO,
    created_at="2024-01-15T10:30:00Z"
)
```

### SubscriptionPlan

::: tally.models.user.SubscriptionPlan
    options:
      show_source: false
      heading_level: 4

**Values:**

- `FREE`: Free plan
- `PRO`: Professional plan
- `BUSINESS`: Business plan

## Official API Reference

For more details, see the [Official Tally API Documentation](https://developers.tally.so/api-reference/endpoint/users/me/get).

## Next Steps

- [Organizations](organizations.md) - Manage organization users and invites
- [Forms](forms.md) - Create and manage forms
- [Workspaces](workspaces.md) - Manage workspaces