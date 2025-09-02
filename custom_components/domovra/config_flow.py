# custom_components/domovra/config_flow.py

import re
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN, CONF_BASE_URL, ingress_path, ADDON_SLUG

# Détecte 127.0.0.1 / localhost pour normaliser vers l'Ingress
_LOCALHOST_RE = re.compile(r"^https?://(127\.0\.0\.1|localhost)(:\d+)?/?.*$", re.I)

class DomovraConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            base_url = str(user_input[CONF_BASE_URL]).rstrip("/")

            # Normalisation : toute URL locale → Ingress propre
            if _LOCALHOST_RE.match(base_url):
                base_url = ingress_path(ADDON_SLUG)

            # unique_id = base_url (normalisé) pour éviter les doublons d'entrée
            await self.async_set_unique_id(base_url)
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title="Domovra",
                data={CONF_BASE_URL: base_url},
            )

        # Par défaut, proposer l’Ingress
        default_url = ingress_path(ADDON_SLUG)
        schema = vol.Schema({
            vol.Required(CONF_BASE_URL, default=default_url): str
        })
        return self.async_show_form(step_id="user", data_schema=schema)

    @callback
    def async_get_options_flow(self, config_entry):
        return DomovraOptionsFlow(config_entry)


class DomovraOptionsFlow(config_entries.OptionsFlow):
    def __init__(self, entry):
        self.entry = entry

    async def async_step_init(self, user_input=None):
        scan = self.entry.options.get("scan_interval", 30)
        schema = vol.Schema({
            vol.Required("scan_interval", default=scan): int
        })
        if user_input:
            return self.async_create_entry(title="", data=user_input)
        return self.async_show_form(step_id="init", data_schema=schema)
