# custom_components/domovra/coordinator.py
from __future__ import annotations

import logging
from datetime import timedelta
import aiohttp

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.helpers.aiohttp_client import async_get_clientsession

_LOGGER = logging.getLogger(__name__)

class DomovraCoordinator(DataUpdateCoordinator):
    """Récupère périodiquement le résumé depuis l'add-on Domovra."""

    def __init__(self, hass: HomeAssistant, base_url: str, scan_secs: int):
        self.hass = hass
        self.base_url = base_url.rstrip("/")
        self._session = async_get_clientsession(hass)

        super().__init__(
            hass,
            _LOGGER,
            name="DomovraCoordinator",
            update_interval=timedelta(seconds=int(scan_secs)),
        )

    async def _async_update_data(self):
        url = f"{self.base_url}/api/ha/summary"
        try:
            timeout = aiohttp.ClientTimeout(total=10)
            async with self._session.get(url, timeout=timeout) as resp:
                resp.raise_for_status()
                data = await resp.json()

                # Normalise les clés au cas où l'add-on renvoie encore *_count
                if isinstance(data, dict):
                    data.setdefault("products", data.get("products_count"))
                    data.setdefault("lots", data.get("lots_count"))
                    data.setdefault("soon", data.get("soon_count"))
                    data.setdefault("urgent", data.get("urgent_count"))

                return data
        except Exception as e:
            raise UpdateFailed(f"Domovra API error: {e}") from e
