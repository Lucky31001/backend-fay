from django.contrib import admin
from FAY.models.model_event import Event
from FAY.models.model_profile import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role")
    search_fields = ("user__username",)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "date",
        "location",
        "price",
        "event_type",
        "note",
        "capacity",
        "creator",
    )
    search_fields = ("name", "location", "event_type", "creator__username")
    list_filter = ("event_type", "date", "creator")
