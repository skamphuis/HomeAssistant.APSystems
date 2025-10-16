# Architecture Overview

## Integration Architecture

The APSystems OpenAPI integration follows Home Assistant's best practices for custom integrations.

```
┌─────────────────────────────────────────────────────────────────┐
│                      Home Assistant Core                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │           APSystems OpenAPI Integration                   │   │
│  │                                                           │   │
│  │  ┌─────────────┐    ┌──────────────┐   ┌────────────┐  │   │
│  │  │ Config Flow │───▶│    __init__  │──▶│  Sensors   │  │   │
│  │  │   (Setup)   │    │  (Platform)  │   │  (Entities)│  │   │
│  │  └─────────────┘    └──────────────┘   └────────────┘  │   │
│  │                              │                           │   │
│  │                              ▼                           │   │
│  │                     ┌────────────────┐                  │   │
│  │                     │  Coordinator   │                  │   │
│  │                     │  (Updates)     │                  │   │
│  │                     └────────────────┘                  │   │
│  │                              │                           │   │
│  │                              ▼                           │   │
│  │                     ┌────────────────┐                  │   │
│  │                     │  API Client    │                  │   │
│  │                     └────────────────┘                  │   │
│  └───────────────────────────│───────────────────────────┘   │
│                                │                               │
└────────────────────────────────┼───────────────────────────────┘
                                 │
                                 │ HTTPS (REST API)
                                 │
                       ┌─────────▼──────────┐
                       │  APSystems OpenAPI │
                       │  api.apsystemsema  │
                       │      .com          │
                       └────────────────────┘
                                 │
                                 │
                       ┌─────────▼──────────┐
                       │   APSystems EMA    │
                       │   Cloud Platform   │
                       └────────────────────┘
                                 │
                                 │
                       ┌─────────▼──────────┐
                       │  Solar Inverter    │
                       │    (Hardware)      │
                       └────────────────────┘
```

## Component Flow

### 1. Initial Setup (Config Flow)
```
User → Config Flow UI → Test Connection → Create Entry → Load Platform
```

1. User enters credentials (App ID, App Secret, System ID)
2. Config flow validates credentials by testing API connection
3. If successful, creates a config entry
4. Integration loads and initializes

### 2. Platform Initialization
```
Entry → __init__.py → Create API Client → Load Sensors → Start Coordinator
```

1. `async_setup_entry` creates API client instance
2. Stores client in hass.data
3. Forwards setup to sensor platform
4. Sensor platform creates coordinator and entities

### 3. Data Update Cycle
```
┌─────────────────────────────────────────────────────────┐
│                     Update Cycle                        │
│                  (Every 5 minutes)                       │
└─────────────────────────────────────────────────────────┘
           │
           ▼
    ┌──────────────┐
    │ Coordinator  │
    │    Timer     │
    └──────────────┘
           │
           ▼
    ┌──────────────┐
    │ API Client   │
    │ get_all_data │
    └──────────────┘
           │
           ├──▶ get_power_data()   → Current Power, Max Power
           │
           └──▶ get_energy_data()  → Today Energy, Lifetime Energy
           │
           ▼
    ┌──────────────┐
    │  Process &   │
    │  Normalize   │
    └──────────────┘
           │
           ▼
    ┌──────────────┐
    │  Update All  │
    │   Sensors    │
    └──────────────┘
           │
           ▼
    ┌──────────────┐
    │  Home        │
    │  Assistant   │
    │  UI Update   │
    └──────────────┘
```

## File Structure

```
custom_components/apsystems_openapi/
├── __init__.py           # Integration setup and platform loading
├── config_flow.py        # UI configuration flow
├── sensor.py            # Sensor platform and entities
├── api.py               # API client for APSystems OpenAPI
├── const.py             # Constants and configuration
├── manifest.json        # Integration metadata
├── strings.json         # UI strings
└── translations/
    └── en.json          # English translations
```

## Key Components

### __init__.py
- Entry point for the integration
- Handles setup and teardown
- Creates API client instance
- Manages platform loading

### config_flow.py
- Provides UI for configuration
- Validates credentials
- Creates config entries
- Prevents duplicate configurations

### sensor.py
- Defines sensor entities
- Creates data update coordinator
- Manages sensor state updates
- Provides device information

### api.py
- Handles all API communication
- Implements authentication
- Provides error handling
- Normalizes API responses

### const.py
- Defines constants
- Sensor type definitions
- Configuration keys
- Default values

## Data Flow

### Authentication
```
App ID + App Secret → Request Headers → APSystems API
```

### Power Data Request
```
GET /ecu/v1/systems/{system_id}/power
   ↓
Response: { currentPower, maxPower }
   ↓
Sensor: sensor.apsystems_current_power
```

### Energy Data Request
```
GET /ecu/v1/systems/{system_id}/energy?date=YYYY-MM-DD
   ↓
Response: { todayEnergy, lifetimeEnergy }
   ↓
Sensors: sensor.apsystems_today_energy
         sensor.apsystems_lifetime_energy
```

## Error Handling

```
API Request
    │
    ├─▶ Success → Update Sensors
    │
    ├─▶ Auth Error → Log Error, Mark Unavailable
    │
    ├─▶ Connection Error → Retry, Log Warning
    │
    └─▶ Timeout → Retry, Log Warning
```

## State Management

- **Available**: API responding, data current
- **Unavailable**: API error, no connection
- **Unknown**: Initial state before first update

## Update Strategy

- **Polling Interval**: 300 seconds (5 minutes)
- **Retry Logic**: Built into Home Assistant coordinator
- **Backoff**: Automatic on repeated failures
- **Cache**: Coordinator maintains last successful state

## Security

- Credentials stored encrypted in Home Assistant
- HTTPS communication with API
- No local storage of sensitive data
- API credentials in request headers only

## Performance Considerations

- Async/await for non-blocking operations
- Single shared aiohttp session
- Batch API calls in get_all_data()
- Coordinator prevents duplicate updates
- Efficient state updates to UI

## Integration with Home Assistant

### Energy Dashboard
- `today_energy` sensor auto-detected
- `state_class: total_increasing` enables tracking
- `device_class: energy` for proper categorization

### Device Registry
- Single device per system ID
- All sensors grouped under device
- Device info includes manufacturer, model

### State Class Support
- Measurement: Current Power, Max Power
- Total Increasing: Today Energy, Lifetime Energy

### Unit Handling
- Power: Watts (W)
- Energy: Kilowatt-hours (kWh)
- Uses Home Assistant standard units
