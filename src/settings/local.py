"""
(C) 1995-2023 Epicor Software Corporation. All Rights Reserved.

The copyright owner has not given any authority for any publication
of this work.  This work contains valuable trade secrets of Epicor
and must be maintained in confidence.  Use of this work is governed
by the terms and conditions of a license agreement with Epicor.

"""

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
        "NAME":     os.environ.get("DB_NAME", "epa"),
        "USER":     os.environ.get("DB_USER", "epa"),
        "PASSWORD": os.environ.get("DB_PASSWORD", "epa"),
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
