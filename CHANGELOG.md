# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2024-01-XX

### Added
- Initial release of APSystems API integration
- System-level sensors for power and energy monitoring
- Inverter-level sensors for individual inverter monitoring
- Device tracking for system and inverter connectivity
- Secure API authentication using APSystems signature method
- Comprehensive error handling to prevent Home Assistant crashes
- Config flow for easy setup
- Support for multiple inverters per system
- Real-time data updates every 5 minutes
- HACS integration support

### Features
- **System Sensors**: Total system power, daily energy, lifetime energy
- **Inverter Sensors**: Individual inverter power, daily energy, lifetime energy
- **Device Tracking**: System and inverter device entities
- **Error Handling**: Graceful handling of API failures and network issues
- **Authentication**: Secure signature-based API authentication
- **Auto-Discovery**: Automatic detection of inverters in your system

### Technical Details
- Uses APSystems OpenAPI v2
- HMAC-SHA256 signature authentication
- 30-second API request timeouts
- Comprehensive error logging
- Safe data parsing and type conversion
- Coordinator-based data management
