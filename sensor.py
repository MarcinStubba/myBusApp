import logging
from datetime import timedelta
from homeassistant.helpers.entity import Entity
from . import DOMAIN, MyBusAPI

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(seconds=30)

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the sensors."""
    api_base = entry.data["api_base"]
    api = MyBusAPI(hass, api_base)

    agencies = ["sf-muni"]  # Example, you can fetch this dynamically
    sensors = [BusRouteSensor(api, agency) for agency in agencies]
    async_add_entities(sensors, True)

class BusRouteSensor(Entity):
    """A sensor for tracking bus routes."""

    def __init__(self, api, agency):
        """Initialize the sensor."""
        self.api = api
        self.agency = agency
        self._state = None
        self._attributes = {}

    async def async_update(self):
        """Fetch new state data."""
        data = await self.api.get_route_list(self.agency)
        if data:
            self._state = len(data)
            self._attributes["routes"] = data

    @property
    def name(self):
        return f"{self.agency} Routes"

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return self._attributes
