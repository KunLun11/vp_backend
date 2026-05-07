from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from account.bl.auth import JWTAuthentication
from account.models.users import User
from chat.api_v1.serializers import (
    ChatRoomSerializer,
    MessageSerializer,
    SendMessageSerializer,
)
from chat.bl.chat_service import ChatService
from chat.bl.exceptions import ChatRoomNotFound, UserMuted
from chat.models import GameChatRoom


@extend_schema_view(
    retrieve=extend_schema(
        summary="Получить чат-комнату",
        description="Возвращает информацию о комнате, участниках и последнем сообщении.",
        tags=["chat"],
    ),
    messages=extend_schema(
        summary="Список сообщений",
        description="Возвращает сообщения комнаты с пагинацией.",
        tags=["chat"],
    ),
    send=extend_schema(
        summary="Отправить сообщение",
        description="Отправляет новое сообщение в чат. Доступно только участникам (не замученным).",
        tags=["chat"],
    ),
    mark_read=extend_schema(
        summary="Прочитать сообщения",
        description="Обновляет время последнего прочтения для текущего участника.",
        tags=["chat"],
    ),
    toggle_mute=extend_schema(
        summary="Замутить/размутить участника",
        description="Только организатор игры может переключить mute участнику.",
        tags=["chat"],
    ),
)
class ChatViewSet(viewsets.GenericViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = GameChatRoom.objects.select_related("game").all()
    serializer_class = ChatRoomSerializer


    def get_room(self):
        game_id = self.kwargs["game_id"]
        try:
            return GameChatRoom.objects.get(game_id=game_id)
        except GameChatRoom.DoesNotExist:
            raise ChatRoomNotFound()


    def retrieve(self, request, *args, **kwargs):
        room = self.get_room()
        serializer = self.get_serializer(room)
        return Response(serializer.data)

    # GET /games/{game_id}/chat/messages/
    @action(detail=False, methods=["get"], url_path="messages")
    def messages(self, request, game_id=None):
        room = self.get_room()
        qs = ChatService.get_messages(room)
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = MessageSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = MessageSerializer(qs, many=True)
        return Response(serializer.data)

    # POST /games/{game_id}/chat/send/
    @action(detail=False, methods=["post"], url_path="send")
    def send(self, request, game_id=None):
        serializer = SendMessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        room = self.get_room()
        try:
            msg = ChatService.send_message(room, request.user, serializer.validated_data["text"])
        except UserMuted as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)
        return Response(MessageSerializer(msg).data, status=status.HTTP_201_CREATED)

    # POST /games/{game_id}/chat/read/
    @action(detail=False, methods=["post"], url_path="read")
    def mark_read(self, request, game_id=None):
        room = self.get_room()
        ChatService.mark_read(room, request.user)
        return Response({"detail": "Сообщения прочитаны"})

    # POST /games/{game_id}/chat/mute/
    @action(detail=False, methods=["post"], url_path="mute")
    def toggle_mute(self, request, game_id=None):
        target_user_id = request.data.get("user_id")
        if not target_user_id:
            return Response({"detail": "user_id обязателен"}, status=status.HTTP_400_BAD_REQUEST)
        room = self.get_room()
        try:
            target = User.objects.get(pk=target_user_id)
        except User.DoesNotExist:
            return Response({"detail": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND)
        try:
            membership = ChatService.toggle_mute(room, target, request.user)
        except UserMuted as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)
        return Response({"is_muted": membership.is_muted})
