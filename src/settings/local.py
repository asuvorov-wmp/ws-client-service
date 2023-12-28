# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
from .base import *


# -----------------------------------------------------------------------------
# --- Override Settings here.
# -----------------------------------------------------------------------------
DEBUG = True

DATABASES = {
    "default": {
        "ENGINE":   "django.db.backends.postgresql",
        "NAME":     os.environ.get("DB_NAME", "ws_demo"),
        "USER":     os.environ.get("DB_USER", "ws_demo"),
        "PASSWORD": os.environ.get("DB_PASSWORD", "ws_demo"),
        "HOST":     os.environ.get("DB_HOST", "db"),
        "PORT":     os.environ.get("DB_PORT", 5432),
    }
}

###############################################################################
### SERVICE SETTINGS                                                        ###
###############################################################################
GATEWAY_URL = os.environ.get("GATEWAY_URL", "https://gateway-dev.toogoerp.net")

###############################################################################
### ASGI / WEBSOCKET                                                        ###
###############################################################################
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("redis", 6379)],
            "symmetric_encryption_keys": [SECRET_KEY, ],
        },
    },
}
