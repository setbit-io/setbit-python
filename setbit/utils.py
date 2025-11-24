"""
Helper utilities for SetBit SDK
"""
import random
import hashlib
from typing import Dict, Any, Optional


def compute_rollout_percentage(identifier: str) -> int:
    """
    Compute a consistent percentage (0-99) for a given identifier.
    Uses SHA-256 hash to ensure consistent assignment.

    Args:
        identifier: User ID or other unique identifier

    Returns:
        Integer between 0 and 99 (inclusive)
    """
    hash_bytes = hashlib.sha256(identifier.encode('utf-8')).digest()
    # Use first 4 bytes to get a number
    hash_int = int.from_bytes(hash_bytes[:4], byteorder='big')
    return hash_int % 100


def select_variant(variants: Dict[str, Any]) -> str:
    """
    Select a variant using weighted random distribution.

    Args:
        variants: Dictionary mapping variant names to config with 'weight' key
                 Example: {"control": {"weight": 34}, "variant_a": {"weight": 33}}

    Returns:
        Selected variant name
    """
    if not variants:
        return "control"

    total_weight = sum(v.get("weight", 0) for v in variants.values())

    if total_weight == 0:
        # If no weights, pick first variant or control
        return list(variants.keys())[0] if variants else "control"

    rand = random.randint(0, total_weight - 1)

    cumulative = 0
    for name, config in variants.items():
        cumulative += config.get("weight", 0)
        if rand < cumulative:
            return name

    # Fallback to control
    return "control"
