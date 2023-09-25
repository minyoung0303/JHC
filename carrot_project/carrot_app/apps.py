from django.apps import AppConfig


class DangunAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "carrot_app"

    def ready(self):
        import carrot_app.signals
