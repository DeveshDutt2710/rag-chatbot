from django.urls import path
from .views import chat_page, ChatAPIView

urlpatterns = [
    path('', chat_page, name='chat-ui'),
    path('chat/', ChatAPIView.as_view(), name='chat-api'),
]
