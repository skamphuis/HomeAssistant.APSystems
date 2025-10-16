"""Constants for the APSystems OpenAPI integration."""

DOMAIN = "apsystems_openapi"
CONF_SYSTEM_ID = "system_id"

# API Configuration
API_BASE_URL = "https://api.apsystemsema.com"
API_TIMEOUT = 30

# Update intervals
UPDATE_INTERVAL = 300  # 5 minutes

# Sensor types
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
    "lifetime_energy": {
        "name": "Lifetime Energy",
        "unit": "kWh",
        "icon": "mdi:solar-power",
        "state_class": "total_increasing",
        "device_class": "energy",
    },
    "max_power": {
        "name": "Max Power",
        "unit": "W",
        "icon": "mdi:flash",
        "state_class": "measurement",
        "device_class": "power",
    },
}
