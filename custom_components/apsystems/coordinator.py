"""Data coordinator for APSystems integration."""

import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, UPDATE_INTERVAL
from .utils import APSystemsAPI

_LOGGER = logging.getLogger(__name__)


class APSystemsDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the APSystems API."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the coordinator."""
        self.entry = entry
        self.api = APSystemsAPI(
            entry.data["app_id"],
            entry.data["app_secret"]
        )
        self.system_id = entry.data["system_id"]
        
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=UPDATE_INTERVAL),
        )

    async def _async_update_data(self) -> Dict[str, Any]:
        """Update data via library."""
        try:
            # Get system details
            system_details = await self.hass.async_add_executor_job(
                self.api.get_system_details, self.system_id
            )
            
            # Get system summary energy
            system_energy = await self.hass.async_add_executor_job(
                self.api.get_system_summary_energy, self.system_id
            )
            
            # Get system inverters
            inverters = await self.hass.async_add_executor_job(
                self.api.get_system_inverters, self.system_id
            )
            
            # Get system meters if available
            try:
                meters = await self.hass.async_add_executor_job(
                    self.api.get_system_meters, self.system_id
                )
            except Exception:
                meters = {"data": []}
            
            # Get inverter data for each inverter
            inverter_data = {}
            if inverters.get("data"):
                for inverter in inverters["data"]:
                    inverter_id = inverter.get("uid")
                    if inverter_id:
                        try:
                            inverter_energy = await self.hass.async_add_executor_job(
                                self.api.get_inverter_summary_energy, 
                                self.system_id, 
                                inverter_id
                            )
                            inverter_data[inverter_id] = inverter_energy
                        except Exception as e:
                            _LOGGER.warning(f"Failed to get energy data for inverter {inverter_id}: {e}")
                            inverter_data[inverter_id] = {"data": {}}
            
            # Get today's date for daily energy
            today = datetime.now().strftime("%Y-%m-%d")
            
            # Get system energy for today
            try:
                system_energy_today = await self.hass.async_add_executor_job(
                    self.api.get_system_energy_period,
                    self.system_id,
                    today,
                    today
                )
            except Exception:
                system_energy_today = {"data": {}}
            
            return {
                "system_details": system_details.get("data", {}),
                "system_energy": system_energy.get("data", {}),
                "system_energy_today": system_energy_today.get("data", {}),
                "inverters": inverters.get("data", []),
                "meters": meters.get("data", []),
                "inverter_data": inverter_data,
                "last_update": datetime.now().isoformat(),
            }
            
        except Exception as error:
            raise UpdateFailed(f"Error communicating with API: {error}")

    async def get_inverter_energy_today(self, inverter_id: str) -> Dict[str, Any]:
        """Get today's energy data for a specific inverter."""
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            return await self.hass.async_add_executor_job(
                self.api.get_inverter_energy_period,
                self.system_id,
                inverter_id,
                today,
                today
            )
        except Exception as error:
            _LOGGER.error(f"Failed to get today's energy for inverter {inverter_id}: {error}")
            return {"data": {}}

    async def get_inverter_power_data(self, ecu_id: str) -> Dict[str, Any]:
        """Get power telemetry data for inverters under an ECU."""
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            return await self.hass.async_add_executor_job(
                self.api.get_inverter_energy_day,
                self.system_id,
                ecu_id,
                today,
                "power"
            )
        except Exception as error:
            _LOGGER.error(f"Failed to get power data for ECU {ecu_id}: {error}")
            return {"data": {}}
