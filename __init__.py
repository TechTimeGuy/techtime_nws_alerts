"""NWS Alerts integration."""

DOMAIN = "nws_alerts"

async def async_setup(hass, config):
    """Set up from YAML (optional)."""
    return True

async def async_setup_entry(hass, entry):
    """Set up from UI config flow."""
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "sensor")
    )
    return True

async def async_unload_entry(hass, entry):
    """Handle removal of config entry."""
    return await hass.config_entries.async_forward_entry_unload(entry, "sensor")
