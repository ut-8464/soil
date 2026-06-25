# mainapp/views.py
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone

from .models import SensorReading


def get_latest_readings():
    latest = {}
    for topic, sensor_key in settings.MQTT_TOPIC_TO_SENSOR.items():
        reading = SensorReading.objects.filter(topic=topic).order_by('-created_at').first()
        latest[sensor_key] = {
            'topic': topic,
            'label': settings.MQTT_SENSOR_LABELS.get(sensor_key, sensor_key),
            'value': reading.value if reading else None,
            'timestamp': reading.created_at.isoformat() if reading else None,
        }
    return latest


def home(request):
    return render(request, 'mainapp/index.html', {
        'current_time': timezone.localtime(),
        'latest': get_latest_readings(),
    })


def latest_data(request):
    return JsonResponse({
        'latest': get_latest_readings(),
        'current_time': timezone.localtime().isoformat(),
    })


def history_data(request):
    history = {}
    for topic, sensor_key in settings.MQTT_TOPIC_TO_SENSOR.items():
        readings = SensorReading.objects.filter(topic=topic).order_by('created_at')[:200]
        history[sensor_key] = [
            {
                'timestamp': reading.created_at.isoformat(),
                'value': reading.value,
            }
            for reading in readings
        ]
    return JsonResponse({'history': history})


def raw_data(request):
    limit = min(int(request.GET.get('limit', 100)), 500)
    readings = SensorReading.objects.order_by('-created_at')[:limit]
    rows = [
        {
            'timestamp': reading.created_at.isoformat(),
            'topic': reading.topic,
            'sensor_name': reading.sensor_name,
            'label': settings.MQTT_SENSOR_LABELS.get(reading.sensor_name, reading.sensor_name),
            'value': reading.value,
            'raw_payload': reading.raw_payload,
        }
        for reading in readings
    ]
    return JsonResponse({'rows': rows})