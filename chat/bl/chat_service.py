from django.db import transaction
from django.utils import timezone

from account.models.users import User
from chat.bl.exceptions import ChatMemberNotFound, ChatRoomNotFound, UserMuted
from chat.models import ChatMembership, ChatMessage, GameChatRoom
from game.models import Game, GameParticipant


class ChatService:
    @staticmethod
    def get_or_create_room(game: Game) -> GameChatRoom:
        room, _ = GameChatRoom.objects.get_or_create(game=game)
        return room

    @classmethod
    def create_room_for_game(cls, game: Game):
        room = cls.get_or_create_room(game)
        cls._add_member(room, game.organizer.user)

    @classmethod
    def add_participant_to_chat(cls, participant: GameParticipant):
        room = GameChatRoom.objects.filter(game=participant.game).first()
        if not room:
            raise ChatRoomNotFound()
        user = participant.player.user
        cls._add_member(room, user)

    @classmethod
    def remove_member(cls, room: GameChatRoom, user: User):
        ChatMembership.objects.filter(room=room, user=user).delete()

    @staticmethod
    def _add_member(room: GameChatRoom, user: User):
        ChatMembership.objects.get_or_create(room=room, user=user)

    @classmethod
    @transaction.atomic
    def toggle_mute(cls, room: GameChatRoom, target_user: User, muted_by: User):
        if room.game.organizer.user != muted_by:
            raise UserMuted(detail="Только организатор может управлять мутом")
        membership = ChatMembership.objects.filter(room=room, user=target_user).first()
        if not membership:
            raise ChatMemberNotFound()
        membership.is_muted = not membership.is_muted
        membership.save(update_fields=["is_muted"])
        return membership

    
    @classmethod
    def send_message(cls, room: GameChatRoom, sender: User, text: str) -> ChatMessage:
        membership = ChatMembership.objects.filter(room=room, user=sender).first()
        if not membership:
            raise ChatMemberNotFound()
        if membership.is_muted:
            raise UserMuted()
        msg = ChatMessage.objects.create(room=room, sender=sender, text=text)
        membership.last_read_at = timezone.now()
        membership.save(update_fields=["last_read_at"])
        return msg

    @classmethod
    def get_messages(cls, room: GameChatRoom):
        return ChatMessage.objects.filter(room=room).order_by("-created_at")

    @classmethod
    def mark_read(cls, room: GameChatRoom, user: User):
        membership = ChatMembership.objects.filter(room=room, user=user).first()
        if not membership:
            raise ChatMemberNotFound()
        membership.last_read_at = timezone.now()
        membership.save(update_fields=["last_read_at"])
