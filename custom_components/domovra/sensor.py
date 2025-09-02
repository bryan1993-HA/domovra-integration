# custom_components/domovra/sensor.py
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN, MANUFACTURER, MODEL, DEVICE_IDENTIFIER,
    ADDON_SLUG, ingress_path,
)
from .coordinator import DomovraCoordinator

# (label, new_key, old_key, icon)
SENSORS = [
    ("Produits", "products", "products_count", "mdi:package-variant"),
    ("Stocks",   "lots",     "lots_count",     "mdi:archive"),
    ("Bientôt",  "soon",     "soon_count",     "mdi:timer-sand"),
    ("Urgents",  "urgent",   "urgent_count",   "mdi:alert-circle"),
]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    stored = hass.data[DOMAIN][entry.entry_id]
    coordinator: DomovraCoordinator = stored["coordinator"]
    base_url: str = stored["base_url"]

    entities = [
        DomovraCountSensor(coordinator, entry, base_url, label, new_key, old_key, icon)
        for (label, new_key, old_key, icon) in SENSORS
    ]
    async_add_entities(entities)

class DomovraCountSensor(CoordinatorEntity, SensorEntity):
    _attr_has_entity_name = True
    _attr_should_poll = False

    def __init__(self, coordinator: DomovraCoordinator, entry: ConfigEntry, base_url: str,
                 label: str, new_key: str, old_key: str, icon: str):
        super().__init__(coordinator)
        self._new_key = new_key
        self._old_key = old_key
        self._entry = entry
        self._base_url = base_url
        self._attr_name = f"Domovra {label}"
        self._attr_unique_id = f"{entry.entry_id}_{new_key}"  # unique par config entry
        self._attr_icon = icon

    @property
    def native_value(self):
        data = self.coordinator.data or {}
        if isinstance(data, dict):
            if self._new_key in data and data[self._new_key] is not None:
                return data[self._new_key]
            return data.get(self._old_key)
        return None

    @property
    def available(self) -> bool:
        return bool(getattr(self.coordinator, "last_update_success", True))

    @property
    def device_info(self) -> DeviceInfo:
        # Un seul "Appareil Domovra" pour toutes les entités + bouton Visiter → Ingress
        version = None
        data = self.coordinator.data
        if isinstance(data, dict):
            version = data.get("_version")
        return DeviceInfo(
            identifiers={DEVICE_IDENTIFIER},
            manufacturer=MANUFACTURER,
            model=MODEL,
            name="Domovra",
            sw_version=str(version) if version else None,
            configuration_url=ingress_path(ADDON_SLUG),
        )
