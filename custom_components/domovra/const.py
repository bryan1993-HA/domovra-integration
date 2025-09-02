# custom_components/domovra/const.py

DOMAIN = "domovra"
PLATFORMS = ["sensor"]

# Clés de conf / options
CONF_BASE_URL = "base_url"
DEFAULT_SCAN_SECS = 30

# Slug EXACT de l'add-on (champ "slug" du config.json de l'add-on)
ADDON_SLUG = "domovra"  # ← adapte si besoin

def ingress_path(slug: str | None = None) -> str:
    s = slug or ADDON_SLUG
    # Route front HA stable qui redirige vers l'Ingress
    return f"/hassio/ingress/{s}"

# Infos "Appareil" (device registry)
MANUFACTURER = "Domovra"
MODEL = "Home Assistant Add-on"
# Identifiant stable : toutes les entités seront regroupées sous un seul appareil
DEVICE_IDENTIFIER = (DOMAIN, "core")
