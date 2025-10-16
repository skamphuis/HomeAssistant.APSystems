# Installation Guide

## HACS Installation (Recommended)

1. Open HACS in Home Assistant
2. Go to "Integrations"
3. Click the 3 dots in the top right corner
4. Select "Custom repositories"
5. Add this repository URL: `https://github.com/skamphuis/HomeAssistant.APSystems`
6. Select category: "Integration"
7. Click "Add"
8. Search for "APSystems OpenAPI" in HACS
9. Click "Download"
10. Restart Home Assistant

## Manual Installation

1. Download the latest release from GitHub
2. Extract the archive
3. Copy the `custom_components/apsystems_openapi` folder to your Home Assistant's `custom_components` directory
   - The path should be: `<config>/custom_components/apsystems_openapi/`
4. Restart Home Assistant

## Configuration

### Step 1: Obtain API Credentials

Before configuring the integration, you need to obtain API credentials from APSystems:

1. Contact APSystems customer support
2. Request OpenAPI access for end users
3. You will receive:
   - **App ID** (username)
   - **App Secret** (password)
4. Also locate your **System ID** from the APSystems EMA portal

### Step 2: Configure Integration in Home Assistant

1. Go to **Settings** → **Devices & Services**
2. Click **+ Add Integration**
3. Search for **APSystems OpenAPI**
4. Enter your credentials:
   - **App ID**: Your APSystems OpenAPI App ID
   - **App Secret**: Your APSystems OpenAPI App Secret  
   - **System ID**: Your system ID from EMA portal
5. Click **Submit**

The integration will test the connection and create the sensors automatically.

## Troubleshooting

### Cannot Connect Error
- Verify your App ID and App Secret are correct
- Check your internet connection
- Ensure the APSystems API is accessible from your network

### Invalid Authentication
- Double-check your credentials
- Ensure your API access is active
- Contact APSystems support if credentials don't work

### No Data Showing
- Wait 5-10 minutes after setup for first data update
- Check the integration logs in Home Assistant
- Verify your system is online in the APSystems EMA portal

## Getting Help

- [GitHub Issues](https://github.com/skamphuis/HomeAssistant.APSystems/issues)
- [Home Assistant Community Forum](https://community.home-assistant.io/)
