from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin

from account.models.profiles import CoachProfile, OrganizerProfile, PlayerProfile
from account.models.users import User


@admin.register(User)
class UserAdmin(ModelAdmin):
    list_display = ["email", "role", "is_verified", "is_active", "created_at"]
    list_filter = ["role", "is_verified", "is_active"]
    search_fields = ["email", "phone"]
    readonly_fields = ["created_at", "updated_at", "last_login_at"]


@admin.register(PlayerProfile)
class PlayerProfileAdmin(ModelAdmin):
    list_display = ["user", "city", "skill_level", "elo_rating", "total_games", "photo_preview"]
    list_filter = ["city", "skill_level", "gender"]
    search_fields = ["first_name", "user__email"]

    def photo_preview(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 50px; border-radius: 4px;" />', obj.photo.url
            )
        return "—"

    photo_preview.short_description = "Фото"


@admin.register(CoachProfile)
class CoachProfileAdmin(ModelAdmin):
    list_display = ["user", "city", "experience_years", "hourly_rate"]
    list_filter = ["city"]
    search_fields = ["first_name", "user__email"]


@admin.register(OrganizerProfile)
class OrganizerProfileAdmin(ModelAdmin):
    list_display = ["user", "city", "total_games"]
    list_filter = ["city"]
    search_fields = ["first_name", "user__email"]
