"""
Example usage of SetBit Python SDK
"""
from setbit import SetBit, SetBitError, SetBitAuthError

# Initialize the client
try:
    client = SetBit(
        api_key="pk_your_api_key_here",  # Replace with your actual API key
        tags={"env": "development", "app": "example"}
    )
    print("✅ SetBit client initialized successfully")
    print(f"   Loaded {len(client._flags_cache)} flags\n")
except SetBitAuthError:
    print("❌ Invalid API key!")
    exit(1)
except SetBitError as e:
    print(f"❌ Failed to initialize SetBit: {e}")
    exit(1)


# Example 1: Boolean Flag
print("=" * 50)
print("Example 1: Boolean Flag")
print("=" * 50)

flag_name = "example-boolean-flag"
is_enabled = client.enabled(flag_name)
print(f"Flag '{flag_name}' is {'enabled ✅' if is_enabled else 'disabled ❌'}")

if is_enabled:
    print("  → Showing new feature!")
else:
    print("  → Showing old feature")
print()


# Example 2: A/B Test Experiment
print("=" * 50)
print("Example 2: A/B Test Experiment")
print("=" * 50)

experiment_name = "pricing-experiment"
variant = client.variant(experiment_name)
print(f"User assigned to variant: '{variant}'")

if variant == "variant_a":
    price = 99
    print(f"  → Showing price: ${price} (Variant A)")
elif variant == "variant_b":
    price = 149
    print(f"  → Showing price: ${price} (Variant B)")
else:
    price = 129
    print(f"  → Showing price: ${price} (Control)")
print()


# Example 3: Conversion Tracking
print("=" * 50)
print("Example 3: Conversion Tracking")
print("=" * 50)

print("Tracking conversion event...")
client.track(
    "example_conversion",
    flag_name=experiment_name,
    metadata={
        "variant": variant,
        "price": price,
        "user_type": "demo"
    }
)
print("✅ Conversion tracked successfully")
print()


# Example 4: Using Default Values
print("=" * 50)
print("Example 4: Using Default Values")
print("=" * 50)

# Flag that doesn't exist
result = client.enabled("nonexistent-flag", default=True)
print(f"Nonexistent flag with default=True: {result}")

result = client.enabled("nonexistent-flag", default=False)
print(f"Nonexistent flag with default=False: {result}")

variant = client.variant("nonexistent-experiment", default="custom-default")
print(f"Nonexistent experiment with custom default: {variant}")
print()


# Example 5: Manual Refresh
print("=" * 50)
print("Example 5: Manual Refresh")
print("=" * 50)

print("Refreshing flags from API...")
try:
    client.refresh()
    print(f"✅ Refreshed {len(client._flags_cache)} flags")
except SetBitError as e:
    print(f"❌ Failed to refresh: {e}")
print()


print("=" * 50)
print("Examples completed!")
print("=" * 50)
