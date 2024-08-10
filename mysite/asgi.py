import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter, ChannelNameRouter
from channels.auth import AuthMiddlewareStack
from qda_gpt.routing import websocket_urlpatterns
from qda_gpt.consumers import AnalysisConsumer  # Or the appropriate consumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Handles HTTP requests
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
    "channel": ChannelNameRouter({
        "analysis_channel": AnalysisConsumer.as_asgi(),  # Replace with the correct consumer for background tasks
    }),
})

