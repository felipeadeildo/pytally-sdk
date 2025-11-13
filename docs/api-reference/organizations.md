# Organizations

The Organizations resource provides methods to manage organization members and invitations.

## Initialization

```python
from tally import Tally

client = Tally(api_key="tly_your_api_key_here")
```

## List Organization Users

Retrieve a list of all users in an organization.

### Method

```python
client.organizations.list_users(organization_id: str) -> list[User]
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `organization_id` | `str` | Yes | The organization ID |

### Returns

List of [`User`](users.md#user-model) objects.

### Example

```python
from tally import Tally

client = Tally(api_key="tly_your_api_key_here")

# Get current user to find organization ID
user = client.users.me()

# List all users in the organization
users = client.organizations.list_users(organization_id=user.organization_id)

for member in users:
    print(f"User: {member.full_name} ({member.email})")
    print(f"  Plan: {member.subscription_plan.value}")
```

### Official Reference

[List Organization Users](https://developers.tally.so/api-reference/endpoint/organizations/users/get)

---

## Remove Organization User

Remove a user from an organization.

### Method

```python
client.organizations.remove_user(
    organization_id: str,
    user_id: str
) -> None
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `organization_id` | `str` | Yes | The organization ID |
| `user_id` | `str` | Yes | The user ID to remove |

### Returns

`None` (successful removal returns no content)

### Example

```python
from tally import Tally

client = Tally(api_key="tly_your_api_key_here")

# Remove a user from the organization
client.organizations.remove_user(
    organization_id="org_abc123",
    user_id="usr_xyz789"
)

print("User removed successfully")
```

### Errors

| Exception | Status Code | Description |
|-----------|-------------|-------------|
| [`NotFoundError`](../error-handling.md#notfounderror-404) | 404 | Organization or user not found |
| [`ForbiddenError`](../error-handling.md#forbiddenerror-403) | 403 | Insufficient permissions |

### Official Reference

[Remove Organization User](https://developers.tally.so/api-reference/endpoint/organizations/users/delete)

---

## List Organization Invites

Retrieve all pending invitations for an organization.

### Method

```python
client.organizations.list_invites(organization_id: str) -> list[Invite]
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `organization_id` | `str` | Yes | The organization ID |

### Returns

List of [`Invite`](#invite-model) objects.

### Example

```python
from tally import Tally

client = Tally(api_key="tly_your_api_key_here")

# List all pending invites
invites = client.organizations.list_invites(organization_id="org_abc123")

for invite in invites:
    print(f"Invite ID: {invite.id}")
    print(f"Email: {invite.email}")
    print(f"Status: {invite.status}")
    print(f"Sent: {invite.created_at}")
```

### Official Reference

[List Organization Invites](https://developers.tally.so/api-reference/endpoint/organizations/invites/get)

---

## Create Organization Invites

Send invitations to join an organization.

### Method

```python
client.organizations.create_invites(
    organization_id: str,
    emails: list[str]
) -> list[Invite]
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `organization_id` | `str` | Yes | The organization ID |
| `emails` | `list[str]` | Yes | List of email addresses to invite |

### Returns

List of created [`Invite`](#invite-model) objects.

### Example

```python
from tally import Tally

client = Tally(api_key="tly_your_api_key_here")

# Invite multiple users
invites = client.organizations.create_invites(
    organization_id="org_abc123",
    emails=[
        "alice@example.com",
        "bob@example.com"
    ]
)

for invite in invites:
    print(f"Invited: {invite.email}")
    print(f"Invite ID: {invite.id}")
```

### Errors

| Exception | Status Code | Description |
|-----------|-------------|-------------|
| [`BadRequestError`](../error-handling.md#badrequesterror-400) | 400 | Invalid email format or duplicate invites |
| [`ForbiddenError`](../error-handling.md#forbiddenerror-403) | 403 | Insufficient permissions |

### Example with Error Handling

```python
from tally import Tally, BadRequestError

client = Tally(api_key="tly_your_api_key_here")

try:
    invites = client.organizations.create_invites(
        organization_id="org_abc123",
        emails=["new.user@example.com"]
    )
    print(f"Invitation sent successfully!")
except BadRequestError as e:
    print(f"Failed to send invite: {e.message}")
    for error in e.errors:
        print(f"  - {error}")
```

### Official Reference

[Create Organization Invites](https://developers.tally.so/api-reference/endpoint/organizations/invites/post)

---

## Cancel Organization Invite

Cancel a pending organization invitation.

### Method

```python
client.organizations.cancel_invite(
    organization_id: str,
    invite_id: str
) -> None
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `organization_id` | `str` | Yes | The organization ID |
| `invite_id` | `str` | Yes | The invite ID to cancel |

### Returns

`None` (successful cancellation returns no content)

### Example

```python
from tally import Tally

client = Tally(api_key="tly_your_api_key_here")

# Cancel a pending invite
client.organizations.cancel_invite(
    organization_id="org_abc123",
    invite_id="inv_xyz789"
)

print("Invite cancelled successfully")
```

### Errors

| Exception | Status Code | Description |
|-----------|-------------|-------------|
| [`NotFoundError`](../error-handling.md#notfounderror-404) | 404 | Invite not found |

### Official Reference

[Cancel Organization Invite](https://developers.tally.so/api-reference/endpoint/organizations/invites/inviteId/delete)

---

## Models

### Invite Model

::: tally.models.invite.Invite
    options:
      show_source: false
      heading_level: 4
      members: []

**Example:**

```python
Invite(
    id="inv_abc123",
    email="newuser@example.com",
    status="pending",
    created_at="2024-01-15T10:30:00Z"
)
```

## Complete Example

```python
from tally import Tally, BadRequestError, NotFoundError

client = Tally(api_key="tly_your_api_key_here")

# Get organization ID from current user
user = client.users.me()
org_id = user.organization_id

# List current members
print("Current members:")
members = client.organizations.list_users(organization_id=org_id)
for member in members:
    print(f"  - {member.full_name} ({member.email})")

# Send invitations
try:
    print("\nSending invitations...")
    invites = client.organizations.create_invites(
        organization_id=org_id,
        emails=["newuser@example.com"]
    )
    print(f"Sent {len(invites)} invitation(s)")
except BadRequestError as e:
    print(f"Failed to send invites: {e.message}")

# List pending invites
print("\nPending invites:")
invites = client.organizations.list_invites(organization_id=org_id)
for invite in invites:
    print(f"  - {invite.email} (ID: {invite.id})")

# Cancel an invite if needed
if invites:
    try:
        client.organizations.cancel_invite(
            organization_id=org_id,
            invite_id=invites[0].id
        )
        print(f"\nCancelled invite for {invites[0].email}")
    except NotFoundError:
        print("Invite not found")
```

## Next Steps

- [Users](users.md) - Get user information
- [Forms](forms.md) - Manage forms
- [Workspaces](workspaces.md) - Manage workspaces