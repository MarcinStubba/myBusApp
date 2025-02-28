DOMAIN = "mybusapp"

import logging
import requests
import voluptuous as vol
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.aiohttp_client import async_get_clientsession

_LOGGER = logging.getLogger(__name__)

CONF_API_BASE = "api_base"
DEFAULT_API_BASE = "http://localhost:5000"

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Optional(CONF_API_BASE, default=DEFAULT_API_BASE): cv.url,
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the integration from configuration.yaml."""
    hass.data.setdefault(DOMAIN, {})
    
    if DOMAIN in config:
        hass.data[DOMAIN][CONF_API_BASE] = config[DOMAIN].get(CONF_API_BASE, DEFAULT_API_BASE)
    
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up the integration from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data
    
    hass.async_create_task(hass.config_entries.async_forward_entry_setup(entry, "sensor"))
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    await hass.config_entries.async_forward_entry_unload(entry, "sensor")
    hass.data[DOMAIN].pop(entry.entry_id)
    return True

class MyBusAPI:
    """Class to interact with the NextBus API."""
    def __init__(self, hass: HomeAssistant, api_base: str):
        """Initialize the API client."""
        self.hass = hass
        self.api_base = api_base
        self.session = async_get_clientsession(hass)

    async def get_route_list(self, agency: str):
        """Fetch route list for a given agency."""
        url = f"{self.api_base}/routeList/{agency}"
        async with self.session.get(url) as response:
            if response.status == 200:
                return await response.json()
            _LOGGER.error("Error fetching route list: %s", response.status)
            return None

    async def get_predictions(self, agency: str, stop_id: str):
        """Fetch predictions for a stop."""
        url = f"{self.api_base}/predictions/bystopid/{agency}/{stop_id}"
        async with self.session.get(url) as response:
            if response.status == 200:
                return await response.json()
            _LOGGER.error("Error fetching predictions: %s", response.status)
            return None
