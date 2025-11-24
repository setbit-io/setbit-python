"""
SetBit Python SDK

Simple feature flag and A/B testing client for SetBit.
"""

from .client import SetBit
from .exceptions import SetBitError, SetBitAuthError, SetBitAPIError

__version__ = "0.1.0"
__all__ = ["SetBit", "SetBitError", "SetBitAuthError", "SetBitAPIError"]
