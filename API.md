# API Reference

## APSystems OpenAPI Integration

This document provides technical details about the APSystems OpenAPI integration for developers.

## API Client

### APSystemsAPIClient

The main API client class that handles communication with the APSystems OpenAPI.

#### Constructor

```python
APSystemsAPIClient(
    app_id: str,
    app_secret: str,
    system_id: str,
    session: aiohttp.ClientSession
)
```

**Parameters:**
- `app_id`: Your APSystems OpenAPI App ID
- `app_secret`: Your APSystems OpenAPI App Secret
- `system_id`: Your system ID from the EMA portal
- `session`: An aiohttp ClientSession instance

#### Methods

##### test_connection()

```python
async def test_connection() -> bool
```

Tests the API connection by attempting to fetch system information.

**Returns:** `True` if connection is successful, `False` otherwise

##### get_system_info()

```python
async def get_system_info() -> dict[str, Any]
```

Retrieves system information from the API.

**Returns:** Dictionary containing system information

**Raises:**
- `APSystemsAPIError`: For general API errors
- `APSystemsAPIAuthError`: For authentication errors

##### get_power_data()

```python
async def get_power_data() -> dict[str, Any]
```

Retrieves current power generation data.

**Returns:** Dictionary with keys:
- `currentPower`: Current power in watts
- `maxPower`: Maximum power capacity in watts

##### get_energy_data(date: str | None = None)

```python
async def get_energy_data(date: str | None = None) -> dict[str, Any]
```

Retrieves energy production data for a specific date.

**Parameters:**
- `date`: Date string in format "YYYY-MM-DD" (optional, defaults to today)

**Returns:** Dictionary with keys:
- `todayEnergy`: Energy produced today in kWh
- `lifetimeEnergy`: Total energy produced in kWh

##### get_all_data()

```python
async def get_all_data() -> dict[str, Any]
```

Retrieves all sensor data in a single call.

**Returns:** Dictionary with keys:
- `current_power`: Current power in watts
- `today_energy`: Today's energy in kWh
- `lifetime_energy`: Lifetime energy in kWh
- `max_power`: Maximum power in watts

## API Endpoints

The integration uses the following APSystems OpenAPI endpoints:

### Base URL
```
https://api.apsystemsema.com
```

### Authentication

All requests must include the following headers:
- `appId`: Your App ID
- `appSecret`: Your App Secret

### Endpoints

#### Get System Information
```
GET /ecu/v1/systems/{system_id}/info
```

#### Get Power Data
```
GET /ecu/v1/systems/{system_id}/power
```

#### Get Energy Data
```
GET /ecu/v1/systems/{system_id}/energy?date=YYYY-MM-DD
```

## Response Format

All API responses follow this structure:

```json
{
  "code": "0",
  "message": "Success",
  "data": {
    // Response data here
  }
}
```

**Response Codes:**
- `0`: Success
- `401`: Unauthorized
- `403`: Forbidden
- Other codes indicate various errors

## Error Handling

### Exception Classes

#### APSystemsAPIError

Base exception class for API errors.

```python
class APSystemsAPIError(Exception):
    """Exception to indicate a general API error."""
```

#### APSystemsAPIAuthError

Exception for authentication-related errors.

```python
class APSystemsAPIAuthError(APSystemsAPIError):
    """Exception to indicate an authentication error."""
```

## Coordinator

### APSystemsDataUpdateCoordinator

Manages data fetching and updates for all sensors.

```python
class APSystemsDataUpdateCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, client: APSystemsAPIClient)
```

**Update Interval:** 300 seconds (5 minutes)

## Sensors

### Sensor Types

All sensors are defined in `const.py`:

```python
SENSOR_TYPES = {
    "current_power": {
        "name": "Current Power",
        "unit": "W",
        "icon": "mdi:solar-power",
        "state_class": "measurement",
        "device_class": "power",
    },
    "today_energy": {
        "name": "Today Energy",
        "unit": "kWh",
        "icon": "mdi:solar-power",
        "state_class": "total_increasing",
        "device_class": "energy",
    },
    # ... etc
}
```

### Sensor Entity IDs

Sensors are created with the following entity ID format:
```
sensor.apsystems_{sensor_type}
```

Example: `sensor.apsystems_current_power`

## Configuration Flow

The integration uses Home Assistant's config flow for setup:

1. User enters credentials (App ID, App Secret, System ID)
2. Integration validates credentials by testing the connection
3. If successful, creates a config entry with unique ID based on System ID
4. Sensors are automatically created

## Constants

Key constants defined in `const.py`:

- `DOMAIN`: "apsystems_openapi"
- `API_BASE_URL`: "https://api.apsystemsema.com"
- `API_TIMEOUT`: 30 seconds
- `UPDATE_INTERVAL`: 300 seconds (5 minutes)

## Development

### Testing

To test the integration:

1. Install in Home Assistant development environment
2. Configure with valid credentials
3. Check logs for errors: `Settings > System > Logs`
4. Monitor sensor states in Developer Tools > States

### Logging

Enable debug logging in `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.apsystems_openapi: debug
```

## API Reference Links

- [APSystems OpenAPI Documentation](https://file.apsystemsema.com:8083/apsystems/resource/openapi/Apsystems_OpenAPI_User_Manual_End_User_EN.pdf)
- [Home Assistant Developer Documentation](https://developers.home-assistant.io/)
- [Home Assistant Integration Development](https://developers.home-assistant.io/docs/creating_integration_manifest)
