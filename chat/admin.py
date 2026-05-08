from django.contrib import admin
from unfold.admin import ModelAdmin

from chat.models.chat import ChatMembership, ChatMessage, GameChatRoom


@admin.register(GameChatRoom)
class GameChatRoomAdmin(ModelAdmin):
    list_display = (
        "uuid",
        "game",
        "is_active",
        "archived_at",
    )
    list_filter = ("uuid",)
    search_fields = ("game",)
    readonly_fields = ("created_at", "updated_at")


@admin.register(ChatMembership)
class ChatMembershipAdmin(ModelAdmin):
    list_display = (
        "id",
        "user",
        "room",
        "joined_at",
        "last_read_at",
        "is_muted",
    )
    list_filter = ("id", "user", "room")
    search_fields = ("user",)
    readonly_fields = ("created_at", "updated_at")


@admin.register(ChatMessage)
class ChatMessageAdmin(ModelAdmin):
    list_display = (
        "uuid",
        "sender",
        "room",
    )
    list_filter = ("uuid", "sender", "room")
    search_fields = ("sender",)
    readonly_fields = ("created_at", "updated_at")
