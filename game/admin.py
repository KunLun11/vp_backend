from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin

from config.core.enums.games import GameStatus, ParticipantStatus
from game.models.games import Game, GameParticipant, GameReview

GAME_STATUS_COLORS = {
    GameStatus.draft: {"bg": "#6b7280", "text": "#ffffff"},  
    GameStatus.registration_open: {"bg": "#1051b9", "text": "#ffffff"}, 
    GameStatus.registration_closed: {"bg": "#10b981", "text": "#ffffff"},
    GameStatus.in_progress: {"bg": "#b910a8", "text": "#ffffff"},
    GameStatus.cancelled: {"bg": "#ef4444", "text": "#ffffff"},  
    GameStatus.completed: {"bg": "#3b82f6", "text": "#ffffff"},  
}

PARTICIPANT_STATUS_COLORS = {
    ParticipantStatus.registered: {"bg": "#f59e0b", "text": "#000000"}, 
    ParticipantStatus.confirmed: {"bg": "#1ea34d", "text": "#000000"}, 
    ParticipantStatus.no_show:  {"bg": "#ef4444", "text": "#ffffff"},
    ParticipantStatus.attended: {"bg": "#1051b9", "text": "#ffffff"},
}

def status_badge(obj, status_field, colors_dict):
    color = colors_dict.get(getattr(obj, status_field), {"bg": "#e5e7eb", "text": "#000000"})
    return format_html(
        '<span style="display:inline-block;padding:2px 8px;border-radius:9999px;'
        'font-size:12px;font-weight:600;background-color:{bg};color:{text};">{label}</span>',
        bg=color["bg"],
        text=color["text"],
        label=getattr(obj, f'get_{status_field}_display')(),
    )


@admin.register(Game)
class GameAdmin(ModelAdmin):
    list_display = ("id", "title", "organizer", "location", "date_time", "game_status_badge", "booked_count", "capacity")
    list_filter = ("status", "skill_level")
    search_fields = ("title", "organizer__first_name")
    readonly_fields = ("created_at", "updated_at")

    def game_status_badge(self, obj):
        return status_badge(obj, "status", GAME_STATUS_COLORS)
    game_status_badge.short_description = "Статус"


@admin.register(GameParticipant)
class GameParticipantAdmin(ModelAdmin):
    list_display = ("player", "game", "participant_status_badge", "registered_at")
    list_filter = ("status",)
    search_fields = ("player__first_name", "game__title")

    def participant_status_badge(self, obj):
        return status_badge(obj, "status", PARTICIPANT_STATUS_COLORS)
    participant_status_badge.short_description = "Статус"


@admin.register(GameReview)
class GameReviewAdmin(ModelAdmin):
    list_display = ("player", "game", "rating_game", "rating_organizer", "created_at")
    list_filter = ("rating_game", "rating_organizer")
    search_fields = ("player__first_name", "game__title")