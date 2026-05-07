from django.urls import path

from .views import ChatViewSet

chat_room_detail = ChatViewSet.as_view(
    {
        "get": "retrieve",
    }
)

chat_messages_list = ChatViewSet.as_view(
    {
        "get": "messages",
    }
)

chat_send = ChatViewSet.as_view(
    {
        "post": "send",
    }
)

chat_mark_read = ChatViewSet.as_view(
    {
        "post": "mark_read",
    }
)

chat_toggle_mute = ChatViewSet.as_view(
    {
        "post": "toggle_mute",
    }
)

urlpatterns = [
    path(
        "games/<int:game_id>/chat/",
        chat_room_detail,
        name="game-chat-detail",
    ),
    path(
        "games/<int:game_id>/chat/messages/",
        chat_messages_list,
        name="game-chat-messages",
    ),
    path(
        "games/<int:game_id>/chat/send/",
        chat_send,
        name="game-chat-send",
    ),
    path(
        "games/<int:game_id>/chat/read/",
        chat_mark_read,
        name="game-chat-mark-read",
    ),
    path(
        "games/<int:game_id>/chat/mute/",
        chat_toggle_mute,
        name="game-chat-toggle-mute",
    ),
]
