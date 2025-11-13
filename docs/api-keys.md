# API Keys

To use the PyTally SDK, you need a Tally API key. This guide explains how to obtain and use your API key securely.

## Getting Your API Key

1. **Log in to Tally**: Go to [tally.so](https://tally.so) and sign in to your account
2. **Navigate to Settings**: Click on your profile and select **Settings**
3. **Access API Keys**: Go to the [API Keys](https://tally.so/settings/api-keys) section
4. **Create New Key**: Click **"Create API key"**
5. **Name Your Key**: Give your key a descriptive name (e.g., "Production App", "Development")
6. **Copy the Key**: Copy the generated API key immediately - you won't be able to see it again!

!!! warning "Keep Your API Key Secure"
Your API key provides access to your Tally account and data. Never commit it to version control or share it publicly.

## Using Your API Key

### Basic Usage

Pass your API key when initializing the client:

```python
from tally import Tally

client = Tally(api_key="tly_your_api_key_here")
```

### Environment Variables (Recommended)

Store your API key in environment variables for better security:

=== "Python"

    ```python
    import os
    from tally import Tally

    # Load API key from environment variable
    api_key = os.getenv("TALLY_API_KEY")
    client = Tally(api_key=api_key)
    ```

=== ".env File"

    Create a `.env` file in your project root:

    ```bash
    TALLY_API_KEY=tly_your_api_key_here
    ```

    Then load it using `python-dotenv`:

    ```python
    from dotenv import load_dotenv
    import os
    from tally import Tally

    load_dotenv()

    client = Tally(api_key=os.getenv("TALLY_API_KEY"))
    ```

=== "Shell"

    Set the environment variable in your shell:

    ```bash
    # Linux/macOS
    export TALLY_API_KEY=tly_your_api_key_here

    # Windows (Command Prompt)
    set TALLY_API_KEY=tly_your_api_key_here

    # Windows (PowerShell)
    $env:TALLY_API_KEY="tly_your_api_key_here"
    ```

## Troubleshooting

### Invalid API Key Error

If you receive an [`UnauthorizedError`](error-handling.md#unauthorizederror-401):

```python
tally.exceptions.UnauthorizedError: Invalid API key
```

**Solutions:**

1. Verify the API key is correct (copy-paste from Tally dashboard)
2. Check that you haven't accidentally included spaces or newlines
3. Ensure the environment variable is properly loaded
4. Verify the key hasn't been revoked in the Tally dashboard

### Environment Variable Not Loading

```python
# Debug environment variables
import os
print(f"TALLY_API_KEY exists: {bool(os.getenv('TALLY_API_KEY'))}")
print(f"TALLY_API_KEY value: {os.getenv('TALLY_API_KEY', 'NOT SET')}")
```

## API Key Format

Tally API keys follow this format:

```
tly_<random_string>
```

Example: `tly_abc123def456ghi789`

## Next Steps

- 📖 [API Reference](api-reference/users.md) - Explore available endpoints
- ⚠️ [Error Handling](error-handling.md) - Handle authentication errors
- 🏠 [Home](index.md) - Return to documentation home

## Additional Resources

- [Official Tally API Documentation](https://developers.tally.so/api-reference/introduction)
- [Tally API Keys Dashboard](https://tally.so/settings/api-keys)
