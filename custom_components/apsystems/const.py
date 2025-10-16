"""Constants for the APSystems integration."""

DOMAIN = "apsystems_api"

# API Configuration
BASE_URL = "https://api.apsystemsema.com:9282"
API_VERSION = "v2"

# API Endpoints
ENDPOINT_SYSTEM_DETAILS = "/user/api/v2/systems/details/{sid}"
ENDPOINT_SYSTEM_INVERTERS = "/user/api/v2/systems/{sid}/devices/inverter"
ENDPOINT_SYSTEM_METERS = "/user/api/v2/systems/{sid}/devices/meter"
ENDPOINT_SYSTEM_SUMMARY_ENERGY = "/user/api/v2/systems/{sid}/energy/summary"
ENDPOINT_SYSTEM_ENERGY_PERIOD = "/user/api/v2/systems/{sid}/energy/period"
ENDPOINT_ECU_SUMMARY_ENERGY = "/user/api/v2/systems/{sid}/devices/ecu/{eid}/energy/summary"
ENDPOINT_ECU_ENERGY_PERIOD = "/user/api/v2/systems/{sid}/devices/ecu/{eid}/energy/period"
ENDPOINT_INVERTER_SUMMARY_ENERGY = "/user/api/v2/systems/{sid}/devices/inverter/{uid}/energy/summary"
ENDPOINT_INVERTER_ENERGY_PERIOD = "/user/api/v2/systems/{sid}/devices/inverter/{uid}/energy/period"
ENDPOINT_INVERTER_ENERGY_DAY = "/user/api/v2/systems/{sid}/devices/inverter/batch/energy/{eid}"

# Update intervals
UPDATE_INTERVAL = 300  # 5 minutes
UPDATE_INTERVAL_FAST = 60  # 1 minute for power data

# Sensor types
SENSOR_TYPES = {
    "system_power": {
        "name": "System Power",
        "unit": "W",
        "icon": "mdi:solar-power",
        "device_class": "power",
    },
    "system_energy_today": {
        "name": "System Energy Today",
        "unit": "kWh",
        "icon": "mdi:solar-panel",
        "device_class": "energy",
        "state_class": "total_increasing",
    },
    "system_energy_total": {
        "name": "System Energy Total",
        "unit": "kWh",
        "icon": "mdi:solar-panel",
        "device_class": "energy",
        "state_class": "total_increasing",
    },
    "inverter_power": {
        "name": "Inverter Power",
        "unit": "W",
        "icon": "mdi:solar-power",
        "device_class": "power",
    },
    "inverter_energy_today": {
        "name": "Inverter Energy Today",
        "unit": "kWh",
        "icon": "mdi:solar-panel",
        "device_class": "energy",
        "state_class": "total_increasing",
    },
    "inverter_energy_total": {
        "name": "Inverter Energy Total",
        "unit": "kWh",
        "icon": "mdi:solar-panel",
        "device_class": "energy",
        "state_class": "total_increasing",
    },
}

# Device types
DEVICE_TYPES = {
    "system": "System",
    "ecu": "ECU",
    "inverter": "Inverter",
    "meter": "Meter",
}
