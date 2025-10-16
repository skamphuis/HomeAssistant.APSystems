"""Support for APSystems OpenAPI sensors."""
from __future__ import annotations

from datetime import timedelta
import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfEnergy, UnitOfPower
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)

from .api import APSystemsAPIClient, APSystemsAPIError
from .const import CONF_SYSTEM_ID, DOMAIN, SENSOR_TYPES, UPDATE_INTERVAL

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up APSystems sensors from a config entry."""
    client: APSystemsAPIClient = hass.data[DOMAIN][entry.entry_id]
    system_id = entry.data[CONF_SYSTEM_ID]

    coordinator = APSystemsDataUpdateCoordinator(hass, client)
    await coordinator.async_config_entry_first_refresh()

    entities = [
        APSystemsSensor(coordinator, system_id, sensor_type)
        for sensor_type in SENSOR_TYPES
    ]

    async_add_entities(entities)


class APSystemsDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching APSystems data."""

    def __init__(self, hass: HomeAssistant, client: APSystemsAPIClient) -> None:
        """Initialize."""
        self.client = client

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=UPDATE_INTERVAL),
        )

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from API."""
        try:
            data = await self.client.get_all_data()
            if not data:
                raise UpdateFailed("No data received from API")
            return data
        except APSystemsAPIError as err:
            raise UpdateFailed(f"Error communicating with API: {err}") from err


class APSystemsSensor(CoordinatorEntity, SensorEntity):
    """Representation of an APSystems sensor."""

    def __init__(
        self,
        coordinator: APSystemsDataUpdateCoordinator,
        system_id: str,
        sensor_type: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._sensor_type = sensor_type
        self._system_id = system_id
        self._attr_name = f"APSystems {SENSOR_TYPES[sensor_type]['name']}"
        self._attr_unique_id = f"{system_id}_{sensor_type}"
        self._attr_icon = SENSOR_TYPES[sensor_type]["icon"]

        # Set device class and state class
        device_class = SENSOR_TYPES[sensor_type].get("device_class")
        if device_class == "power":
            self._attr_device_class = device_class
            self._attr_native_unit_of_measurement = UnitOfPower.WATT
        elif device_class == "energy":
            self._attr_device_class = device_class
            self._attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR

        state_class = SENSOR_TYPES[sensor_type].get("state_class")
        if state_class == "measurement":
            self._attr_state_class = SensorStateClass.MEASUREMENT
        elif state_class == "total_increasing":
            self._attr_state_class = SensorStateClass.TOTAL_INCREASING

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        if self.coordinator.data:
            return self.coordinator.data.get(self._sensor_type)
        return None

    @property
    def device_info(self) -> dict[str, Any]:
        """Return device information."""
        return {
            "identifiers": {(DOMAIN, self._system_id)},
            "name": f"APSystems {self._system_id}",
            "manufacturer": "APSystems",
            "model": "EMA",
        }
