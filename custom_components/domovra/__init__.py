# custom_components/domovra/__init__.py
from __future__ import annotations
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN, PLATFORMS, CONF_BASE_URL, DEFAULT_SCAN_SECS
from .coordinator import DomovraCoordinator

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    base_url: str = entry.data[CONF_BASE_URL]
    scan_secs: int = entry.options.get("scan_interval", DEFAULT_SCAN_SECS)

    coordinator = DomovraCoordinator(hass, base_url, scan_secs)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {
        "coordinator": coordinator,
        "base_url": base_url,
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Si l'utilisateur change les options, on recrée proprement le coordinator
    entry.async_on_unload(entry.add_update_listener(async_options_updated))
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)
    return unload_ok

async def async_options_updated(hass: HomeAssistant, entry: ConfigEntry):
    # Recharge l'entrée pour appliquer le nouvel intervalle de scan
    await hass.config_entries.async_reload(entry.entry_id)
