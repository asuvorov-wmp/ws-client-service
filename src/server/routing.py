from django.core.asgi import get_asgi_application
from django.urls import re_path

from channels.auth import AuthMiddlewareStack
from channels.routing import (
    ProtocolTypeRouter,
    URLRouter)


from .consumers import MasterConsumer


application = ProtocolTypeRouter(
    {
        "http":         get_asgi_application(),
        "websocket":    AuthMiddlewareStack(
            URLRouter(
                [
                    re_path(r"^ws/$", MasterConsumer.as_asgi()),
                ]
            )
        ),
    }
)
