from django import forms
from api.forms import BaseAPIForm
from facility.models import Facility, FacilityReading2 , FacilityReading
import requests


class FacilityReadingForm(BaseAPIForm):

    # facility = forms.ModelChoiceField(queryset=Facility.objects.all(), required=True)
    # pir = forms.BooleanField(required=False)
    # temperature = forms.IntegerField(required=True)
    # light = forms.IntegerField(required=True)
    # ultrasonic = forms.FloatField(required=True)
    #
    # def save(self):
    #     facility = self.cleaned_data.get('facility')
    #     pir = self.cleaned_data.get('pir')
    #     temperature = self.cleaned_data.get('temperature')
    #     light = self.cleaned_data.get('light')
    #     ultrasonic = self.cleaned_data.get('ultrasonic')
    #
    #     facility_reading = FacilityReading(facility=facility, pir=pir, temperature=temperature, light=light,
    #                                        ultrasonic=ultrasonic)
    #     facility_reading.save()
    #
    #     return facility_reading.id

    facility = forms.ModelChoiceField(queryset=Facility.objects.all(), required=True)
    reading_type = forms.CharField(required=True)
    value = forms.FloatField(required=True)

    def save(self):
        facility = self.cleaned_data.get('facility')
        reading_type = self.cleaned_data.get('reading_type')
        value = self.cleaned_data.get('value')

        facility_reading = FacilityReading2(facility=facility, reading_type=reading_type, value=value)
        facility_reading.save()

        return facility_reading.id


class FacilityReadingListForm(BaseAPIForm):

    facility = forms.ModelChoiceField(queryset=Facility.objects.all(), required=False)

    # def get_queryset(self):
    #     facility = self.cleaned_data.get('facility')
    #     object_list = FacilityReading.objects.get_queryset().order_by('-created_at')[:3]
    #
    #     if facility:
    #         object_list = object_list.filter(facility=facility)
    #
    #     return object_list

    def get_queryset(self):
        facility = self.cleaned_data.get('facility')
        object_list = FacilityReading2.objects.get_queryset().order_by('-created_at')

        if facility:
            object_list = object_list.filter(facility=facility)

        return object_list


# class FacilityListForm(BaseAPIForm):
#
#     def __init__(self, *args, **kwargs):
#         self.instance = kwargs.pop('instance', None)
#         super(FacilityListForm, self).__init__(*args, **kwargs)
#
#     def get_queryset(self):
#         facility = self.instance
#         object_list = FacilityReading.objects.get_queryset().filter(facility=facility.id).order_by('-created_at').first()
#         return object_list
#
#     def get_all(self):
#         facility = self.instance
#         object_list = FacilityReading.objects.all().filter(facility=facility.id).order_by('-created_at')
#         return object_list
