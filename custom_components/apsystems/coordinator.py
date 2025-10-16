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
            # Initialize default data structure
            data = {
                "system_details": {},
                "system_energy": {},
                "system_energy_today": {},
                "inverters": [],
                "meters": [],
                "inverter_data": {},
                "last_update": datetime.now().isoformat(),
                "errors": []
            }
            
            # Get system details with error handling
            try:
                system_details = await self.hass.async_add_executor_job(
                    self.api.get_system_details, self.system_id
                )
                if system_details.get("code") == 0:
                    data["system_details"] = system_details.get("data", {})
                else:
                    _LOGGER.warning(f"System details error: {system_details.get('message', 'Unknown error')}")
                    data["errors"].append(f"System details: {system_details.get('message', 'Unknown error')}")
            except Exception as e:
                _LOGGER.error(f"Failed to get system details: {e}")
                data["errors"].append(f"System details: {e}")
            
            # Get system summary energy with error handling
            try:
                system_energy = await self.hass.async_add_executor_job(
                    self.api.get_system_summary_energy, self.system_id
                )
                if system_energy.get("code") == 0:
                    data["system_energy"] = system_energy.get("data", {})
                else:
                    _LOGGER.warning(f"System energy error: {system_energy.get('message', 'Unknown error')}")
                    data["errors"].append(f"System energy: {system_energy.get('message', 'Unknown error')}")
            except Exception as e:
                _LOGGER.error(f"Failed to get system energy: {e}")
                data["errors"].append(f"System energy: {e}")
            
            # Get system inverters with error handling
            try:
                inverters = await self.hass.async_add_executor_job(
                    self.api.get_system_inverters, self.system_id
                )
                if inverters.get("code") == 0:
                    data["inverters"] = inverters.get("data", [])
                else:
                    _LOGGER.warning(f"Inverters error: {inverters.get('message', 'Unknown error')}")
                    data["errors"].append(f"Inverters: {inverters.get('message', 'Unknown error')}")
            except Exception as e:
                _LOGGER.error(f"Failed to get inverters: {e}")
                data["errors"].append(f"Inverters: {e}")
            
            # Get system meters if available (optional)
            try:
                meters = await self.hass.async_add_executor_job(
                    self.api.get_system_meters, self.system_id
                )
                if meters.get("code") == 0:
                    data["meters"] = meters.get("data", [])
            except Exception as e:
                _LOGGER.debug(f"Meters not available: {e}")
                data["meters"] = []
            
            # Get inverter data for each inverter with error handling
            if data["inverters"]:
                for inverter in data["inverters"]:
                    inverter_id = inverter.get("uid")
                    if inverter_id:
                        try:
                            inverter_energy = await self.hass.async_add_executor_job(
                                self.api.get_inverter_summary_energy, 
                                self.system_id, 
                                inverter_id
                            )
                            if inverter_energy.get("code") == 0:
                                data["inverter_data"][inverter_id] = inverter_energy.get("data", {})
                            else:
                                _LOGGER.warning(f"Inverter {inverter_id} energy error: {inverter_energy.get('message', 'Unknown error')}")
                                data["inverter_data"][inverter_id] = {}
                        except Exception as e:
                            _LOGGER.warning(f"Failed to get energy data for inverter {inverter_id}: {e}")
                            data["inverter_data"][inverter_id] = {}
            
            # Get today's date for daily energy
            today = datetime.now().strftime("%Y-%m-%d")
            
            # Get system energy for today with error handling
            try:
                system_energy_today = await self.hass.async_add_executor_job(
                    self.api.get_system_energy_period,
                    self.system_id,
                    today,
                    today
                )
                if system_energy_today.get("code") == 0:
                    data["system_energy_today"] = system_energy_today.get("data", {})
                else:
                    _LOGGER.warning(f"Today's energy error: {system_energy_today.get('message', 'Unknown error')}")
            except Exception as e:
                _LOGGER.warning(f"Failed to get today's energy: {e}")
                data["system_energy_today"] = {}
            
            return data
            
        except Exception as error:
            _LOGGER.error(f"Critical error in coordinator update: {error}")
            # Return minimal data structure to prevent crashes
            return {
                "system_details": {},
                "system_energy": {},
                "system_energy_today": {},
                "inverters": [],
                "meters": [],
                "inverter_data": {},
                "last_update": datetime.now().isoformat(),
                "errors": [f"Critical error: {error}"]
            }

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
