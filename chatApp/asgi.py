import os

# Set DJANGO_SETTINGS_MODULE before any Django imports
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatApp.settings')

# Only now import Django modules
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

# Import routing after setting the environment
import chat.routing

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # initializes Django
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})