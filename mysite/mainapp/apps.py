import sys
import threading

from django.apps import AppConfig
from django.conf import settings


class MainappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mainapp'

    def ready(self):
        if len(sys.argv) > 1 and sys.argv[1] == 'runserver' and not getattr(settings, 'MQTT_CLIENT_STARTED', False):
            settings.MQTT_CLIENT_STARTED = True
            try:
                from .mqtt import start_mqtt_client
            except ImportError:
                return

            thread = threading.Thread(target=start_mqtt_client, daemon=True)
            thread.start()