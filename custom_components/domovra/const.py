# custom_components/domovra/const.py
DOMAIN = "domovra"
PLATFORMS = ["sensor"]

# Conf / options
CONF_BASE_URL = "base_url"
DEFAULT_SCAN_SECS = 30

# Slug EXACT de l'add-on (champ "slug" dans le config.json de l'add-on)
ADDON_SLUG = "domovra_beta"  # ← adapte si besoin

def ingress_path(slug: str | None = None) -> str:
    s = slug or ADDON_SLUG
    return f"/hassio/ingress/{s}"

# Device registry
MANUFACTURER = "Domovra"
MODEL = "Home Assistant Add-on"
DEVICE_IDENTIFIER = (DOMAIN, "core")

