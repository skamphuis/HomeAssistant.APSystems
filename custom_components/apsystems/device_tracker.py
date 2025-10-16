"""Device tracker platform for APSystems integration."""

import logging
from typing import Any, Dict, List, Optional

from homeassistant.components.device_tracker import DeviceTracker
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import APSystemsDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up APSystems device tracker entities."""
    coordinator: APSystemsDataUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id]
    
    entities = []
    
    # System device tracker
    entities.append(APSystemsSystemDevice(coordinator))
    
    # Inverter device trackers
    if coordinator.data and "inverters" in coordinator.data:
        for inverter in coordinator.data["inverters"]:
            inverter_id = inverter.get("uid")
            if inverter_id:
                entities.append(APSystemsInverterDevice(coordinator, inverter_id))
    
    async_add_entities(entities)


class APSystemsSystemDevice(CoordinatorEntity, DeviceTracker):
    """Representation of an APSystems system device."""

    def __init__(self, coordinator: APSystemsDataUpdateCoordinator) -> None:
        """Initialize the device."""
        super().__init__(coordinator)
        self._attr_name = f"APSystems {coordinator.data.get('system_details', {}).get('name', 'Unknown System')}"
        self._attr_unique_id = f"{coordinator.system_id}_system"
        self._attr_icon = "mdi:solar-panel"

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        return DeviceInfo(
            identifiers={(DOMAIN, self.coordinator.system_id)},
            name=self._attr_name,
            manufacturer="APSystems",
            model=self.coordinator.data.get("system_details", {}).get("type", "Unknown"),
            sw_version="1.0.0",
        )

    @property
    def is_connected(self) -> bool:
        """Return if the device is connected."""
        if not self.coordinator.data:
            return False
        return True  # If we have data, the system is connected


class APSystemsInverterDevice(CoordinatorEntity, DeviceTracker):
    """Representation of an APSystems inverter device."""

    def __init__(self, coordinator: APSystemsDataUpdateCoordinator, inverter_id: str) -> None:
        """Initialize the device."""
        super().__init__(coordinator)
        self._inverter_id = inverter_id
        self._attr_name = f"APSystems Inverter {inverter_id}"
        self._attr_unique_id = f"{coordinator.system_id}_{inverter_id}"
        self._attr_icon = "mdi:solar-power"

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
            name=self._attr_name,
            manufacturer="APSystems",
            model=inverter_details.get("model", "Unknown") if inverter_details else "Unknown",
            sw_version=inverter_details.get("firmware", "Unknown") if inverter_details else "Unknown",
            via_device=(DOMAIN, self.coordinator.system_id),
        )

    @property
    def is_connected(self) -> bool:
        """Return if the device is connected."""
        if not self.coordinator.data:
            return False
        
        # Check if inverter data is available
        inverter_data = self.coordinator.data.get("inverter_data", {}).get(self._inverter_id, {})
        return bool(inverter_data)
