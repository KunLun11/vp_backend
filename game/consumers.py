from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.core.exceptions import PermissionDenied
from django.utils import timezone

from chat.models.chat import ChatMembership, ChatMessage, GameChatRoom
from game.models.games import Game


class GameChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.game_id = self.scope["url_route"]["kwargs"]["game_id"]
        self.room_group_name = f"chat_{self.game_id}"
        self.user = self.scope["user"]

        if not self.user.is_authenticated:
            await self.close(code=4003)
            return 
        
        try:
            membership = await self.get_membership()
            if not membership:
                raise PermissionDenied("Вы не участник этого чата")
            self.can_send = not membership.is_muted
            self.membership = membership
        except (Game.DoesNotExist, GameChatRoom.DoesNotExist, PermissionDenied):
            await self.close(code=4004)
            return
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )
        await self.accept()

        await self.send_chat_history()

        await self.mark_as_read()
    

    async def receive_json(self, content, **kwargs):
        msg_type = content.get("type")

        if msg_type == "message":
            text = content.get("message", "").strip()
            if not text:
                await self.send_error("Сообщение не может быть пустым")
                return
            if not self.can_send:
                await self.send_error("Вы не можете отправлять сообщения (muted)")
                return
            if not await self.is_room_active():
                await self.send_error("Чат архивирован, отправка невозможна")
                return

            message = await self.save_message(text)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": text,
                    "sender_id": str(message.sender.id),
                    "sender_email": message.sender.email,
                    "created_at": message.created_at.isoformat(),
                    "message_id": str(message.id),
                }
            )
        elif msg_type == "mark_read":
            await self.mark_as_read()


    async def chat_message(self, event):
        await self.send_json({
            "type": "message",
            "message": event["message"],
            "sender_id": event["sender_id"],
            "sender_email": event["sender_email"],
            "created_at": event["created_at"],
            "message_id": event["message_id"],
        })


    async def send_error(self, message: str):
        await self.send_json({
            "type": "error",
            "message": message
        })


    @database_sync_to_async
    def get_membership(self):
        try:
            return ChatMembership.objects.get(game_id=self.game_id)
        except Exception as e:
            return None
        

    @database_sync_to_async
    def is_room_active(self) -> bool:
        try:
            return ChatMembership.objects.select_related("room").get(
                user=self.user,
                room__game_id=self.game_id
            )
        except ChatMembership.DoesNotExist:
            return None
    

    @database_sync_to_async
    def save_message(self, text) -> ChatMessage:
        room = GameChatRoom.objects.get(game_id=self.game_id)
        return ChatMessage.objects.create(
            room=room,
            sender=self.user,
            text=text
        )
    

    @database_sync_to_async
    def mark_as_read(self) -> bool:
        ChatMembership.objects.filter(
            user=self.user,
            room__game_id=self.game_id
        ).update(last_read_at=timezone.now())


    @database_sync_to_async
    def get_last_message(self, limit=50):
        messages = ChatMessage.objects.filter(
            room__game_id=self.game_id
        ).select_related('sender').order_by('-created_at')[:limit]
        return list(messages)[::-1]


    async def send_chat_history(self):
        messages = await self.get_last_messages()
        for msg in messages:
            await self.send_json({
                "type": "history",
                "message": msg.text,
                "sender_id": str(msg.sender.id),
                "sender_email": msg.sender.email,
                "created_at": msg.created_at.isoformat(),
                "message_id": str(msg.id),
            })


    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name, 
            self.channel_name,
        )