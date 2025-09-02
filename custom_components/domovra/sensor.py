from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, MANUFACTURER, MODEL, DEVICE_IDENTIFIER
from .coordinator import DomovraCoordinator

# Aligne les clés sur l'endpoint /api/ha/summary
SENSORS = [
    ("Produits", "products", "mdi:package-variant"),
    ("Stocks",   "lots",     "mdi:archive"),
    ("Bientôt",  "soon",     "mdi:timer-sand"),
    ("Urgents",  "urgent",   "mdi:alert-circle"),
]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, add_entities: AddEntitiesCallback):
    d = hass.data[DOMAIN][entry.entry_id]
    coord: DomovraCoordinator = d["coordinator"]
    base_url: str = d["base_url"]
    entities = [DomovraCountSensor(coord, entry, base_url, name, key, icon) for name, key, icon in SENSORS]
    add_entities(entities)

class DomovraCountSensor(CoordinatorEntity, SensorEntity):
    _attr_has_entity_name = True
    _attr_should_poll = False
    _attr_native_unit_of_measurement = None

    def __init__(self, coordinator: DomovraCoordinator, entry: ConfigEntry, base_url: str,
                 name: str, key: str, icon: str):
        super().__init__(coordinator)
        self._key = key
        self._entry = entry
        self._base_url = base_url

        # Nom & UID
        self._attr_name = f"Domovra {name}"
        # Unique par entrée + métrique
        self._attr_unique_id = f"{entry.entry_id}_{key}"
        self._attr_icon = icon

    @property
    def native_value(self):
        data = self.coordinator.data or {}
        return data.get(self._key)

    @property
    def available(self) -> bool:
        return bool(self.coordinator.last_update_success)

    @property
    def device_info(self) -> DeviceInfo:
        """
        Regroupe toutes les entités sous UN 'Appareil Domovra' avec :
        - nom, constructeur, modèle
        - version (si tu veux, ajoute-la dans coordinator.data["_version"])
        - configuration_url (ouvre l'UI de l'add-on/Ingress si base_url pointe dessus)
        """
        version = None
        if isinstance(self.coordinator.data, dict):
            version = self.coordinator.data.get("_version")

        return DeviceInfo(
            identifiers={DEVICE_IDENTIFIER},
            manufacturer=MANUFACTURER,
            model=MODEL,
            name="Domovra",
            sw_version=str(version) if version else None,
            configuration_url=self._base_url or None,
        )
