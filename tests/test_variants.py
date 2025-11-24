"""
Tests for variant selection logic
"""
import pytest
from collections import Counter
from setbit.utils import select_variant


def test_select_variant_basic():
    """Test basic variant selection"""
    variants = {
        "control": {"weight": 50},
        "variant_a": {"weight": 50}
    }

    # Run multiple times to ensure both variants can be selected
    results = [select_variant(variants) for _ in range(100)]

    # Both variants should appear
    assert "control" in results
    assert "variant_a" in results


def test_select_variant_weighted_distribution():
    """Test that variant selection follows weight distribution"""
    variants = {
        "control": {"weight": 90},
        "variant_a": {"weight": 10}
    }

    # Run many times to get statistical distribution
    results = [select_variant(variants) for _ in range(1000)]
    counts = Counter(results)

    # Control should appear roughly 9x more than variant_a
    # Using loose bounds to avoid flaky tests
    assert counts["control"] > counts["variant_a"]
    assert counts["control"] / len(results) > 0.7  # Should be ~0.9


def test_select_variant_three_way():
    """Test three-way split"""
    variants = {
        "control": {"weight": 34},
        "variant_a": {"weight": 33},
        "variant_b": {"weight": 33}
    }

    results = [select_variant(variants) for _ in range(1000)]
    counts = Counter(results)

    # All three variants should appear
    assert len(counts) == 3
    assert "control" in counts
    assert "variant_a" in counts
    assert "variant_b" in counts

    # Each should be roughly equal (allowing for randomness)
    for variant in counts.values():
        assert 200 < variant < 500


def test_select_variant_empty():
    """Test variant selection with empty variants"""
    assert select_variant({}) == "control"


def test_select_variant_zero_weights():
    """Test variant selection when all weights are zero"""
    variants = {
        "control": {"weight": 0},
        "variant_a": {"weight": 0}
    }

    # Should return first variant
    result = select_variant(variants)
    assert result in ["control", "variant_a"]


def test_select_variant_missing_weight():
    """Test variant selection with missing weight key"""
    variants = {
        "control": {},
        "variant_a": {"weight": 100}
    }

    # Should handle missing weight gracefully
    results = [select_variant(variants) for _ in range(100)]
    assert "variant_a" in results
