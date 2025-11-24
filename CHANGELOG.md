# Changelog

All notable changes to the SetBit Python SDK will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-11-23

### Added
- Initial release of SetBit Python SDK
- Boolean flag checking with `enabled()` method
- A/B test variant selection with `variant()` method
- Conversion tracking with `track()` method
- Tag-based targeting support
- Manual flag refresh with `refresh()` method
- Comprehensive error handling with custom exceptions
- Fail-open design - returns defaults on errors
- Full test coverage
- Type hints for all public methods
- Detailed README with examples

### Features
- Boolean flag checking with consistent behavior
- Rollout flags with percentage-based gradual rollout (requires user_id)
- Weighted random distribution for A/B tests
- In-memory flag caching
- Silent failure for tracking (logs errors but doesn't crash)
- Support for custom base URL (self-hosted instances)
- Consistent user assignment using SHA-256 hashing
- Django and Flask integration examples

[0.1.0]: https://github.com/setbit/setbit-python/releases/tag/v0.1.0
