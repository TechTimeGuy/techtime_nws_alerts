import logging
from datetime import timedelta
import aiohttp
import async_timeout

from homeassistant.helpers.entity import Entity
from homeassistant.const import CONF_NAME
from .const import DOMAIN  # DOMAIN = "techtime_nws_alerts"

SCAN_INTERVAL = timedelta(minutes=5)

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the Techtime NWS Alerts sensor from a config entry."""
    zone_id = config_entry.data.get("zone_id")
    name = config_entry.data.get("name", "Techtime NWS Alerts")

    async_add_entities([TechtimeNWSAlertSensor(name, zone_id)], True)


class TechtimeNWSAlertSensor(Entity):
    """Representation of a Techtime NWS Alert Sensor."""

    def __init__(self, name, zone_id):
        """Initialize the sensor."""
        self._name = name
        self._zone_id = zone_id
        self._state = "No Alerts"
        self._attributes = {
            "headline": "Loading...",
            "description": "Fetching latest alerts...",
            "effective": None,
            "expires": None,
        }

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def extra_state_attributes(self):
        """Return additional state attributes."""
        return self._attributes

    async def async_update(self):
        """Fetch new state data for the sensor asynchronously."""
        url = f"https://api.weather.gov/alerts/active/zone/{self._zone_id}"
        headers = {
            "Accept": "application/ld+json",
            "User-Agent": "techtimeguy.com (youremail@domain.com)"  # Replace with your site/email
        }

        _LOGGER.debug("Fetching NWS alerts from URL: %s", url)

        try:
            async with aiohttp.ClientSession() as session:
                with async_timeout.timeout(10):
                    response = await session.get(url, headers=headers)
                    if response.status != 200:
                        _LOGGER.error("HTTP Error: %s when fetching NWS alerts", response.status)
                        self._state = "Error"
                        self._attributes = {}
                        return

                    data = await response.json()

            _LOGGER.debug("NWS API response: %s", data)

            if isinstance(data, dict) and '@graph' in data:
                graph = data['@graph']

                if graph:
                    first_alert = graph[0]
                    properties = first_alert

                    self._state = properties.get('event', "Unknown Event")
                    self._attributes = {
                        "headline": properties.get('headline', "No headline provided."),
                        "description": properties.get('description', "No description available."),
                        "effective": properties.get('effective', "Unknown effective time."),
                        "expires": properties.get('expires', "Unknown expiration time."),
                        "instruction": properties.get('instruction', "No instructions available."),
                        "severity": properties.get('severity', "Unknown severity"),
                        "certainty": properties.get('certainty', "Unknown certainty"),
                        "urgency": properties.get('urgency', "Unknown urgency"),
                    }

                    _LOGGER.info("Techtime NWS Alerts - Active alert: %s", self._attributes['headline'])
                else:
                    self._state = "No Alerts"
                    self._attributes = {
                        "headline": "No active alerts.",
                        "description": "There are currently no weather alerts.",
                        "effective": None,
                        "expires": None,
                        "instruction": None,
                        "severity": None,
                        "certainty": None,
                        "urgency": None,
                    }
                    _LOGGER.info("Techtime NWS Alerts - No active alerts.")
            else:
                _LOGGER.error("Unexpected API response structure from NWS: %s", data)
                self._state = "Error"
                self._attributes = {}

        except asyncio.TimeoutError:
            _LOGGER.error("Timeout while fetching data from NWS API.")
            self._state = "Error"
            self._attributes = {}
        except aiohttp.ClientError as err:
            _LOGGER.error("Client error fetching NWS alerts: %s", err)
            self._state = "Error"
            self._attributes = {}
        except Exception as err:
            _LOGGER.error("Unexpected error: %s", err)
            self._state = "Error"
            self._attributes = {}
