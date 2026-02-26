from django.apps import AppConfig


class AutocareappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Autocareapp'

    def ready(self):
         import Autocareapp.signals