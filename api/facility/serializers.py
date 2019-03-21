from rest_framework import serializers
from facility.models import FacilityReading, FacilityReading2
import datetime
from django.utils import timezone


class FacilityReadingSerializer(serializers.ModelSerializer):

    facility = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = FacilityReading
        fields = ('id', 'pir', 'light', 'temperature', 'ultrasonic', 'facility', 'created_at', 'status')

    def get_facility(self, obj):
        return obj.facility.name

    def get_status(self, obj):
        now = timezone.now()
        now_minus_10 = now - datetime.timedelta(minutes=10)
        facility_obj = FacilityReading.objects.all().filter(facility=obj.facility).order_by('-created_at').first()
        created_at = getattr(facility_obj, 'created_at')
        if created_at > now_minus_10:
            return "working"
        return "Not Working"


class FacilityReadingSerializer2(serializers.ModelSerializer):

    facility = serializers.SerializerMethodField()

    class Meta:
        model = FacilityReading2
        fields = ('id', 'reading_type', 'value', 'facility', 'created_at')

    def get_facility(self, obj):
        return obj.facility.name

