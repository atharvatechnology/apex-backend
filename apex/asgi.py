"""ASGI config for apex project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""
# flake8: noqa

import os

from django.core.asgi import get_asgi_application

django_asgi_app = get_asgi_application()


from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

import clock.routing

# from django.core.asgi import get_asgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "apex.settings")

# django_asgi_app = get_asgi_application()


application = ProtocolTypeRouter(
    {
        # (http->django:)
        # "http": get_asgi_application(),
        # (websocket->django:)
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(clock.routing.websocket_urlpatterns))
        ),
    }
)
# get_asgi_application()
