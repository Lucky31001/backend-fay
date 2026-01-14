from django.apps import AppConfig


class Config(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "FAY"
    label = "FAY"

    def ready(self):
        try:
            from . import signals  # noqa: F401
        except Exception:
            pass
