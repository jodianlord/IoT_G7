from django.db import models
from django.utils import timezone

class Alert(models.Model):
    class Meta:
        db_table = "alerts"
    alerted_at = models.DateTimeField(default=timezone.now)