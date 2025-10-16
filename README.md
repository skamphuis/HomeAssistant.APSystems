# APSystems OpenAPI Integration for Home Assistant

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)
[![hacs][hacsbadge]][hacs]

A custom integration for Home Assistant to monitor APSystems solar inverters using the APSystems OpenAPI.

**Monitor your solar production in real-time with Home Assistant!** ☀️

[releases-shield]: https://img.shields.io/github/release/skamphuis/HomeAssistant.APSystems.svg?style=for-the-badge
[releases]: https://github.com/skamphuis/HomeAssistant.APSystems/releases
[commits-shield]: https://img.shields.io/github/commit-activity/y/skamphuis/HomeAssistant.APSystems.svg?style=for-the-badge
[commits]: https://github.com/skamphuis/HomeAssistant.APSystems/commits/main
[license-shield]: https://img.shields.io/github/license/skamphuis/HomeAssistant.APSystems.svg?style=for-the-badge
[hacs]: https://github.com/hacs/integration
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge

## ⚡ Features

- 📊 **Real-time monitoring** - Live power generation data
- 📈 **Energy tracking** - Daily and lifetime energy production
- ⚙️ **Easy setup** - UI-based configuration flow
- 🔄 **Automatic updates** - Data refreshes every 5 minutes
- 📱 **Energy Dashboard** - Native integration with Home Assistant Energy
- 🎨 **Beautiful sensors** - Four sensor types with proper device classes

### Available Sensors

| Sensor | Description | Unit | Device Class |
|--------|-------------|------|--------------|
| **Current Power** | Real-time power generation | W | power |
| **Today Energy** | Energy generated today | kWh | energy |
| **Lifetime Energy** | Total energy generated | kWh | energy |
| **Max Power** | System maximum capacity | W | power |

## 🚀 Quick Start

Want to get started right away? Check out the [**Quick Start Guide**](QUICKSTART.md)!

### Prerequisites

- Home Assistant 2023.1.0 or newer
- APSystems solar inverter with EMA monitoring
- APSystems OpenAPI credentials (App ID, App Secret, System ID)

> **Need API credentials?** See the [Quick Start Guide](QUICKSTART.md#getting-api-credentials) for instructions on obtaining them.

## 📦 Installation

### HACS (Recommended)

1. Open HACS in Home Assistant
2. Go to "Integrations" 
3. Click "⋮" → "Custom repositories"
4. Add repository: `https://github.com/skamphuis/HomeAssistant.APSystems`
5. Category: "Integration"
6. Search for "APSystems OpenAPI" and install
7. Restart Home Assistant

### Manual Installation

1. Download the [latest release](https://github.com/skamphuis/HomeAssistant.APSystems/releases)
2. Copy `custom_components/apsystems_openapi` to your `custom_components` directory
3. Restart Home Assistant

For detailed instructions, see [INSTALLATION.md](INSTALLATION.md).

## ⚙️ Configuration

1. Go to **Settings** → **Devices & Services**
2. Click **+ Add Integration**
3. Search for **APSystems OpenAPI**
4. Enter your credentials:
   - **App ID**: Your APSystems OpenAPI App ID
   - **App Secret**: Your APSystems OpenAPI App Secret
   - **System ID**: Your system ID from EMA portal

That's it! Your sensors will be created automatically. ✨

## 📚 Documentation

- 📖 **[Quick Start Guide](QUICKSTART.md)** - Get up and running in minutes
- 🔧 **[Installation Guide](INSTALLATION.md)** - Detailed installation instructions
- 💡 **[Examples & Usage](EXAMPLES.md)** - Dashboard cards, automations, and more
- 🏗️ **[Architecture](ARCHITECTURE.md)** - Technical architecture overview
- 📡 **[API Reference](API.md)** - API documentation for developers
- 🤝 **[Contributing](CONTRIBUTING.md)** - Help improve the integration

## 🎨 Dashboard Examples

### Simple Entities Card
```yaml
type: entities
title: Solar Power
entities:
  - sensor.apsystems_current_power
  - sensor.apsystems_today_energy
  - sensor.apsystems_lifetime_energy
```

### Power Gauge
```yaml
type: gauge
entity: sensor.apsystems_current_power
name: Solar Power
min: 0
max: 5000
needle: true
```

See [EXAMPLES.md](EXAMPLES.md) for more dashboard and automation examples!

## 🤝 Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Ways to Contribute

- 🐛 Report bugs
- 💡 Suggest new features
- 📝 Improve documentation
- 🔧 Submit pull requests
- ⭐ Star the repository

## 🔗 Related Links

- [APSystems OpenAPI Documentation](https://file.apsystemsema.com:8083/apsystems/resource/openapi/Apsystems_OpenAPI_User_Manual_End_User_EN.pdf)
- [APSystems EMA Portal](https://ema.apsystemsema.com)
- [Home Assistant](https://www.home-assistant.io)
- [HACS](https://hacs.xyz)

## ⚠️ Disclaimer

This is an unofficial integration and is not affiliated with or endorsed by APSystems. Use at your own risk.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built for the Home Assistant community
- Based on APSystems OpenAPI documentation
- Thanks to all contributors!

---

**Found this useful?** ⭐ Star this repo and share it with others!

**Having issues?** 🐛 [Open an issue](https://github.com/skamphuis/HomeAssistant.APSystems/issues) on GitHub.