from django.apps import AppConfig


class MmorpgConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'MMORPG'

    def ready(self):
        import MMORPG.signals
