DOMAIN = "domovra"
PLATFORMS = ["sensor"]

# Options / conf
CONF_BASE_URL = "base_url"
DEFAULT_SCAN_SECS = 30

# Device registry
MANUFACTURER = "Domovra"
MODEL = "Home Assistant Add-on"

# Identifiant stable pour regrouper toutes les entités sous UN appareil
# (si tu prévois plusieurs instances, utilise plutôt (DOMAIN, entry.entry_id))
DEVICE_IDENTIFIER = (DOMAIN, "core")
