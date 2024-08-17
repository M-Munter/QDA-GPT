# routing.py
#
# This script configures WebSocket routing for the Django Channels application.

from django.urls import path
from channels.routing import URLRouter, ProtocolTypeRouter
from channels.auth import AuthMiddlewareStack
from qda_gpt.consumers import AnalysisConsumer

# Define the URL patterns for WebSocket connections
websocket_urlpatterns = [
    path('ws/analysis/', AnalysisConsumer.as_asgi()),
]

# Set up the main application routing for different protocol types
application = ProtocolTypeRouter({
    # Route WebSocket connections through the authentication middleware stack
    "websocket": AuthMiddlewareStack(
        # Route the WebSocket connections based on the defined URL patterns
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
