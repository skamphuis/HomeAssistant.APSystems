"""Config flow for APSystems integration."""

import logging
from typing import Any, Dict, Optional

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN
from .utils import APSystemsAPI

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required("app_id"): str,
        vol.Required("app_secret"): str,
        vol.Required("system_id"): str,
    }
)


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""


async def validate_input(hass: HomeAssistant, data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate the user input allows us to connect."""
    api = APSystemsAPI(data["app_id"], data["app_secret"])
    
    try:
        # Test the connection by getting system details
        system_details = await hass.async_add_executor_job(
            api.get_system_details, data["system_id"]
        )
        
        if system_details.get("code") != 0:
            raise InvalidAuth("Invalid credentials or system ID")
            
        return {
            "title": f"APSystems {data['system_id']}",
            "system_name": system_details.get("data", {}).get("name", "Unknown System"),
        }
        
    except Exception as err:
        if "Invalid" in str(err):
            raise InvalidAuth("Invalid credentials or system ID") from err
        raise CannotConnect("Unable to connect to APSystems API") from err


class APSystemsConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for APSystems."""

    VERSION = 1

    async def async_step_user(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(
                step_id="user", data_schema=STEP_USER_DATA_SCHEMA
            )

        errors = {}

        try:
            info = await validate_input(self.hass, user_input)
        except CannotConnect:
            errors["base"] = "cannot_connect"
        except InvalidAuth:
            errors["base"] = "invalid_auth"
        except Exception:  # pylint: disable=broad-except
            _LOGGER.exception("Unexpected exception")
            errors["base"] = "unknown"
        else:
            return self.async_create_entry(title=info["title"], data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )
