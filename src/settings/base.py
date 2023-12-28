"""
(C) 1995-2023 Epicor Software Corporation. All Rights Reserved.

The copyright owner has not given any authority for any publication
of this work.  This work contains valuable trade secrets of Epicor
and must be maintained in confidence.  Use of this work is governed
by the terms and conditions of a license agreement with Epicor.

"""

import os
import os.path

from django.utils.translation import gettext_lazy as _

from decouple import config


###############################################################################
### How does it work?
### Decouple always searches for Options in this Order:
### - Environment Variables;
### - Repository: `settings.ini` or `.env` File;
### - Default Argument, passed to Config.
###############################################################################

###############################################################################
### BASIC SETTINGS                                                          ###
###############################################################################
PRODUCT_VERSION = "0.0.0"

DEBUG = config("DEBUG", default=False)
DEBUG_TOOLBAR = True

# PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..",))

# We have 6 Types of Environments: "local", "dev", "test", "int", "staging", and "prod".
ENVIRONMENT = config("ENVIRONMENT", "dev")

DJANGO_SETTINGS_MODULE = config("DJANGO_SETTINGS_MODULE", "settings.dev")

ADMINS = (
    ("Artem Suvorov", "artem.suvorov@epicor.com"),
)
MANAGERS = ADMINS

DATABASES = {
    "default": {
        "ENGINE":   "django.db.backends.sqlite3",
        "NAME":     "sqlite.db",
        "USER":     "",
        "PASSWORD": "",
        "HOST":     "",
        "PORT":     "",
    },
    "TEST": {
        "ENGINE":   "django.db.backends.sqlite3",
        "NAME":     "test.sqlite.db",
        "USER":     "",
        "PASSWORD": "",
        "HOST":     "",
        "PORT":     "",
    }
}

DOMAIN_NAME = "example.com"
ALLOWED_HOSTS = ["*"]
APPEND_SLASH = True

TIME_ZONE = "America/Los_Angeles"

LANGUAGE_CODE = "en-us"
LANGUAGES = (
    ("en",  _("English")),
    ("de",  _("Deutsch")),
    ("es",  _("Spanish")),
)

LOCALE_PATHS = (
    os.path.join(PROJECT_PATH, "locale"),
)

SITE_ID = 1

USE_I18N = True
USE_L10N = True
USE_TZ = True

ADMIN_MEDIA_PREFIX = "/static/admin/"

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(PROJECT_PATH, "media")

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(PROJECT_PATH, "staticserve")
STATICFILES_DIRS = (
    ("", f"{PROJECT_PATH}/static"),
)
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "django.contrib.staticfiles.finders.DefaultStorageFinder",
)

SECRET_KEY = config("SECRET_KEY", default="@zew8t_wcz!qn9=8+hheltx@&b#!x@i6ores96lhbnobr3jp*c")
SECURE_SSL_REDIRECT = config("SECURE_SSL_REDIRECT", default=False, cast=bool)

TEMPLATES = [
    {
        "BACKEND":  "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(PROJECT_PATH, "templates/"),
            os.path.join(PROJECT_PATH, "templates/emails/"),
            os.path.join(PROJECT_PATH, "templates/cyborg/"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "debug":    DEBUG,
            # "loaders": [
            #     "django.template.loaders.filesystem.Loader",
            #     "django.template.loaders.app_directories.Loader",
            # ],
            "context_processors": [
                "django.template.context_processors.csrf",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.request",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'


###############################################################################
### DJANGO MIDDLEWARE CLASSES                                               ###
###############################################################################
MIDDLEWARE = (
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    # "django.contrib.auth.middleware.SessionAuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
)

ROOT_URLCONF = "urls"

WSGI_APPLICATION = "wsgi.application"

INSTALLED_APPS = (
    # --- Django Apps.
    # "grappelli",

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.sitemaps",
    "django.contrib.sites",
    "django.contrib.staticfiles",

    # --- 3rd Party Apps.
    # "rangefilter",

    # --- Project Apps.
    "adrf",
    "api",
    "app",
    "archive",
    "core",
    "integrations",
    "lib",
    "rest_framework_proxy",
    "sales",
    "service",
    "tests",
)

SESSION_SERIALIZER = "django.contrib.sessions.serializers.JSONSerializer"


###############################################################################
### DJANGO CACHING                                                          ###
###############################################################################
CACHES = {
    "default": {
        "BACKEND":  "django.core.cache.backends.dummy.DummyCache",
    }
}

REDIS_FILE = "/etc/uwsgi/redis_params"


###############################################################################
### DJANGO LOGGING                                                          ###
###############################################################################
LOGGING = {
    "version":                      1,
    "disable_existing_loggers":     False,
    "filters": {
        "require_debug_false": {
            "()":                   "django.utils.log.RequireDebugFalse",
        },
        "require_debug_true": {
            "()":                   "django.utils.log.RequireDebugTrue",
        },
    },
    "formatters": {
        "simple": {
            "format":               "[%(asctime)s] %(levelname)s %(message)s",
            "datefmt":              "%Y-%m-%d %H:%M:%S",
        },
        "verbose": {
            "format":               "[%(asctime)s] %(levelname)s "
                                    "[%(name)s.%(funcName)s:%(lineno)d] "
                                    "%(message)s",
            "datefmt":              "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "level":                "INFO",
            "filters": [
                "require_debug_true",
            ],
            "class":                "logging.StreamHandler",
            "formatter":            "simple",
        },
        "null": {
            "class":                "logging.NullHandler",
        },
        "mail_admins": {
            "level":                "ERROR",
            "filters": [
                "require_debug_false",
            ],
            "class":                "django.utils.log.AdminEmailHandler",
            "formatter":            "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": [
                "console",
            ],
        },
        "django.request": {
            "handlers": [
                "mail_admins",
            ],
            "level":                "ERROR",
            "propagate":            False,
        },
        "py.warnings": {
            "handlers": [
                "console",
            ],
        },
        # "": {
        #     "handlers": [
        #         "console", "stdout",
        #     ],
        # },
    },
}

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
)
# AUTH_USER_MODEL = "accounts.User"


###############################################################################
### SERVICE SETTINGS                                                        ###
###############################################################################
MANAGEMENT_SECRET_KEY = "176261cf87655d488357aeb666038b4a5a02f95b"
OUR_APPLICATION_NAME = "ERC"
TOOGO_VERSION = config("TOOGO_VERSION", "125.139.1399.8234")

OFFLINE_MODE = config("OFFLINE_MODE", "false").lower() == "true"
OFFLINE_SYSTEM_IDENTIFIER = config("OFFLINE_SYSTEM_IDENTIFIER", "")
CLOUDFRONT_DOMAIN = config("CLOUDFRONT_DOMAIN", None)

EPA_CLOUD_INSTANCE = config("EPA_CLOUD_INSTANCE", "wss://epa-ws.toogoerp.net")
EPA_MPOS_INSTANCE = config("EPA_MPOS_INSTANCE", "https://mpos-dev.eaglesoa.com")
EPA_HUB_INSTANCE = config("EPA_HUB_INSTANCE", "https://epa-hub.toogoerp.net")

GATEWAY_URL = config("GATEWAY_URL", "https://gateway.toogoerp.net")
GATEWAY_TOKEN = config("GATEWAY_TOKEN", MANAGEMENT_SECRET_KEY)

###############################################################################
### DJANGO GRAPPELLI                                                        ###
###############################################################################
GRAPPELLI_ADMIN_TITLE = "State Machine Admin"
GRAPPELLI_AUTOCOMPLETE_LIMIT = 25
# GRAPPELLI_AUTOCOMPLETE_SEARCH_FIELDS
GRAPPELLI_SWITCH_USER = True
# GRAPPELLI_SWITCH_USER_ORIGINAL
# GRAPPELLI_SWITCH_USER_TARGET
# GRAPPELLI_CLEAN_INPUT_TYPES = False


###############################################################################
### DJANGO REST FRAMEWORK                                                   ###
###############################################################################
INSTALLED_APPS += (
    "rest_framework",
    "rest_framework.authtoken",
)
REST_FRAMEWORK = {
    "DEFAULT_MODEL_SERIALIZER_CLASS":   "rest_framework.serializers.HyperlinkedModelSerializer",
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.BrowsableAPIRenderer",
        "rest_framework.renderers.JSONRenderer",
        "rest_framework_jsonp.renderers.JSONPRenderer",
    ),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),

    "TEST_REQUEST_DEFAULT_FORMAT":  "json",
    "TEST_REQUEST_RENDERER_CLASSES": (
        "rest_framework.renderers.MultiPartRenderer",
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.TemplateHTMLRenderer"
    ),
}
TOKEN_AUTHENTICATION_TYPE = "jwt"


###############################################################################
### AWS SNS                                                                 ###
###############################################################################
PRODUCTION_MODE = False

SNS_ENABLED = config("SNS_ENABLED", True)

AWS_STORAGE_BUCKET_NAME = config("AWS_STORAGE_BUCKET_NAME", "toogo-production-dev")
AWS_STORAGE_BUCKET_NAME_MIRROR = AWS_STORAGE_BUCKET_NAME + "-backups"


###############################################################################
### ASGI / WEBSOCKET                                                        ###
###############################################################################
ASGI_APPLICATION = "service.routing.application"

USE_REDIS_PUBSUB = config("USE_REDIS_PUBSUB", default=True, cast=bool)

REDIS_DEFAULT_CACHE_TTL = config("REDIS_DEFAULT_CACHE_TTL", default=60, cast=int)
REDIS_TRANSACTION_CACHE_TTL = config("REDIS_TRANSACTION_CACHE_TTL", default=86400, cast=int)
REDIS_TENDER_CACHE_TTL = config("REDIS_TENDER_CACHE_TTL", default=86400, cast=int)
REDIS_SOCKET_TTL = config("REDIS_SOCKET_TTL", default=2, cast=int)
REDIS_SOCKET_CONNECT_TTL = config("REDIS_SOCKET_CONNECT_TTL", default=2, cast=int)

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("localhost", 6379)],
            "symmetric_encryption_keys": [SECRET_KEY, ],
        },
    },
}

WEBSOCKET_STREAM_HANDLERS = {
    "channel":      "service.handlers.ChannelStreamHandler",
    "ping":         "lib.handlers.PingStreamHandler",
    # "pos_tender":   "sales.channels.POSTenderStreamHandler",
    # "hub_request":  "organization.channels.HubStreamHandler",
}

MESSAGING_STREAM_HANDLERS = {
    "channel_control":  "service.messaging.ControlStreamHandler",
    "normal":           "service.messaging.FakeStreamHandler",
    "test_harness":     "service.messaging.TestHarnessHandler",
}
