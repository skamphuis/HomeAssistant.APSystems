# APSystems API

A Home Assistant integration for APSystems solar inverters using the APSystems OpenAPI. This integration is different from the existing APSystems integration as it uses the cloud API instead of direct inverter communication.

## Features

- **System-level sensors**: Total system power, daily energy, and lifetime energy
- **Inverter-level sensors**: Individual inverter power, daily energy, and lifetime energy  
- **Device tracking**: System and inverter devices for monitoring connectivity
- **Real-time data**: Automatic updates every 5 minutes (configurable)
- **Secure authentication**: Uses APSystems signature-based authentication

## Installation

1. Copy the `custom_components/apsystems` folder to your Home Assistant `custom_components` directory
2. Restart Home Assistant
3. Go to Settings > Devices & Services > Add Integration
4. Search for "APSystems API" and add it
5. Enter your API credentials:
   - **App ID**: Your APSystems API App ID
   - **App Secret**: Your APSystems API App Secret  
   - **System ID**: Your APSystems system ID

## Getting API Credentials

To get your API credentials:

1. Send an application email to APsystems' support email address with:
   - Who you are
   - Why you want to register an OpenAPI account
   - What you plan to do with the data

2. When approved, you'll receive an email with your App ID and App Secret

## Sensors Created

### System Sensors
- `sensor.apsystems_api_system_power` - Current system power in watts
- `sensor.apsystems_api_system_energy_today` - Today's energy production in kWh
- `sensor.apsystems_api_system_energy_total` - Lifetime energy production in kWh

### Inverter Sensors (per inverter)
- `sensor.apsystems_api_inverter_[ID]_power` - Current inverter power in watts
- `sensor.apsystems_api_inverter_[ID]_energy_today` - Today's energy production in kWh
- `sensor.apsystems_api_inverter_[ID]_energy_total` - Lifetime energy production in kWh

## Devices Created

- **System Device**: Represents your entire APSystems solar system
- **Inverter Devices**: Individual devices for each inverter in your system

## Configuration

The integration automatically discovers your inverters and creates appropriate sensors and devices. No additional configuration is required after the initial setup.

## Troubleshooting

If you encounter issues:

1. Check that your API credentials are correct
2. Verify your system ID is valid
3. Check the Home Assistant logs for any error messages
4. Ensure your APSystems system is online and reporting data

## API Documentation

This integration uses the APSystems OpenAPI. For more information, see the [APSystems OpenAPI User Manual](https://file.apsystemsema.com:8083/apsystems/resource/openapi/Apsystems_OpenAPI_User_Manual_End_User_EN.pdf).

## License

This project is licensed under the MIT License - see the LICENSE file for details.
