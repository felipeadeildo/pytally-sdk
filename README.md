# PyTally SDK

> Unofficial Python SDK for the [Tally.so](https://tally.so) API.

[![PyPI version](https://badge.fury.io/py/pytally-sdk.svg)](https://badge.fury.io/py/pytally-sdk)
[![Python Versions](https://img.shields.io/pypi/pyversions/pytally-sdk.svg)](https://pypi.org/project/pytally-sdk/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Docs](https://img.shields.io/badge/docs-online-brightgreen)](https://pytally-sdk.fa.dev.br)

---

## Overview

**PyTally SDK** is a lightweight, fully typed Python client for the [Tally.so API](https://tally.so).
It provides a clean, Pythonic interface for authenticating, querying, and managing Tally resources -- without worrying about HTTP requests or pagination.

### Implemented Resources

- [x] Users
- [x] Organizations
- [x] Forms
- [x] Workspaces
- [x] Webhooks
- [ ] MCP

---

## Installation

### pip

```bash
pip install pytally-sdk
```

### uv (recommended)

```bash
uv add pytally-sdk
```

**Requirements:**
Python ≥ 3.11
`httpx` (auto-installed)

---

## Quick Start

```python
from tally import Tally

client = Tally(api_key="tly_your_api_key_here")

user = client.users.me()
print(f"Hello, {user.full_name} ({user.email})")
```

### With Context Manager

```python
from tally import Tally

with Tally(api_key="tly_your_api_key_here") as client:
    for form in client.forms:
        print(f"{form.name} ({form.id})")
```

---

## Webhooks — Example Usage

### List Webhooks

```python
from tally import Tally

client = Tally(api_key="tly_your_api_key_here")

# Get all webhooks
for webhook in client.webhooks:
    print(f"{webhook.url} → enabled={webhook.is_enabled}")
```

### Create a Webhook

```python
from tally import Tally

client = Tally(api_key="tly_your_api_key_here")

webhook = client.webhooks.create(
    url="https://your-app.com/webhooks/tally",
    event_types=["FORM_RESPONSE"],
)

print(f"Webhook created: {webhook.id}")
```

For complete API usage, visit the [📘 Webhooks Reference](https://pytally-sdk.fa.dev.br/api-reference/webhooks/).

---

## Error Handling

```python
from tally import Tally, UnauthorizedError, NotFoundError

client = Tally(api_key="tly_invalid")

try:
    client.users.me()
except UnauthorizedError:
    print("Invalid API key.")
except NotFoundError:
    print("Resource not found.")
```

See [Error Handling → docs](https://pytally-sdk.fa.dev.br/error-handling/).

---

## Documentation

👉 Full documentation and API reference available at:
**[https://pytally-sdk.fa.dev.br](https://pytally-sdk.fa.dev.br)**

---

## Development

Wanna help improve the SDK?

```bash
git clone https://github.com/felipeadeildo/pytally.git
cd pytally
uv sync
uv run mkdocs serve  # preview docs locally
pre-commit install   # install pre-commit hooks
```

---

## 🔗 Links

* 📦 [PyPI Package](https://pypi.org/project/pytally-sdk/)
* 💻 [GitHub Repository](https://github.com/felipeadeildo/pytally)
* 🧾 [Tally API Reference](https://developers.tally.so/api-reference/introduction)
* 🪲 [Issue Tracker](https://github.com/felipeadeildo/pytally/issues)
* 📘 [Documentation](https://pytally-sdk.fa.dev.br)

---

## ⚖️ License

Licensed under the [Apache License 2.0](https://github.com/felipeadeildo/pytally/blob/main/LICENSE).

> **Disclaimer**
> This is an unofficial SDK and is not affiliated with or endorsed by Tally.
> “Tally” and the Tally logo are trademarks of Tally B.V.
