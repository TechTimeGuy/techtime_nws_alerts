import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN

@callback
def configured_instances(hass):
    """Return a set of configured zone IDs already set up."""
    return {
        entry.data["zone_id"]
        for entry in hass.config_entries.async_entries(DOMAIN)
    }

class TechtimeNWSAlertsConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle the config flow for Techtime NWS Alerts."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    async def async_step_user(self, user_input=None):
        """Handle the initial step in the UI."""
        errors = {}

        if user_input is not None:
            zone_id = user_input["zone_id"]

            # Check if zone_id already exists
            if zone_id in configured_instances(self.hass):
                errors["base"] = "zone_exists"
            else:
                # Create entry with user inputs
                return self.async_create_entry(
                    title=f"Techtime NWS Alerts - {zone_id}",
                    data=user_input
                )

        # Default form fields
        data_schema = vol.Schema({
            vol.Required("zone_id"): str,
            vol.Optional("name", default="Techtime NWS Alerts"): str
        })

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors
        )
