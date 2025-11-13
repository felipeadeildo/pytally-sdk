# Forms

The Forms resource provides comprehensive methods to create, manage, and interact with forms and their submissions.

## Initialization

```python
from tally import Tally

client = Tally(api_key="tly_your_api_key_here")
```

## List Forms

Retrieve a paginated list of forms.

### Method

```python
client.forms.all(
    page: int = 1,
    limit: int = 25,
    workspace_id: str | None = None
) -> PaginatedForms
```

### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `page` | `int` | No | `1` | Page number for pagination |
| `limit` | `int` | No | `25` | Items per page (max: 100) |
| `workspace_id` | `str` | No | `None` | Filter by workspace ID |

### Returns

[`PaginatedForms`](#paginatedforms-model) object containing:

- `data`: List of [`Form`](#form-model) objects
- `page`: Current page number
- `total_pages`: Total number of pages

### Example

```python
from tally import Tally

client = Tally(api_key="tly_your_api_key_here")

# Get first page of forms
forms = client.forms.all(page=1, limit=10)

print(f"Page {forms.page} of {forms.total_pages}")
for form in forms.data:
    print(f"Form: {form.name} (ID: {form.id})")
    print(f"  Status: {form.status}")
    print(f"  Submissions: {form.submission_count}")
```

### Filtering by Workspace

```python
# Get forms from a specific workspace
forms = client.forms.all(workspace_id="wksp_abc123")

for form in forms.data:
    print(f"Form: {form.name}")
```

### Iteration Support

The forms resource supports automatic pagination through iteration:

```python
# Iterate through all forms automatically
for form in client.forms:
    print(f"{form.name}: {form.submission_count} submissions")
```

### Official Reference

[List Forms](https://developers.tally.so/api-reference/endpoint/forms/list)

---

## Create Form

Create a new form with blocks and settings.

### Method

```python
client.forms.create(
    name: str,
    workspace_id: str,
    blocks: list[dict] | None = None,
    settings: dict | None = None
) -> FormCreated
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | `str` | Yes | The form name |
| `workspace_id` | `str` | Yes | The workspace ID where the form will be created |
| `blocks` | `list[dict]` | No | List of form blocks (questions, text, images, etc.) |
| `settings` | `dict` | No | Form settings configuration |

### Returns

[`FormCreated`](#formcreated-model) object containing the created form's ID and edit URL.

### Example: Simple Form

```python
from tally import Tally

client = Tally(api_key="tly_your_api_key_here")

# Create a basic form
form = client.forms.create(
    name="Customer Feedback",
    workspace_id="wksp_abc123"
)

print(f"Form created: {form.id}")
print(f"Edit URL: {form.edit_url}")
```

### Example: Form with Blocks

```python
from tally import Tally

client = Tally(api_key="tly_your_api_key_here")

# Create a form with questions
form = client.forms.create(
    name="Contact Form",
    workspace_id="wksp_abc123",
    blocks=[
        {
            "type": "INPUT_TEXT",
            "payload": {
                "text": [{"type": "p", "children": [{"text": "What's your name?"}]}],
                "required": True
            }
        },
        {
            "type": "INPUT_EMAIL",
            "payload": {
                "text": [{"type": "p", "children": [{"text": "Your email address"}]}],
                "required": True
            }
        },
        {
            "type": "TEXTAREA",
            "payload": {
                "text": [{"type": "p", "children": [{"text": "Your message"}]}],
                "required": False
            }
        }
    ]
)

print(f"Form created with {len(form.blocks) if hasattr(form, 'blocks') else 0} blocks")
```

### Example: Form with Settings

```python
from tally import Tally

client = Tally(api_key="tly_your_api_key_here")

# Create form with custom settings
form = client.forms.create(
    name="Survey 2024",
    workspace_id="wksp_abc123",
    settings={
        "submitButtonText": "Send Response",
        "showProgressBar": True,
        "autoSave": True,
        "respondOnce": True
    }
)

print(f"Form created: {form.id}")
```

### Official Reference

[Create Form](https://developers.tally.so/api-reference/endpoint/forms/post)

---

## Get Form

Retrieve detailed information about a specific form.

### Method

```python
client.forms.get(form_id: str) -> FormDetails
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `form_id` | `str` | Yes | The form ID |

### Returns

[`FormDetails`](#formdetails-model) object with complete form information including blocks and settings.

### Example

```python
from tally import Tally

client = Tally(api_key="tly_your_api_key_here")

# Get form details
form = client.forms.get(form_id="wXYz123")

print(f"Form: {form.name}")
print(f"Status: {form.status}")
print(f"Submissions: {form.submission_count}")
print(f"Created: {form.created_at}")
print(f"Blocks: {len(form.blocks)}")

# Access form blocks
for block in form.blocks:
    print(f"  Block type: {block.type}")
```

### Official Reference

[Get Form](https://developers.tally.so/api-reference/endpoint/forms/get)

---

## Update Form

Update a form's name, blocks, or settings.

### Method

```python
client.forms.update(
    form_id: str,
    name: str | None = None,
    blocks: list[dict] | None = None,
    settings: dict | None = None
) -> None
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `form_id` | `str` | Yes | The form ID |
| `name` | `str` | No | New form name |
| `blocks` | `list[dict]` | No | Updated form blocks |
| `settings` | `dict` | No | Updated form settings |

### Returns

`None` (successful update returns no content)

### Example: Update Name

```python
from tally import Tally

client = Tally(api_key="tly_your_api_key_here")

# Update form name
client.forms.update(
    form_id="wXYz123",
    name="Customer Feedback 2024"
)

print("Form updated successfully")
```

### Example: Update Settings

```python
from tally import Tally

client = Tally(api_key="tly_your_api_key_here")

# Update form settings
client.forms.update(
    form_id="wXYz123",
    settings={
        "respondOnce": True,
        "showProgressBar": True,
        "submitButtonText": "Submit Your Response"
    }
)

print("Form settings updated")
```

### Official Reference

[Update Form](https://developers.tally.so/api-reference/endpoint/forms/patch)

---

## Delete Form

Delete a form permanently.

### Method

```python
client.forms.delete(form_id: str) -> None
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `form_id` | `str` | Yes | The form ID |

### Returns

`None` (successful deletion returns no content)

### Example

```python
from tally import Tally

client = Tally(api_key="tly_your_api_key_here")

# Delete a form
client.forms.delete(form_id="wXYz123")

print("Form deleted successfully")
```

!!! warning "Permanent Deletion"
    Deleting a form is permanent and cannot be undone. All submissions will also be deleted.

### Official Reference

[Delete Form](https://developers.tally.so/api-reference/endpoint/forms/delete)

---

## List Form Questions

Retrieve all questions from a form.

### Method

```python
client.forms.list_questions(form_id: str) -> list[Question]
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `form_id` | `str` | Yes | The form ID |

### Returns

List of [`Question`](#question-model) objects.

### Example

```python
from tally import Tally

client = Tally(api_key="tly_your_api_key_here")

# Get all questions from a form
questions = client.forms.list_questions(form_id="wXYz123")

for question in questions:
    print(f"Question: {question.title}")
    print(f"  Type: {question.type}")
    print(f"  Required: {question.required}")
    if question.fields:
        for field in question.fields:
            print(f"  Field: {field.key} ({field.type})")
```

### Official Reference

[List Questions](https://developers.tally.so/api-reference/endpoint/forms/questions/list)

---

## List Form Submissions

Retrieve submissions for a form with filtering and pagination.

### Method

```python
client.forms.list_submissions(
    form_id: str,
    filter: str = "all",
    page: int = 1,
    limit: int = 25,
    since: str | None = None,
    until: str | None = None
) -> PaginatedSubmissions
```

### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `form_id` | `str` | Yes | - | The form ID |
| `filter` | `str` | No | `"all"` | Filter type: `"all"`, `"completed"`, `"partial"`, `"spam"` |
| `page` | `int` | No | `1` | Page number |
| `limit` | `int` | No | `25` | Items per page (max: 100) |
| `since` | `str` | No | `None` | ISO 8601 date for start of range |
| `until` | `str` | No | `None` | ISO 8601 date for end of range |

### Returns

[`PaginatedSubmissions`](#paginatedsubmissions-model) object with submission data and counts.

### Example

```python
from tally import Tally

client = Tally(api_key="tly_your_api_key_here")

# Get all submissions
submissions = client.forms.list_submissions(
    form_id="wXYz123",
    filter="all",
    page=1,
    limit=50
)

print(f"Total submissions: {submissions.filter_count.all}")
print(f"Completed: {submissions.filter_count.completed}")
print(f"Partial: {submissions.filter_count.partial}")

for submission in submissions.data:
    print(f"Submission: {submission.submission_id}")
    print(f"  Created: {submission.created_at}")
```

### Example: Filter by Date Range

```python
from tally import Tally

client = Tally(api_key="tly_your_api_key_here")

# Get submissions from last week
submissions = client.forms.list_submissions(
    form_id="wXYz123",
    filter="completed",
    since="2024-01-01T00:00:00Z",
    until="2024-01-07T23:59:59Z"
)

print(f"Submissions in date range: {len(submissions.data)}")
```

### Official Reference

[List Submissions](https://developers.tally.so/api-reference/endpoint/forms/submissions/list)

---

## Get Form Submission

Retrieve a specific submission with all responses.

### Method

```python
client.forms.get_submission(
    form_id: str,
    submission_id: str
) -> SubmissionWithQuestions
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `form_id` | `str` | Yes | The form ID |
| `submission_id` | `str` | Yes | The submission ID |

### Returns

[`SubmissionWithQuestions`](#submissionwithquestions-model) object containing submission data and questions.

### Example

```python
from tally import Tally

client = Tally(api_key="tly_your_api_key_here")

# Get specific submission
submission = client.forms.get_submission(
    form_id="wXYz123",
    submission_id="sub_abc456"
)

print(f"Submission ID: {submission.submission.submission_id}")
print(f"Created: {submission.submission.created_at}")

# Access responses
for response in submission.submission.responses:
    question_key = response.key
    answer = response.value
    print(f"{question_key}: {answer}")
```

### Official Reference

[Get Submission](https://developers.tally.so/api-reference/endpoint/forms/submissions/get)

---

## Delete Form Submission

Delete a specific submission from a form.

### Method

```python
client.forms.delete_submission(
    form_id: str,
    submission_id: str
) -> None
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `form_id` | `str` | Yes | The form ID |
| `submission_id` | `str` | Yes | The submission ID to delete |

### Returns

`None` (successful deletion returns no content)

### Example

```python
from tally import Tally

client = Tally(api_key="tly_your_api_key_here")

# Delete a submission
client.forms.delete_submission(
    form_id="wXYz123",
    submission_id="sub_abc456"
)

print("Submission deleted successfully")
```

### Official Reference

[Delete Submission](https://developers.tally.so/api-reference/endpoint/forms/submissions/delete)

---

## Models

### Form Model

::: tally.models.form.Form
    options:
      show_source: false
      heading_level: 4
      members: []

### FormCreated Model

::: tally.models.form.FormCreated
    options:
      show_source: false
      heading_level: 4
      members: []

### FormDetails Model

::: tally.models.form.FormDetails
    options:
      show_source: false
      heading_level: 4
      members: []

### PaginatedForms Model

::: tally.models.form.PaginatedForms
    options:
      show_source: false
      heading_level: 4
      members: []

### Question Model

::: tally.models.form.Question
    options:
      show_source: false
      heading_level: 4
      members: []

### Submission Model

::: tally.models.form.Submission
    options:
      show_source: false
      heading_level: 4
      members: []

### SubmissionWithQuestions Model

::: tally.models.form.SubmissionWithQuestions
    options:
      show_source: false
      heading_level: 4
      members: []

### PaginatedSubmissions Model

::: tally.models.form.PaginatedSubmissions
    options:
      show_source: false
      heading_level: 4
      members: []

### FormStatus Enum

::: tally.models.form.FormStatus
    options:
      show_source: false
      heading_level: 4

**Values:**

- `PUBLISHED`: Form is live and accepting responses
- `DRAFT`: Form is in draft mode
- `CLOSED`: Form is closed and not accepting responses

### BlockType Enum

::: tally.models.form.BlockType
    options:
      show_source: false
      heading_level: 4

**Common Block Types:**

- `INPUT_TEXT`: Single-line text input
- `INPUT_EMAIL`: Email address input
- `INPUT_NUMBER`: Number input
- `INPUT_PHONE_NUMBER`: Phone number input
- `INPUT_LINK`: URL input
- `INPUT_DATE`: Date picker
- `TEXTAREA`: Multi-line text input
- `CHECKBOX`: Multiple choice (checkboxes)
- `DROPDOWN`: Dropdown select
- `LINEAR_SCALE`: Linear scale rating
- `FILE_UPLOAD`: File upload
- And 60+ more block types...

## Complete Example

```python
from tally import Tally, NotFoundError

client = Tally(api_key="tly_your_api_key_here")

# Create a complete form
form = client.forms.create(
    name="Product Feedback Survey",
    workspace_id="wksp_abc123",
    blocks=[
        {
            "type": "INPUT_TEXT",
            "payload": {
                "text": [{"type": "p", "children": [{"text": "What's your name?"}]}],
                "required": True
            }
        },
        {
            "type": "INPUT_EMAIL",
            "payload": {
                "text": [{"type": "p", "children": [{"text": "Email address"}]}],
                "required": True
            }
        },
        {
            "type": "LINEAR_SCALE",
            "payload": {
                "text": [{"type": "p", "children": [{"text": "Rate our product"}]}],
                "min": 1,
                "max": 10,
                "required": True
            }
        },
        {
            "type": "TEXTAREA",
            "payload": {
                "text": [{"type": "p", "children": [{"text": "Additional feedback"}]}],
                "required": False
            }
        }
    ],
    settings={
        "submitButtonText": "Send Feedback",
        "showProgressBar": True,
        "respondOnce": False
    }
)

print(f"Form created: {form.id}")
print(f"Edit URL: {form.edit_url}")

# List all questions
questions = client.forms.list_questions(form_id=form.id)
print(f"\nForm has {len(questions)} questions")

# Get submissions
submissions = client.forms.list_submissions(
    form_id=form.id,
    filter="completed"
)

print(f"\nTotal submissions: {submissions.filter_count.completed}")

# Process each submission
for sub in submissions.data:
    # Get full submission details
    try:
        full_sub = client.forms.get_submission(
            form_id=form.id,
            submission_id=sub.submission_id
        )
        
        print(f"\nSubmission: {full_sub.submission.submission_id}")
        for response in full_sub.submission.responses:
            print(f"  {response.key}: {response.value}")
    except NotFoundError:
        print(f"Submission {sub.submission_id} not found")
```

## Use Cases

### Export Form Submissions

```python
from tally import Tally
import json

client = Tally(api_key="tly_your_api_key_here")

# Export all submissions
submissions = client.forms.list_submissions(
    form_id="wXYz123",
    filter="completed",
    limit=100
)

# Convert to JSON
export_data = []
for sub in submissions.data:
    full_sub = client.forms.get_submission(
        form_id="wXYz123",
        submission_id=sub.submission_id
    )
    export_data.append({
        "id": full_sub.submission.submission_id,
        "created_at": full_sub.submission.created_at,
        "responses": {r.key: r.value for r in full_sub.submission.responses}
    })

with open("submissions.json", "w") as f:
    json.dump(export_data, f, indent=2)

print(f"Exported {len(export_data)} submissions")
```

### Clone a Form

```python
from tally import Tally

client = Tally(api_key="tly_your_api_key_here")

# Get original form
original = client.forms.get(form_id="wXYz123")

# Create a copy
copy = client.forms.create(
    name=f"{original.name} (Copy)",
    workspace_id="wksp_abc123",
    blocks=[block.to_dict() for block in original.blocks],
    settings=original.settings.to_dict() if original.settings else None
)

print(f"Form cloned: {copy.id}")
```

## Next Steps

- [Webhooks](webhooks.md) - Set up real-time notifications for form submissions
- [Workspaces](workspaces.md) - Organize forms into workspaces
- [Error Handling](../error-handling.md) - Handle form-related errors