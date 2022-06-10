"""ASGI config for apex project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

import clock.routing

# from django.core.asgi import get_asgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "apex.settings")

application = ProtocolTypeRouter(
    {
        # (http->django:)
        # "http": get_asgi_application(),
        # (websocket->django:)
        "websocket": AuthMiddlewareStack(
            URLRouter(clock.routing.websocket_urlpatterns)
        ),
    }
)
# get_asgi_application()
