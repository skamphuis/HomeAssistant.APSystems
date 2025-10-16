# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-10-16

### Added
- Initial release of APSystems OpenAPI integration
- Config flow for easy UI-based setup
- Support for four sensor types:
  - Current Power (W)
  - Today Energy (kWh)
  - Lifetime Energy (kWh)
  - Max Power (W)
- API client with authentication and error handling
- Automatic data updates every 5 minutes
- HACS compatibility
- Device registry integration
- Multi-language support (English)
- Comprehensive documentation:
  - Installation guide
  - Usage examples
  - API reference
  - Contributing guidelines

### Features
- Async/await implementation for optimal performance
- Proper error handling for API and network issues
- Integration with Home Assistant Energy Dashboard
- Device class and state class support for sensors
- Unique device identification per system

### Documentation
- README with quick start guide
- INSTALLATION.md with detailed setup instructions
- EXAMPLES.md with dashboard and automation examples
- API.md with technical API documentation
- CONTRIBUTING.md with contribution guidelines

[1.0.0]: https://github.com/skamphuis/HomeAssistant.APSystems/releases/tag/v1.0.0
