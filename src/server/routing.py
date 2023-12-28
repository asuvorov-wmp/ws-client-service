"""
(C) 1995-2023 Epicor Software Corporation. All Rights Reserved.

The copyright owner has not given any authority for any publication
of this work.  This work contains valuable trade secrets of Epicor
and must be maintained in confidence.  Use of this work is governed
by the terms and conditions of a license agreement with Epicor.

"""

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
