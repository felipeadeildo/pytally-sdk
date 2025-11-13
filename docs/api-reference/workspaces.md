# Workspaces

The Workspaces resource provides methods to create, retrieve, update, and delete workspaces.

## Initialization

```python
from tally import Tally

client = Tally(api_key="tly_your_api_key_here")
```

## List Workspaces

Retrieve a paginated list of workspaces.

### Method

```python
client.workspaces.all(page: int = 1) -> PaginatedWorkspaces
```

### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `page` | `int` | No | `1` | Page number for pagination |

### Returns

[`PaginatedWorkspaces`](#paginatedworkspaces-model) object containing:

- `data`: List of [`Workspace`](#workspace-model) objects
- `page`: Current page number
- `total_pages`: Total number of pages

### Example

```python
from tally import Tally

client = Tally(api_key="tly_your_api_key_here")

# Get first page of workspaces
workspaces = client.workspaces.all(page=1)

print(f"Page {workspaces.page} of {workspaces.total_pages}")
for workspace in workspaces.data:
    print(f"Workspace: {workspace.name} (ID: {workspace.id})")
```

### Iteration Support

The workspaces resource supports automatic pagination through iteration:

```python
from tally import Tally

client = Tally(api_key="tly_your_api_key_here")

# Iterate through all workspaces automatically
for workspace in client.workspaces:
    print(f"Workspace: {workspace.name}")
    print(f"  Forms: {workspace.form_count}")
```

### Official Reference

[List Workspaces](https://developers.tally.so/api-reference/endpoint/workspaces/list)

---

## Create Workspace

Create a new workspace.

### Method

```python
client.workspaces.create(name: str) -> Workspace
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | `str` | Yes | The workspace name |

### Returns

Created [`Workspace`](#workspace-model) object.

### Example

```python
from tally import Tally

client = Tally(api_key="tly_your_api_key_here")

# Create a new workspace
workspace = client.workspaces.create(name="Marketing Team")

print(f"Created workspace: {workspace.name}")
print(f"Workspace ID: {workspace.id}")
```

### Errors

| Exception | Status Code | Description |
|-----------|-------------|-------------|
| [`BadRequestError`](../error-handling.md#badrequesterror-400) | 400 | Invalid workspace name |

### Official Reference

[Create Workspace](https://developers.tally.so/api-reference/endpoint/workspaces/post)

---

## Get Workspace

Retrieve a specific workspace by ID.

### Method

```python
client.workspaces.get(workspace_id: str) -> Workspace
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `workspace_id` | `str` | Yes | The workspace ID |

### Returns

[`Workspace`](#workspace-model) object.

### Example

```python
from tally import Tally

client = Tally(api_key="tly_your_api_key_here")

# Get a specific workspace
workspace = client.workspaces.get(workspace_id="wksp_abc123")

print(f"Workspace: {workspace.name}")
print(f"Forms: {workspace.form_count}")
print(f"Created: {workspace.created_at}")
```

### Errors

| Exception | Status Code | Description |
|-----------|-------------|-------------|
| [`NotFoundError`](../error-handling.md#notfounderror-404) | 404 | Workspace not found |

### Official Reference

[Get Workspace](https://developers.tally.so/api-reference/endpoint/workspaces/get)

---

## Update Workspace

Update a workspace's name.

### Method

```python
client.workspaces.update(
    workspace_id: str,
    name: str
) -> None
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `workspace_id` | `str` | Yes | The workspace ID |
| `name` | `str` | Yes | The new workspace name |

### Returns

`None` (successful update returns no content)

### Example

```python
from tally import Tally

client = Tally(api_key="tly_your_api_key_here")

# Update workspace name
client.workspaces.update(
    workspace_id="wksp_abc123",
    name="Marketing & Sales Team"
)

print("Workspace updated successfully")
```

### Errors

| Exception | Status Code | Description |
|-----------|-------------|-------------|
| [`NotFoundError`](../error-handling.md#notfounderror-404) | 404 | Workspace not found |
| [`BadRequestError`](../error-handling.md#badrequesterror-400) | 400 | Invalid workspace name |

### Official Reference

[Update Workspace](https://developers.tally.so/api-reference/endpoint/workspaces/patch)

---

## Delete Workspace

Delete a workspace permanently.

### Method

```python
client.workspaces.delete(workspace_id: str) -> None
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `workspace_id` | `str` | Yes | The workspace ID |

### Returns

`None` (successful deletion returns no content)

### Example

```python
from tally import Tally

client = Tally(api_key="tly_your_api_key_here")

# Delete a workspace
client.workspaces.delete(workspace_id="wksp_abc123")

print("Workspace deleted successfully")
```

### Errors

| Exception | Status Code | Description |
|-----------|-------------|-------------|
| [`NotFoundError`](../error-handling.md#notfounderror-404) | 404 | Workspace not found |

!!! warning "Permanent Deletion"
    Deleting a workspace is permanent and cannot be undone. All forms in the workspace will also be deleted.

### Official Reference

[Delete Workspace](https://developers.tally.so/api-reference/endpoint/workspaces/workspaceId/delete)

---

## Models

### Workspace Model

::: tally.models.workspace.Workspace
    options:
      show_source: false
      heading_level: 4
      members: []

**Example:**

```python
Workspace(
    id="wksp_abc123",
    name="Marketing Team",
    form_count=15,
    created_at="2024-01-15T10:30:00Z"
)
```

### PaginatedWorkspaces Model

::: tally.models.workspace.PaginatedWorkspaces
    options:
      show_source: false
      heading_level: 4
      members: []

**Example:**

```python
PaginatedWorkspaces(
    data=[workspace1, workspace2, ...],
    page=1,
    total_pages=3
)
```

## Complete Example

```python
from tally import Tally, NotFoundError, BadRequestError

client = Tally(api_key="tly_your_api_key_here")

# Create a new workspace
try:
    workspace = client.workspaces.create(name="Product Team")
    print(f"Created: {workspace.name} (ID: {workspace.id})")
except BadRequestError as e:
    print(f"Failed to create workspace: {e.message}")

# List all workspaces
print("\nAll workspaces:")
for workspace in client.workspaces:
    print(f"  - {workspace.name}: {workspace.form_count} forms")

# Get specific workspace
try:
    workspace = client.workspaces.get(workspace_id="wksp_abc123")
    print(f"\nWorkspace details:")
    print(f"  Name: {workspace.name}")
    print(f"  Forms: {workspace.form_count}")
    print(f"  Created: {workspace.created_at}")
except NotFoundError:
    print("Workspace not found")

# Update workspace
try:
    client.workspaces.update(
        workspace_id="wksp_abc123",
        name="Product & Engineering Team"
    )
    print("\nWorkspace updated successfully")
except NotFoundError:
    print("Workspace not found")

# Delete workspace (use with caution!)
try:
    client.workspaces.delete(workspace_id="wksp_old123")
    print("\nWorkspace deleted")
except NotFoundError:
    print("Workspace not found")
```

## Use Cases

### Organize Forms by Department

```python
from tally import Tally

client = Tally(api_key="tly_your_api_key_here")

# Create workspaces for different departments
departments = ["Sales", "Marketing", "Support", "HR"]

for dept in departments:
    workspace = client.workspaces.create(name=f"{dept} Team")
    print(f"Created workspace for {dept}: {workspace.id}")
```

### Audit Workspace Usage

```python
from tally import Tally

client = Tally(api_key="tly_your_api_key_here")

# Get statistics on workspace usage
total_forms = 0
workspaces_data = []

for workspace in client.workspaces:
    total_forms += workspace.form_count
    workspaces_data.append({
        "name": workspace.name,
        "forms": workspace.form_count
    })

print(f"Total workspaces: {len(workspaces_data)}")
print(f"Total forms: {total_forms}")
print("\nWorkspace breakdown:")
for ws in sorted(workspaces_data, key=lambda x: x["forms"], reverse=True):
    print(f"  {ws['name']}: {ws['forms']} forms")
```

## Next Steps

- [Forms](forms.md) - Create and manage forms
- [Webhooks](webhooks.md) - Set up webhook integrations
- [Users](users.md) - Get user information