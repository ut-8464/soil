import time

import paho.mqtt.client as mqtt
from django.conf import settings
from django.utils import timezone


def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print('MQTT 已連線，開始訂閱主題')
        client.subscribe(settings.MQTT_TOPICS)
    else:
        print('MQTT 連線失敗，rc=', rc)


def on_message(client, userdata, msg):
    payload = msg.payload.decode('utf-8', errors='ignore').strip()
    sensor_key = settings.MQTT_TOPIC_TO_SENSOR.get(msg.topic)
    if sensor_key is None:
        return

    try:
        value = float(payload)
    except ValueError:
        return

    from .models import SensorReading

    SensorReading.objects.create(
        topic=msg.topic,
        sensor_name=sensor_key,
        value=value,
        raw_payload=payload,
        created_at=timezone.now(),
    )


def start_mqtt_client():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    while True:
        try:
            client.connect(settings.MQTT_BROKER, settings.MQTT_PORT, keepalive=60)
            client.loop_forever()
        except Exception as exc:
            print('MQTT client 發生錯誤：', exc)
            time.sleep(10)
