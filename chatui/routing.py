from django.urls import re_path
from chatui import consumers

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<session_id>[^/]+)/$", consumers.ChatConsumer.as_asgi()),
]