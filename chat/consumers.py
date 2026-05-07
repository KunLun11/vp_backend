import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from chat.bl.chat_service import ChatService
from chat.bl.exceptions import ChatRoomNotFound, UserMuted
from chat.models import GameChatRoom


class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.room_group_name = f"chat_{self.room_id}"
        user = self.scope.get("user")

        if not user or not user.is_authenticated:
            await self.close()
            return

        is_member = await self.is_member(user)
        if not is_member:
            await self.close()
            return

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, "room_group_name"):
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        if text_data is None:
            return
        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            return

        action = data.get("action")
        if action == "message":
            await self.handle_message(data)
        elif action == "typing":
            pass

    async def handle_message(self, data):
        text = data.get("text", "").strip()
        if not text:
            return

        user = self.scope.get("user")
        try:
            room = await self.get_room()
            message = await self.create_message(room, user, text)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat.message",
                    "id": str(message.id),
                    "text": message.text,
                    "sender": {
                        "id": str(user.pk),
                        "email": user.email,
                        "role": user.role,
                    },
                    "created_at": message.created_at.isoformat(),
                },
            )
        except (ChatRoomNotFound, UserMuted) as e:
            await self.send_json({"error": str(e)})

    async def chat_message(self, event):
        await self.send_json(event)

    @database_sync_to_async
    def get_room(self):
        return GameChatRoom.objects.get(pk=self.room_id)

    @database_sync_to_async
    def create_message(self, room, user, text):
        return ChatService.send_message(room, user, text)

    @database_sync_to_async
    def is_member(self, user):
        from chat.models import ChatMembership

        return ChatMembership.objects.filter(
            room_id=self.room_id,
            user=user,
        ).exists()
