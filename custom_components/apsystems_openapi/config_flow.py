"""Config flow for APSystems OpenAPI integration."""
from __future__ import annotations

import logging
from typing import Any

import aiohttp
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import APSystemsAPIAuthError, APSystemsAPIClient, APSystemsAPIError
from .const import CONF_SYSTEM_ID, DOMAIN

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_USERNAME, description="App ID"): str,
        vol.Required(CONF_PASSWORD, description="App Secret"): str,
        vol.Required(CONF_SYSTEM_ID, description="System ID"): str,
    }
)


class APSystemsConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for APSystems OpenAPI."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            app_id = user_input[CONF_USERNAME]
            app_secret = user_input[CONF_PASSWORD]
            system_id = user_input[CONF_SYSTEM_ID]

            # Test the connection
            session = async_get_clientsession(self.hass)
            client = APSystemsAPIClient(app_id, app_secret, system_id, session)

            try:
                if await client.test_connection():
                    # Create unique ID based on system ID
                    await self.async_set_unique_id(system_id)
                    self._abort_if_unique_id_configured()

                    return self.async_create_entry(
                        title=f"APSystems {system_id}",
                        data=user_input,
                    )
                else:
                    errors["base"] = "cannot_connect"
            except APSystemsAPIAuthError:
                errors["base"] = "invalid_auth"
            except APSystemsAPIError:
                errors["base"] = "cannot_connect"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )
