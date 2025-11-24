"""
Tests for SetBit client
"""
import pytest
from unittest.mock import Mock, patch
from setbit import SetBit, SetBitError, SetBitAuthError, SetBitAPIError


@pytest.fixture
def mock_response():
    """Mock successful API response"""
    return {
        "simple-flag": {
            "enabled": True,
            "type": "boolean",
            "tags": {"env": "production"}
        },
        "disabled-flag": {
            "enabled": False,
            "type": "boolean",
            "tags": {"env": "production"}
        },
        "experiment-flag": {
            "enabled": True,
            "type": "experiment",
            "variants": {
                "control": {"weight": 50},
                "variant_a": {"weight": 50}
            },
            "tags": {"env": "production"}
        }
    }


@pytest.fixture
def client(mock_response):
    """Create a SetBit client with mocked API"""
    with patch('requests.get') as mock_get:
        mock_get.return_value = Mock(
            status_code=200,
            json=lambda: mock_response
        )
        return SetBit(api_key="test_key", tags={"env": "production"})


def test_init_requires_api_key():
    """Test that initialization requires an API key"""
    with pytest.raises(SetBitError):
        SetBit(api_key="")


def test_init_fetches_flags(mock_response):
    """Test that initialization fetches flags from API"""
    with patch('requests.get') as mock_get:
        mock_get.return_value = Mock(
            status_code=200,
            json=lambda: mock_response
        )

        client = SetBit(api_key="test_key")

        # Verify API was called
        mock_get.assert_called_once()
        assert "simple-flag" in client._flags_cache


def test_init_handles_auth_error():
    """Test that initialization raises SetBitAuthError on 401"""
    with patch('requests.get') as mock_get:
        mock_get.return_value = Mock(status_code=401)

        with pytest.raises(SetBitAuthError):
            SetBit(api_key="invalid_key")


def test_enabled_returns_true_for_enabled_flag(client):
    """Test enabled() returns True for enabled boolean flag"""
    assert client.enabled("simple-flag") is True


def test_enabled_returns_false_for_disabled_flag(client):
    """Test enabled() returns False for disabled flag"""
    assert client.enabled("disabled-flag") is False


def test_enabled_returns_default_for_missing_flag(client):
    """Test enabled() returns default value for missing flag"""
    assert client.enabled("nonexistent-flag", default=True) is True
    assert client.enabled("nonexistent-flag", default=False) is False
    assert client.enabled("nonexistent-flag") is False


def test_enabled_returns_false_for_experiment(client):
    """Test enabled() returns False for experiment flags"""
    assert client.enabled("experiment-flag") is False


def test_variant_returns_variant_for_experiment(client):
    """Test variant() returns a variant for experiment flag"""
    variant = client.variant("experiment-flag")
    assert variant in ["control", "variant_a"]


def test_variant_returns_default_for_missing_flag(client):
    """Test variant() returns default for missing flag"""
    assert client.variant("nonexistent-flag") == "control"
    assert client.variant("nonexistent-flag", default="custom") == "custom"


def test_variant_returns_default_for_disabled_flag(mock_response):
    """Test variant() returns default for disabled experiment"""
    mock_response["experiment-flag"]["enabled"] = False

    with patch('requests.get') as mock_get:
        mock_get.return_value = Mock(
            status_code=200,
            json=lambda: mock_response
        )
        client = SetBit(api_key="test_key")

        assert client.variant("experiment-flag") == "control"


def test_variant_returns_default_for_non_experiment(client):
    """Test variant() returns default for non-experiment flags"""
    assert client.variant("simple-flag") == "control"


def test_track_sends_event(client):
    """Test track() sends event to API"""
    with patch('requests.post') as mock_post:
        mock_post.return_value = Mock(status_code=200)

        client.track("purchase", flag_name="test-flag", metadata={"amount": 99.99})

        # Verify API was called
        mock_post.assert_called_once()
        call_args = mock_post.call_args

        # Check URL
        assert call_args[0][0].endswith("/api/events")

        # Check payload
        payload = call_args[1]["json"]
        assert payload["event"] == "conversion"
        assert payload["event_name"] == "purchase"
        assert payload["flag_name"] == "test-flag"
        assert payload["metadata"]["amount"] == 99.99


def test_track_fails_silently_on_error(client):
    """Test track() doesn't raise exception on API error"""
    with patch('requests.post') as mock_post:
        mock_post.side_effect = Exception("API Error")

        # Should not raise
        client.track("purchase")


def test_refresh_updates_cache(client, mock_response):
    """Test refresh() updates the flags cache"""
    # Modify response for second call
    new_response = {
        "new-flag": {
            "enabled": True,
            "type": "boolean",
            "tags": {"env": "production"}
        }
    }

    with patch('requests.get') as mock_get:
        mock_get.return_value = Mock(
            status_code=200,
            json=lambda: new_response
        )

        client.refresh()

        assert "new-flag" in client._flags_cache
        assert "simple-flag" not in client._flags_cache


def test_refresh_raises_on_auth_error(client):
    """Test refresh() raises SetBitAuthError on 401"""
    with patch('requests.get') as mock_get:
        mock_get.return_value = Mock(status_code=401)

        with pytest.raises(SetBitAuthError):
            client.refresh()


def test_custom_base_url(mock_response):
    """Test client can use custom base URL"""
    with patch('requests.get') as mock_get:
        mock_get.return_value = Mock(
            status_code=200,
            json=lambda: mock_response
        )

        client = SetBit(
            api_key="test_key",
            base_url="http://localhost:5000"
        )

        # Verify URL used in request
        call_args = mock_get.call_args
        assert call_args[0][0].startswith("http://localhost:5000")
