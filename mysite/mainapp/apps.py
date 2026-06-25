import sys
import threading

from django.apps import AppConfig
from django.conf import settings


class MainappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mainapp'

    def ready(self):
        if not getattr(settings, 'MQTT_CLIENT_STARTED', False):
            if len(sys.argv) > 1 and sys.argv[1] == 'runserver':
                settings.MQTT_CLIENT_STARTED = True
                from .mqtt import start_mqtt_client

                thread = threading.Thread(target=start_mqtt_client, daemon=True)
                thread.start()
