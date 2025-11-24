"""
Tests for conversion tracking
"""
import pytest
from unittest.mock import Mock, patch
from setbit import SetBit


@pytest.fixture
def client():
    """Create a SetBit client with mocked API"""
    mock_response = {
        "test-flag": {
            "enabled": True,
            "type": "boolean",
            "tags": {"env": "production"}
        }
    }

    with patch('requests.get') as mock_get:
        mock_get.return_value = Mock(
            status_code=200,
            json=lambda: mock_response
        )
        return SetBit(api_key="test_key", tags={"env": "production", "app": "web"})


def test_track_basic_event(client):
    """Test tracking a basic event without flag"""
    with patch('requests.post') as mock_post:
        mock_post.return_value = Mock(status_code=200)

        client.track("purchase")

        mock_post.assert_called_once()
        payload = mock_post.call_args[1]["json"]

        assert payload["event"] == "conversion"
        assert payload["event_name"] == "purchase"
        assert "flag_name" not in payload or payload["flag_name"] is None
        assert payload["tags"] == {"env": "production", "app": "web"}


def test_track_with_flag_name(client):
    """Test tracking event with associated flag"""
    with patch('requests.post') as mock_post:
        mock_post.return_value = Mock(status_code=200)

        client.track("signup", flag_name="onboarding-experiment")

        payload = mock_post.call_args[1]["json"]
        assert payload["flag_name"] == "onboarding-experiment"


def test_track_with_metadata(client):
    """Test tracking event with metadata"""
    with patch('requests.post') as mock_post:
        mock_post.return_value = Mock(status_code=200)

        client.track(
            "purchase",
            flag_name="pricing-experiment",
            metadata={"amount": 99.99, "currency": "USD", "product_id": 123}
        )

        payload = mock_post.call_args[1]["json"]
        assert payload["metadata"]["amount"] == 99.99
        assert payload["metadata"]["currency"] == "USD"
        assert payload["metadata"]["product_id"] == 123


def test_track_includes_timestamp(client):
    """Test that tracking includes timestamp"""
    with patch('requests.post') as mock_post:
        mock_post.return_value = Mock(status_code=200)

        client.track("purchase")

        payload = mock_post.call_args[1]["json"]
        assert "timestamp" in payload
        assert payload["timestamp"].endswith("Z") or "+" in payload["timestamp"]


def test_track_includes_auth_header(client):
    """Test that tracking includes authorization header"""
    with patch('requests.post') as mock_post:
        mock_post.return_value = Mock(status_code=200)

        client.track("purchase")

        headers = mock_post.call_args[1]["headers"]
        assert "Authorization" in headers
        assert headers["Authorization"] == "Bearer test_key"


def test_track_handles_network_error(client):
    """Test that tracking handles network errors gracefully"""
    with patch('requests.post') as mock_post:
        mock_post.side_effect = Exception("Network error")

        # Should not raise exception
        try:
            client.track("purchase")
        except Exception:
            pytest.fail("track() should not raise exception on network error")


def test_track_handles_timeout(client):
    """Test that tracking handles timeouts gracefully"""
    with patch('requests.post') as mock_post:
        from requests.exceptions import Timeout
        mock_post.side_effect = Timeout("Request timed out")

        # Should not raise exception
        try:
            client.track("purchase")
        except Exception:
            pytest.fail("track() should not raise exception on timeout")


def test_track_handles_api_error(client):
    """Test that tracking handles API errors gracefully"""
    with patch('requests.post') as mock_post:
        mock_post.return_value = Mock(status_code=500)
        mock_post.return_value.raise_for_status.side_effect = Exception("Server error")

        # Should not raise exception
        try:
            client.track("purchase")
        except Exception:
            pytest.fail("track() should not raise exception on API error")
