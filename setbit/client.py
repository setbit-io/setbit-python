"""
SetBit Python SDK - Main Client
"""
import logging
from typing import Dict, Any, Optional
import requests

from .exceptions import SetBitError, SetBitAuthError, SetBitAPIError


logger = logging.getLogger(__name__)


class SetBit:
    """
    SetBit feature flag client.

    Example:
        >>> client = SetBit(api_key="pk_abc123", tags={"env": "production"})
        >>> if client.enabled("new-feature", user_id="user_123"):
        >>>     show_new_feature()
    """

    def __init__(
        self,
        api_key: str,
        tags: Optional[Dict[str, str]] = None,
        base_url: str = "https://flags.setbit.io"
    ):
        """
        Initialize SetBit client.

        Args:
            api_key: SetBit API key (required)
            tags: Dictionary of tags for targeting (env, app, team, region, etc.)
            base_url: API endpoint base URL

        Raises:
            SetBitError: If API key is missing
        """
        if not api_key:
            raise SetBitError("API key is required")

        self.api_key = api_key
        self.tags = tags or {}
        self.base_url = base_url.rstrip('/')

    def enabled(self, flag_name: str, user_id: str, default: bool = False) -> bool:
        """
        Check if a flag is enabled.

        Args:
            flag_name: Name of the flag to check
            user_id: User identifier (required for analytics and billing)
            default: Default value if flag not found or API fails

        Returns:
            True if flag is enabled, False otherwise
        """
        try:
            url = f"{self.base_url}/v1/evaluate"

            payload = {
                "apiKey": self.api_key,
                "userId": user_id,
                "tags": self.tags,
                "flagName": flag_name
            }

            response = requests.post(url, json=payload, timeout=5)

            # Handle authentication errors
            if response.status_code == 401:
                logger.error(f"Invalid API key")
                return default

            # Handle other errors - fail open
            if not response.ok:
                logger.error(f"API error {response.status_code}, returning default: {default}")
                return default

            result = response.json()
            return result.get('enabled', default)

        except requests.RequestException as e:
            logger.error(f"Failed to evaluate flag '{flag_name}': {e}, returning default: {default}")
            return default
        except Exception as e:
            logger.error(f"Unexpected error evaluating flag '{flag_name}': {e}, returning default: {default}")
            return default

    def variant(self, flag_name: str, user_id: str, default: str = "control") -> str:
        """
        Get the variant for an A/B test experiment.

        Args:
            flag_name: Name of the experiment flag
            user_id: User identifier (required)
            default: Default variant if flag not found or API fails

        Returns:
            Variant name (e.g., "control", "variant_a", "variant_b")
        """
        try:
            url = f"{self.base_url}/v1/evaluate"

            payload = {
                "apiKey": self.api_key,
                "userId": user_id,
                "tags": self.tags,
                "flagName": flag_name
            }

            response = requests.post(url, json=payload, timeout=5)

            # Handle authentication errors
            if response.status_code == 401:
                logger.error(f"Invalid API key")
                return default

            # Handle other errors - fail open
            if not response.ok:
                logger.error(f"API error {response.status_code}, returning default: {default}")
                return default

            result = response.json()

            # If flag is disabled, return default
            if not result.get('enabled', False):
                return default

            return result.get('variant', default)

        except requests.RequestException as e:
            logger.error(f"Failed to get variant for '{flag_name}': {e}, returning default: {default}")
            return default
        except Exception as e:
            logger.error(f"Unexpected error getting variant for '{flag_name}': {e}, returning default: {default}")
            return default

    def track(
        self,
        event_name: str,
        user_id: str,
        flag_name: Optional[str] = None,
        variant: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Track a conversion event.

        Args:
            event_name: Name of the event (e.g., "purchase", "signup")
            user_id: User identifier (required)
            flag_name: Optional flag name to associate with event
            variant: Optional variant the user was assigned to (for A/B test attribution)
            metadata: Optional metadata dictionary

        Note:
            Fails silently if tracking request fails (logs error but doesn't raise)

        Example:
            >>> variant = client.variant("pricing-test", user_id)
            >>> # ... later when user converts ...
            >>> client.track("purchase", user_id, flag_name="pricing-test", variant=variant)
        """
        try:
            url = f"{self.base_url}/v1/track"

            payload = {
                "apiKey": self.api_key,
                "userId": user_id,
                "eventName": event_name
            }

            if flag_name:
                payload["flagName"] = flag_name

            if variant:
                payload["variant"] = variant

            if metadata:
                payload["metadata"] = metadata

            response = requests.post(url, json=payload, timeout=5)
            response.raise_for_status()

            logger.debug(f"Tracked event '{event_name}' for user '{user_id}'")

        except requests.RequestException as e:
            logger.error(f"Failed to track event '{event_name}': {e}")
        except Exception as e:
            logger.error(f"Unexpected error tracking event '{event_name}': {e}")
