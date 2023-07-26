from django.apps import AppConfig


class DemositeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'demosite'

    def ready(self):
        import demosite.signals