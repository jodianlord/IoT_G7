from rest_framework import serializers
from facility.models import FacilityReading


class FacilityReadingSerializer(serializers.ModelSerializer):

    class Meta:
        model = FacilityReading
        fields = ('id', 'pir', 'light', 'temperature', 'ultrasonic', 'facility')
