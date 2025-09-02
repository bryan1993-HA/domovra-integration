# custom_components/domovra/__init__.py

from __future__ import annotations
import re
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import (
    DOMAIN, PLATFORMS, CONF_BASE_URL,
    ingress_path, ADDON_SLUG,
)
from .coordinator import DomovraCoordinator

# Reconnaît une ancienne URL locale à migrer vers l’Ingress
_LOCALHOST_RE = re.compile(r"^https?://(127\.0\.0\.1|localhost)(:\d+)?/?.*$", re.I)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    base_url: str = entry.data.get(CONF_BASE_URL, "").rstrip("/")

    # Migration silencieuse : si ancien http://127.0.0.1:XXXX → /hassio/ingress/<slug>
    if not base_url or _LOCALHOST_RE.match(base_url):
        base_url = ingress_path(ADDON_SLUG)
        hass.config_entries.async_update_entry(entry, data={CONF_BASE_URL: base_url})

    coordinator = DomovraCoordinator(hass, base_url)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {
        "coordinator": coordinator,
        "base_url": base_url,
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)
    return unload_ok
