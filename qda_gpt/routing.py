from django.urls import path
from channels.routing import URLRouter, ProtocolTypeRouter
from channels.auth import AuthMiddlewareStack
from qda_gpt.consumers import AnalysisConsumer

websocket_urlpatterns = [
    path('ws/analysis/', AnalysisConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
