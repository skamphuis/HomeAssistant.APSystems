"""Sensor platform for APSystems integration."""

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, SENSOR_TYPES
from .coordinator import APSystemsDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up APSystems sensor entities."""
    coordinator: APSystemsDataUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id]
    
    entities = []
    
    # System-level sensors
    entities.append(APSystemsSystemSensor(coordinator, "system_power"))
    entities.append(APSystemsSystemSensor(coordinator, "system_energy_today"))
    entities.append(APSystemsSystemSensor(coordinator, "system_energy_total"))
    
    # Inverter-level sensors
    if coordinator.data and "inverters" in coordinator.data:
        for inverter in coordinator.data["inverters"]:
            inverter_id = inverter.get("uid")
            if inverter_id:
                entities.append(APSystemsInverterSensor(coordinator, inverter_id, "inverter_power"))
                entities.append(APSystemsInverterSensor(coordinator, inverter_id, "inverter_energy_today"))
                entities.append(APSystemsInverterSensor(coordinator, inverter_id, "inverter_energy_total"))
    
    async_add_entities(entities)


class APSystemsSystemSensor(CoordinatorEntity, SensorEntity):
    """Representation of an APSystems system sensor."""

    def __init__(self, coordinator: APSystemsDataUpdateCoordinator, sensor_type: str) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._sensor_type = sensor_type
        self._attr_name = f"APSystems {SENSOR_TYPES[sensor_type]['name']}"
        self._attr_unique_id = f"{coordinator.system_id}_{sensor_type}"
        self._attr_icon = SENSOR_TYPES[sensor_type]["icon"]
        self._attr_native_unit_of_measurement = SENSOR_TYPES[sensor_type]["unit"]
        self._attr_device_class = SENSOR_TYPES[sensor_type].get("device_class")
        self._attr_state_class = SENSOR_TYPES[sensor_type].get("state_class")

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        return DeviceInfo(
            identifiers={(DOMAIN, self.coordinator.system_id)},
            name=f"APSystems {self.coordinator.data.get('system_details', {}).get('name', 'Unknown System')}",
            manufacturer="APSystems",
            model=self.coordinator.data.get("system_details", {}).get("type", "Unknown"),
            sw_version="1.0.0",
        )

    @property
    def native_value(self) -> Optional[float]:
        """Return the state of the sensor."""
        if not self.coordinator.data:
            return None
            
        try:
            system_energy = self.coordinator.data.get("system_energy", {})
            system_energy_today = self.coordinator.data.get("system_energy_today", {})
            
            if self._sensor_type == "system_power":
                # Get current power from system energy data
                power_value = system_energy.get("power", 0)
                return float(power_value) if power_value is not None else 0.0
            elif self._sensor_type == "system_energy_today":
                # Get today's energy
                energy_value = system_energy_today.get("energy", 0)
                return float(energy_value) if energy_value is not None else 0.0
            elif self._sensor_type == "system_energy_total":
                # Get total energy
                energy_value = system_energy.get("energy", 0)
                return float(energy_value) if energy_value is not None else 0.0
            
            return None
        except (ValueError, TypeError) as e:
            _LOGGER.warning(f"Error parsing system sensor value for {self._sensor_type}: {e}")
            return None


class APSystemsInverterSensor(CoordinatorEntity, SensorEntity):
    """Representation of an APSystems inverter sensor."""

    def __init__(self, coordinator: APSystemsDataUpdateCoordinator, inverter_id: str, sensor_type: str) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._inverter_id = inverter_id
        self._sensor_type = sensor_type
        self._attr_name = f"APSystems Inverter {inverter_id} {SENSOR_TYPES[sensor_type]['name']}"
        self._attr_unique_id = f"{coordinator.system_id}_{inverter_id}_{sensor_type}"
        self._attr_icon = SENSOR_TYPES[sensor_type]["icon"]
        self._attr_native_unit_of_measurement = SENSOR_TYPES[sensor_type]["unit"]
        self._attr_device_class = SENSOR_TYPES[sensor_type].get("device_class")
        self._attr_state_class = SENSOR_TYPES[sensor_type].get("state_class")

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        # Find inverter details
        inverter_details = None
        if self.coordinator.data and "inverters" in self.coordinator.data:
            for inverter in self.coordinator.data["inverters"]:
                if inverter.get("uid") == self._inverter_id:
                    inverter_details = inverter
                    break
        
        return DeviceInfo(
            identifiers={(DOMAIN, f"{self.coordinator.system_id}_{self._inverter_id}")},
            name=f"APSystems Inverter {self._inverter_id}",
            manufacturer="APSystems",
            model=inverter_details.get("model", "Unknown") if inverter_details else "Unknown",
            sw_version=inverter_details.get("firmware", "Unknown") if inverter_details else "Unknown",
            via_device=(DOMAIN, self.coordinator.system_id),
        )

    @property
    def native_value(self) -> Optional[float]:
        """Return the state of the sensor."""
        if not self.coordinator.data:
            return None
            
        try:
            inverter_data = self.coordinator.data.get("inverter_data", {}).get(self._inverter_id, {})
            
            if self._sensor_type == "inverter_power":
                # Get current power from inverter data
                power_value = inverter_data.get("power", 0)
                return float(power_value) if power_value is not None else 0.0
            elif self._sensor_type == "inverter_energy_today":
                # Get today's energy - this would need to be fetched separately
                # For now, return 0 as we'd need to make additional API calls
                return 0.0
            elif self._sensor_type == "inverter_energy_total":
                # Get total energy
                energy_value = inverter_data.get("energy", 0)
                return float(energy_value) if energy_value is not None else 0.0
            
            return None
        except (ValueError, TypeError) as e:
            _LOGGER.warning(f"Error parsing inverter sensor value for {self._inverter_id} {self._sensor_type}: {e}")
            return None
