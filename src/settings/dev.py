# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
from .base import *


# -----------------------------------------------------------------------------
# --- Override Settings here.
# -----------------------------------------------------------------------------
DEBUG = True

###############################################################################
### SERVICE SETTINGS                                                        ###
###############################################################################
GATEWAY_URL = os.environ.get("GATEWAY_URL", "https://gateway-dev.toogoerp.net")
