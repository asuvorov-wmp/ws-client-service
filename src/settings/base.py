import os
import os.path

from django.utils.translation import gettext_lazy as _


###############################################################################
### BASIC SETTINGS                                                          ###
###############################################################################
PRODUCT_VERSION = "0.0.0"

DEBUG = bool(os.environ.get("DEBUG", False))
DEBUG_TOOLBAR = True

# PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..",))

# We have 6 Types of Environments: "local", "dev", "test", "int", "staging", and "prod".
ENVIRONMENT = os.environ.get("ENVIRONMENT", "dev")

DJANGO_SETTINGS_MODULE = os.environ.get("DJANGO_SETTINGS_MODULE", "settings.dev")

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

SECRET_KEY = os.environ.get("SECRET_KEY", default="@zew8t_wcz!qn9=8+hheltx@&b#!x@i6ores96lhbnobr3jp*c")
SECURE_SSL_REDIRECT = bool(os.environ.get("SECURE_SSL_REDIRECT", False))

TEMPLATES = [
    {
        "BACKEND":  "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(PROJECT_PATH, "templates/"),
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
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.sitemaps",
    "django.contrib.sites",
    "django.contrib.staticfiles",

    # --- 3rd Party Apps.

    # --- Project Apps.
    "app",
    "client",
    "server",
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


###############################################################################
### SERVICE SETTINGS                                                        ###
###############################################################################
CLOUD_SERVICE_INSTANCE = os.environ.get("CLOUD_SERVICE_INSTANCE", "wss://ws.postman-echo.com/raw")


###############################################################################
### ASGI / WEBSOCKET                                                        ###
###############################################################################
ASGI_APPLICATION = "server.routing.application"

USE_REDIS_PUBSUB = bool(os.environ.get("USE_REDIS_PUBSUB", True))

REDIS_DEFAULT_CACHE_TTL = int(os.environ.get("REDIS_DEFAULT_CACHE_TTL", 60))
REDIS_TRANSACTION_CACHE_TTL = int(os.environ.get("REDIS_TRANSACTION_CACHE_TTL", 86400))
REDIS_TENDER_CACHE_TTL = int(os.environ.get("REDIS_TENDER_CACHE_TTL", 86400))
REDIS_SOCKET_TTL = int(os.environ.get("REDIS_SOCKET_TTL", 2))
REDIS_SOCKET_CONNECT_TTL = int(os.environ.get("REDIS_SOCKET_CONNECT_TTL", 2))

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("localhost", 6379)],
            "symmetric_encryption_keys": [SECRET_KEY, ],
        },
    },
}


VALID_STREAM_NAMES = {
    "CHANNEL":  "channel",
    "PING":     "ping",
}

WEBSOCKET_STREAM_HANDLERS = {
    VALID_STREAM_NAMES["CHANNEL"]:  "server.handlers.ChannelStreamHandler",
    VALID_STREAM_NAMES["PING"]:     "server.handlers.PingStreamHandler",
}
