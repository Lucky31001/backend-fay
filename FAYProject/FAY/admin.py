from django.contrib import admin
from FAY.models.model_event import Event
from FAY.models.model_event_type import EventType
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
        "display_event_types",
        "note",
        "capacity",
        "creator",
    )
    search_fields = ("name", "location", "event_types__name", "creator__username")
    list_filter = ("event_types", "date", "creator")
    filter_horizontal = ("event_types",)

    @admin.display(description="Types")
    def display_event_types(self, obj):
        return ", ".join(obj.event_types.values_list("name", flat=True)) or "-"


@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
