"""
ASGI config for CIO_MACHINE_SERVER project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from channels.routing import ProtocolTypeRouter,URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from django.urls import path
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CIO_MACHINE_SERVER.settings')

django_asgi_app = get_asgi_application()
from users.routing import ws_urls

application = ProtocolTypeRouter({
    # WebSocket chat handler
    "http":django_asgi_app,
    "websocket": AuthMiddlewareStack(URLRouter(ws_urls))
})


