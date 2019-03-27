from django.db import models
from django.utils import timezone

class Facility(models.Model):
    name = models.CharField(max_length=100)
    class Meta:
        db_table = "facility"

# Superclass for a sensor
class Sensor(models.Model):
    class Meta:
        db_table = "sensors"
    # Time fields
    created_at = models.DateTimeField(default=timezone.now)
    reading_type = models.CharField(max_length=5)
    value = models.FloatField(default=0.0)
    facility = models.ForeignKey(Facility, null=True, on_delete=models.SET_NULL)

