# custom_components/domovra/config_flow.py
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN, CONF_BASE_URL, DEFAULT_SCAN_SECS

class DomovraConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            base_url = str(user_input[CONF_BASE_URL]).rstrip("/")
            await self.async_set_unique_id(base_url)
            self._abort_if_unique_id_configured()
            return self.async_create_entry(
                title="Domovra",
                data={CONF_BASE_URL: base_url},
                options={"scan_interval": DEFAULT_SCAN_SECS},
            )

        schema = vol.Schema({
            vol.Required(CONF_BASE_URL, default="http://127.0.0.1:8099"): str
        })
        return self.async_show_form(step_id="user", data_schema=schema)

    @callback
    def async_get_options_flow(self, config_entry):
        return DomovraOptionsFlow(config_entry)


class DomovraOptionsFlow(config_entries.OptionsFlow):
    def __init__(self, entry):
        self.entry = entry

    async def async_step_init(self, user_input=None):
        scan = self.entry.options.get("scan_interval", DEFAULT_SCAN_SECS)
        schema = vol.Schema({
            vol.Required("scan_interval", default=scan): int
        })
        if user_input:
            return self.async_create_entry(title="", data=user_input)
        return self.async_show_form(step_id="init", data_schema=schema)
