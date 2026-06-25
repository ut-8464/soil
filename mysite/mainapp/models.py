from django.db import models
from django.utils import timezone


class SensorReading(models.Model):
    topic = models.CharField(max_length=200)
    sensor_name = models.CharField(max_length=100)
    value = models.FloatField()
    raw_payload = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.sensor_name} ({self.topic}) = {self.value} @ {self.created_at}"