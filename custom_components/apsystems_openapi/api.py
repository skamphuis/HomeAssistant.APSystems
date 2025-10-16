"""API client for APSystems OpenAPI."""
import logging
from datetime import datetime
from typing import Any

import aiohttp
import async_timeout

from .const import API_BASE_URL, API_TIMEOUT

_LOGGER = logging.getLogger(__name__)


class APSystemsAPIError(Exception):
    """Exception to indicate a general API error."""


class APSystemsAPIAuthError(APSystemsAPIError):
    """Exception to indicate an authentication error."""


class APSystemsAPIClient:
    """API client for APSystems OpenAPI."""

    def __init__(
        self,
        app_id: str,
        app_secret: str,
        system_id: str,
        session: aiohttp.ClientSession,
    ) -> None:
        """Initialize the API client."""
        self._app_id = app_id
        self._app_secret = app_secret
        self._system_id = system_id
        self._session = session
        self._base_url = API_BASE_URL

    async def _request(
        self,
        method: str,
        endpoint: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Make a request to the API."""
        url = f"{self._base_url}{endpoint}"
        
        # Add authentication headers
        headers = kwargs.get("headers", {})
        headers.update({
            "appId": self._app_id,
            "appSecret": self._app_secret,
        })
        kwargs["headers"] = headers

        try:
            async with async_timeout.timeout(API_TIMEOUT):
                async with self._session.request(method, url, **kwargs) as response:
                    response.raise_for_status()
                    data = await response.json()
                    
                    # Check API response code
                    if data.get("code") != "0":
                        error_msg = data.get("message", "Unknown error")
                        _LOGGER.error("API error: %s", error_msg)
                        if data.get("code") in ["401", "403"]:
                            raise APSystemsAPIAuthError(error_msg)
                        raise APSystemsAPIError(error_msg)
                    
                    return data
        except aiohttp.ClientResponseError as err:
            if err.status in (401, 403):
                raise APSystemsAPIAuthError(f"Authentication failed: {err}") from err
            raise APSystemsAPIError(f"API request failed: {err}") from err
        except aiohttp.ClientError as err:
            raise APSystemsAPIError(f"Connection error: {err}") from err
        except TimeoutError as err:
            raise APSystemsAPIError(f"Request timeout: {err}") from err

    async def test_connection(self) -> bool:
        """Test the API connection."""
        try:
            await self.get_system_info()
            return True
        except APSystemsAPIError:
            return False

    async def get_system_info(self) -> dict[str, Any]:
        """Get system information."""
        data = await self._request(
            "GET",
            f"/ecu/v1/systems/{self._system_id}/info",
        )
        return data.get("data", {})

    async def get_power_data(self) -> dict[str, Any]:
        """Get current power data."""
        data = await self._request(
            "GET",
            f"/ecu/v1/systems/{self._system_id}/power",
        )
        return data.get("data", {})

    async def get_energy_data(self, date: str | None = None) -> dict[str, Any]:
        """Get energy data for a specific date."""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        data = await self._request(
            "GET",
            f"/ecu/v1/systems/{self._system_id}/energy",
            params={"date": date},
        )
        return data.get("data", {})

    async def get_all_data(self) -> dict[str, Any]:
        """Get all sensor data."""
        try:
            power_data = await self.get_power_data()
            energy_data = await self.get_energy_data()
            
            return {
                "current_power": power_data.get("currentPower", 0),
                "today_energy": energy_data.get("todayEnergy", 0),
                "lifetime_energy": energy_data.get("lifetimeEnergy", 0),
                "max_power": power_data.get("maxPower", 0),
            }
        except APSystemsAPIError as err:
            _LOGGER.error("Error fetching data: %s", err)
            return {}
