"""
ASGI configuration script for the 'mysite' project.

This script, `asgi.py`, defines the ASGI application for handling different types
of connections, including HTTP requests, WebSocket connections, and background tasks
via channels. It sets up routing for these different protocols using Django Channels.
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter, ChannelNameRouter
from channels.auth import AuthMiddlewareStack
from qda_gpt.routing import websocket_urlpatterns
from qda_gpt.consumers import AnalysisConsumer

# Set the default settings module for Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

# Define the ASGI application
application = ProtocolTypeRouter({
    # Route HTTP requests to Django's ASGI application handler
    "http": get_asgi_application(),  # Handles HTTP requests
    # Route WebSocket connections through the authentication middleware stack and URL router
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
    # Handles background tasks on 'analysis_channel'
    "channel": ChannelNameRouter({
        "analysis_channel": AnalysisConsumer.as_asgi(),  # Replace with the correct consumer for background tasks
    }),
})


