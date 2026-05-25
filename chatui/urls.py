from django.urls import path
from chatui import views

urlpatterns = [
    path("", views.chat_view, name="chat"),
    path("clear/", views.clear_chat, name="clear_chat"),
]