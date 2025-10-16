# APSystems OpenAPI Integration for Home Assistant

A custom integration for Home Assistant to monitor APSystems solar inverters using the APSystems OpenAPI.

## Features

- Monitor real-time power generation
- Track daily and lifetime energy production
- Easy configuration through Home Assistant UI
- Automatic updates every 5 minutes
- Support for multiple sensor types:
  - Current Power (W)
  - Today Energy (kWh)
  - Lifetime Energy (kWh)
  - Max Power (W)

## Installation

### HACS (Recommended)

1. Add this repository to HACS as a custom repository
2. Search for "APSystems OpenAPI" in HACS
3. Click "Install"
4. Restart Home Assistant

### Manual Installation

1. Copy the `custom_components/apsystems_openapi` directory to your Home Assistant `custom_components` directory
2. Restart Home Assistant

## Configuration

1. Go to **Configuration** → **Integrations**
2. Click the **+ Add Integration** button
3. Search for "APSystems OpenAPI"
4. Enter your credentials:
   - **App ID**: Your APSystems OpenAPI App ID
   - **App Secret**: Your APSystems OpenAPI App Secret
   - **System ID**: Your APSystems system ID

### Getting API Credentials

To use this integration, you need to obtain API credentials from APSystems:

1. Contact APSystems support or visit their developer portal
2. Request OpenAPI access credentials
3. You will receive an App ID and App Secret
4. Find your System ID in the APSystems EMA portal

For more information, refer to the [APSystems OpenAPI documentation](https://file.apsystemsema.com:8083/apsystems/resource/openapi/Apsystems_OpenAPI_User_Manual_End_User_EN.pdf).

## Sensors

The integration creates the following sensors:

| Sensor | Description | Unit |
|--------|-------------|------|
| Current Power | Real-time power generation | W |
| Today Energy | Energy generated today | kWh |
| Lifetime Energy | Total energy generated | kWh |
| Max Power | Maximum power capacity | W |

## Support

For issues, feature requests, or contributions, please visit the [GitHub repository](https://github.com/skamphuis/HomeAssistant.APSystems).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.