from rest_framework import serializers

from account.models.users import User
from chat.models import ChatMembership, ChatMessage, GameChatRoom


class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["uuid", "email", "role"]


class ChatMemberSerializer(serializers.ModelSerializer):
    user = UserShortSerializer(read_only=True)

    class Meta:
        model = ChatMembership
        fields = ["id", "user", "joined_at", "is_muted"]


class ChatRoomSerializer(serializers.ModelSerializer):
    members = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = GameChatRoom
        fields = ["uuid", "game", "is_active", "archived_at", "members", "last_message"]

    def get_members(self, obj):
        memberships = ChatMembership.objects.filter(room=obj).select_related("user")
        return ChatMemberSerializer(memberships, many=True).data

    def get_last_message(self, obj):
        last_msg = ChatMessage.objects.filter(room=obj).order_by("-created_at").first()
        return last_msg.text if last_msg else None


class MessageSerializer(serializers.ModelSerializer):
    sender = UserShortSerializer(read_only=True)

    class Meta:
        model = ChatMessage
        fields = ["id", "text", "sender", "created_at"]


class SendMessageSerializer(serializers.Serializer):
    text = serializers.CharField()


class MarkReadSerializer(serializers.Serializer):
    pass
