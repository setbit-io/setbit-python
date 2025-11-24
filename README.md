# SetBit Python SDK

Official Python SDK for [SetBit](https://setbit.io) - Simple feature flags and A/B testing.

## Features

- ✅ **Boolean Flags** - Simple on/off feature toggles
- 🧪 **A/B Testing** - Weighted variant distribution for experiments
- 📊 **Conversion Tracking** - Track events and conversions
- 🏷️ **Tag-Based Targeting** - Target by environment, app, team, region, etc.
- 🚀 **Fail-Open Design** - Returns defaults if API is unreachable
- 🪶 **Lightweight** - Minimal dependencies

## Installation

```bash
pip install setbit
```

## Quick Start

```python
from setbit import SetBit

# Initialize the client
client = SetBit(
    api_key="pk_your_api_key_here",
    tags={"env": "production", "app": "web"}
)

# Check a boolean flag (user_id required for analytics)
user_id = get_current_user_id()
if client.enabled("new-checkout", user_id=user_id):
    show_new_checkout()
else:
    show_old_checkout()

# Rollout flag (gradual percentage-based rollout)
variant = client.variant("new-api", user_id=current_user.id)
if variant == "enabled":
    use_new_api()
else:
    use_old_api()

# Get A/B test variant
variant = client.variant("pricing-experiment", user_id=current_user.id)
if variant == "variant_a":
    show_price_99()
elif variant == "variant_b":
    show_price_149()
else:  # control
    show_price_129()

# Track conversions
client.track("purchase", user_id=current_user.id, metadata={"amount": 99.99})
```

## API Reference

### Initialization

```python
SetBit(api_key: str, tags: dict = None, base_url: str = "https://flags.setbit.io")
```

**Parameters:**
- `api_key` (str, required): Your SetBit API key
- `tags` (dict, optional): Tags for targeting flags (e.g., `{"env": "production", "app": "web"}`)
- `base_url` (str, optional): API endpoint URL (useful for self-hosted instances)

**Raises:**
- `SetBitAuthError`: If API key is invalid
- `SetBitAPIError`: If initial flag fetch fails

**Example:**
```python
client = SetBit(
    api_key="pk_abc123",
    tags={"env": "production", "app": "web", "region": "us-east"}
)
```

---

### `enabled(flag_name, user_id, default=False)`

Check if a flag is enabled. Returns `True` if the flag is globally enabled, `False` otherwise.

**Parameters:**
- `flag_name` (str): Name of the flag
- `user_id` (str, **required**): User identifier (required for analytics and billing)
- `default` (bool): Value to return if flag not found (default: `False`)

**Returns:** `bool` - `True` if enabled, `False` otherwise

**Note:** This method returns whether the flag is globally enabled. For rollout flags, use `variant()` to check which rollout group the user is in.

**Example:**
```python
# Check if flag is enabled (user_id required)
user_id = get_current_user_id()
if client.enabled("new-dashboard", user_id=user_id):
    render_new_dashboard()
else:
    render_old_dashboard()

# With custom default
if client.enabled("beta-feature", user_id=user_id, default=True):
    show_beta_feature()
```

---

### `variant(flag_name, user_id, default="control")`

Get the variant for an A/B test experiment or rollout flag.

**Parameters:**
- `flag_name` (str): Name of the experiment or rollout flag
- `user_id` (str): User identifier (required)
- `default` (str): Variant to return if flag not found (default: `"control"`)

**Returns:** `str` - Variant name

For experiments: `"control"`, `"variant_a"`, `"variant_b"`, etc.
For rollout flags: `"enabled"` (user in rollout) or `"disabled"` (user not in rollout)

**Example:**
```python
# A/B test experiment
variant = client.variant("button-color-test", user_id=current_user.id)

if variant == "variant_a":
    button_color = "blue"
elif variant == "variant_b":
    button_color = "green"
else:  # control
    button_color = "red"

# Rollout flag (gradual percentage-based rollout)
variant = client.variant("new-api", user_id=current_user.id)

if variant == "enabled":
    use_new_api()  # User is in the rollout group
else:
    use_old_api()  # User is not in the rollout group
```

---

### `track(event_name, user_id, flag_name=None, metadata=None)`

Track a conversion event.

**Parameters:**
- `event_name` (str): Name of the event (e.g., `"purchase"`, `"signup"`)
- `user_id` (str, **required**): User identifier (required for analytics and billing)
- `flag_name` (str, optional): Flag to associate with this conversion
- `metadata` (dict, optional): Additional event data

**Returns:** `None`

**Note:** This method fails silently - errors are logged but not raised.

**Example:**
```python
user_id = get_current_user_id()

# Track basic conversion
client.track("signup", user_id=user_id)

# Track with flag association
client.track("purchase", user_id=user_id, flag_name="checkout-experiment")

# Track with metadata
client.track(
    "purchase",
    user_id=user_id,
    flag_name="pricing-test",
    metadata={
        "amount": 99.99,
        "currency": "USD",
        "product_id": "prod_123"
    }
)
```

---

### `refresh()`

Manually refresh flags from the API.

**Returns:** `None`

**Raises:**
- `SetBitAuthError`: If API key is invalid
- `SetBitAPIError`: If API request fails

**Example:**
```python
# Refresh flags if you know they've changed
client.refresh()
```

---

## Usage Examples

### Boolean Flags

```python
from setbit import SetBit

client = SetBit(
    api_key="pk_abc123",
    tags={"env": "production", "app": "web"}
)

# Simple feature toggle (boolean flag) - user_id required
user_id = get_current_user_id()
if client.enabled("dark-mode", user_id=user_id):
    enable_dark_mode()

# With default value
debug_mode = client.enabled("debug-logging", user_id=user_id, default=False)
```

### Rollout Flags

```python
# Gradual percentage-based rollout
# Use variant() to check which rollout group the user is in
variant = client.variant("new-api-v2", user_id=current_user.id)

if variant == "enabled":
    use_api_v2()  # User is in the rollout group
else:
    use_api_v1()  # User is not in the rollout group

# Example: Rollout new checkout flow
checkout_variant = client.variant("new-checkout", user_id=current_user.id)

if checkout_variant == "enabled":
    render_new_checkout()
    client.track("checkout_started", user_id=current_user.id, flag_name="new-checkout")
else:
    render_old_checkout()
```

### A/B Testing

```python
# Get variant for experiment
variant = client.variant("homepage-hero", user_id=current_user.id)

if variant == "variant_a":
    # Version A: Large hero image
    render_hero(size="large", style="image")
elif variant == "variant_b":
    # Version B: Video hero
    render_hero(size="large", style="video")
elif variant == "variant_c":
    # Version C: Minimal hero
    render_hero(size="small", style="minimal")
else:
    # Control: Original hero
    render_hero(size="medium", style="image")

# Track conversion for this experiment
client.track("signup", user_id=current_user.id, flag_name="homepage-hero")
```

### Conversion Tracking

```python
user_id = get_current_user_id()

# Track page view
client.track("page_view", user_id=user_id, metadata={"page": "/pricing"})

# Track user signup
client.track("signup", user_id=user_id, metadata={
    "plan": "pro",
    "source": "landing_page"
})

# Track purchase with detailed metadata
client.track(
    "purchase",
    user_id=user_id,
    flag_name="checkout-experiment",
    metadata={
        "amount": 149.99,
        "currency": "USD",
        "items": 3,
        "payment_method": "credit_card"
    }
)
```

### Error Handling

```python
from setbit import SetBit, SetBitAuthError, SetBitAPIError

try:
    client = SetBit(api_key="invalid_key")
except SetBitAuthError:
    print("Invalid API key!")
    # Fall back to default behavior
    client = None

# Client returns safe defaults if initialization failed
user_id = get_current_user_id()
if client and client.enabled("new-feature", user_id=user_id):
    show_new_feature()
else:
    show_old_feature()
```

### Multi-Environment Setup

```python
import os
from setbit import SetBit

# Use environment variables for configuration
client = SetBit(
    api_key=os.getenv("SETBIT_API_KEY"),
    tags={
        "env": os.getenv("ENVIRONMENT", "development"),
        "app": "backend",
        "region": os.getenv("AWS_REGION", "us-east-1")
    }
)

# Same flag, different behavior per environment
# In dev: 100% rollout
# In prod: 10% gradual rollout
user_id = get_current_user_id()
if client.enabled("new-caching-layer", user_id=user_id):
    use_redis_cache()
```

### Django Integration

```python
# settings.py
from setbit import SetBit

SETBIT_CLIENT = SetBit(
    api_key=config("SETBIT_API_KEY"),
    tags={
        "env": config("ENVIRONMENT"),
        "app": "django-app"
    }
)

# views.py
from django.conf import settings

def checkout_view(request):
    user_id = str(request.user.id)
    variant = settings.SETBIT_CLIENT.variant("checkout-flow", user_id=user_id)

    if variant == "one_page":
        return render(request, "checkout_one_page.html")
    else:
        return render(request, "checkout_multi_step.html")

def purchase_complete(request):
    user_id = str(request.user.id)
    settings.SETBIT_CLIENT.track(
        "purchase",
        user_id=user_id,
        flag_name="checkout-flow",
        metadata={"amount": request.POST["amount"]}
    )
    return redirect("thank_you")
```

### Flask Integration

```python
from flask import Flask, g
from setbit import SetBit

app = Flask(__name__)

@app.before_request
def setup_setbit():
    g.setbit = SetBit(
        api_key=app.config["SETBIT_API_KEY"],
        tags={"env": app.config["ENV"], "app": "flask-app"}
    )

@app.route("/")
def index():
    user_id = get_current_user_id()  # Your method to get user ID
    if g.setbit.enabled("new-homepage", user_id=user_id):
        return render_template("homepage_v2.html")
    return render_template("homepage.html")
```

## Development

### Running Tests

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run with coverage
pytest --cov=setbit --cov-report=html
```

### Type Checking

```bash
mypy setbit
```

### Code Formatting

```bash
black setbit tests
flake8 setbit tests
```

## Error Handling

The SDK uses a **fail-open** philosophy - if something goes wrong, it returns safe default values rather than crashing your application.

### Exception Types

- `SetBitError`: Base exception for all SDK errors
- `SetBitAuthError`: Invalid API key (raised during initialization/refresh)
- `SetBitAPIError`: API request failed (raised during initialization/refresh)

### Behavior

| Method | Error Behavior |
|--------|----------------|
| `__init__()` | Raises exception if API key invalid or flags can't be fetched |
| `enabled()` | Returns `default` value if flag not found |
| `variant()` | Returns `default` variant if flag not found |
| `track()` | Logs error but does not raise exception |
| `refresh()` | Raises exception if refresh fails |

## API Endpoints

The SDK communicates with these SetBit API endpoints:

- **GET** `/api/sdk/flags` - Fetch flags for given tags
- **POST** `/api/events` - Send conversion events

## Requirements

- Python >= 3.7
- requests >= 2.25.0

## Support

- 📚 [Documentation](https://docs.setbit.io)
- 💬 [Discord Community](https://discord.gg/setbit)
- 📧 Email: support@setbit.io
- 🐛 [Report Issues](https://github.com/setbit/setbit-python/issues)

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

Made with ❤️ by the SetBit team
