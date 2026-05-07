from django.contrib import admin
from unfold.admin import ModelAdmin

from etc.models.location import Location


@admin.register(Location)
class GameAdmin(ModelAdmin):
    list_display = ("name", "address", "venue_type", "surface_type")
    list_filter = ("venue_type", "surface_type")
    search_fields = ()
    readonly_fields = ("created_at", "updated_at")

