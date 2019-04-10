from django.db import models
from django.utils import timezone

class Alert(models.Model):
    class Meta:
        db_table = "alerts"
    alerted_at = models.DateTimeField(default=timezone.now)

class Wastage(models.Model):
    class Meta:
        db_table = "wastage"
    time_wasted = models.DateTimeField(default=timezone.now)
    aircon_wasted_hours = models.FloatField(default=0.0)
    light_wasted_hours = models.FloatField(default=0.0)