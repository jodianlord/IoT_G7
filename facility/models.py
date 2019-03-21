from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if self.id:
            self.updated_at = timezone.now()
        return super(BaseModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class Facility(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "iot_facility"


class FacilityReadingQuerySet(models.QuerySet):

    def id(self, id):
        return self.filter(id=id)


class FacilityReadingManager(models.Manager):

    def get_queryset(self):
        return FacilityReadingQuerySet(self.model, using=self._db)


class FacilityReading(BaseModel):

    pir = models.BooleanField()
    temperature = models.IntegerField()
    light = models.IntegerField()
    ultrasonic = models.FloatField()
    facility = models.ForeignKey(Facility, null=True, on_delete=models.SET_NULL)

    objects = FacilityReadingManager()

    class Meta:
        db_table = "iot_facility_reading"


class FacilityReadingQuerySet2(models.QuerySet):

    def id(self, id):
        return self.filter(id=id)


class FacilityReadingManager2(models.Manager):

    def get_queryset(self):
        return FacilityReadingQuerySet2(self.model, using=self._db)


class FacilityReading2(BaseModel):

    facility = models.ForeignKey(Facility, null=True, on_delete=models.SET_NULL)
    reading_type = models.CharField(max_length=100)
    value = models.FloatField(default=0.0)

    objects = FacilityReadingManager2()

    class Meta:
        db_table = "iot_facility_reading2"
