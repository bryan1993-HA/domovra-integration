import logging
from datetime import timedelta
import aiohttp

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.helpers.aiohttp_client import async_get_clientsession  # <-- import correct

from .const import DEFAULT_SCAN_SECS

_LOGGER = logging.getLogger(__name__)

class DomovraCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, base_url: str):
        self.hass = hass
        self._session = async_get_clientsession(hass)  # <-- appel correct
        self.base_url = base_url.rstrip("/")
        super().__init__(
            hass,
            _LOGGER,
            name="DomovraCoordinator",
            update_interval=timedelta(seconds=DEFAULT_SCAN_SECS),
        )

    async def _async_update_data(self):
        url = f"{self.base_url}/api/ha/summary"
        try:
            timeout = aiohttp.ClientTimeout(total=10)
            async with self._session.get(url, timeout=timeout) as resp:
                resp.raise_for_status()
                return await resp.json()
        except Exception as e:
            raise UpdateFailed(f"Domovra API error: {e}") from e
