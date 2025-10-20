from django.urls import path
from .views import *

urlpatterns = [
    path('', chat_view, name='chat'),
    path('chat/<str:username>/', get_or_create_chatroom_view, name='start-chat'),
    path('chat/room/<chatroom_name>/', chat_view, name='chatroom'),
    
]