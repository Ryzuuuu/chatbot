import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import chatui.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web_app.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(chatui.routing.websocket_urlpatterns)
    ),
})