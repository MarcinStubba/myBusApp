import logging
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from . import DOMAIN

_LOGGER = logging.getLogger(__name__)

CONF_API_BASE = "api_base"

class MyBusAppConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for MyBusApp."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle user configuration."""
        errors = {}

        if user_input is not None:
            return self.async_create_entry(title="MyBusApp", data=user_input)

        data_schema = vol.Schema({vol.Required(CONF_API_BASE, default="http://localhost:5000"): str})
        return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Return the options flow handler."""
        return OptionsFlowHandler(config_entry)

class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options flow for MyBusApp."""

    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        return self.async_show_form(step_id="init", data_schema=vol.Schema({}))
