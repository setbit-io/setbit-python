"""
Custom exceptions for SetBit SDK
"""


class SetBitError(Exception):
    """Base exception for SetBit SDK"""
    pass


class SetBitAuthError(SetBitError):
    """Raised when API key is invalid"""
    pass


class SetBitAPIError(SetBitError):
    """Raised when API request fails"""
    pass
