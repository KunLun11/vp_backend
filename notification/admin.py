from django.contrib import admin
from unfold.admin import ModelAdmin

from notification.models.notifications import Notification


@admin.register(Notification)
class NotificationAdmin(ModelAdmin):
    list_display = ("title", "user", "type", "category", "is_read", "created_at")
    list_filter = ("type", "category", "is_read")
    search_fields = ("title", "user__email")
