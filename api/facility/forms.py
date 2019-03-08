from django import forms
from api.forms import BaseAPIForm
from facility.models import Facility, FacilityReading
import requests


class FacilityReadingForm(BaseAPIForm):

    facility = forms.ModelChoiceField(queryset=Facility.objects.all(), required=True)
    pir = forms.BooleanField(required=False)
    temperature = forms.IntegerField(required=True)
    light = forms.IntegerField(required=True)
    ultrasonic = forms.FloatField(required=True)

    def save(self):
        facility = self.cleaned_data.get('facility')
        pir = self.cleaned_data.get('pir')
        temperature = self.cleaned_data.get('temperature')
        light = self.cleaned_data.get('light')
        ultrasonic = self.cleaned_data.get('ultrasonic')

        facility_reading = FacilityReading(facility=facility, pir=pir, temperature=temperature, light=light,
                                           ultrasonic=ultrasonic)
        facility_reading.save()

        #Telegram bot -- not done.
        # message = "&text= Room name:" + str(facility.name)+"%0D%0A Temperature : "+str(temperature)
        # url = "https://api.telegram.org/bot709093710:AAFsz53pcCxcTZU2fhche6ihnJoKG9jTjcA/sendMessage?chat_id=-325193992" \
        #       + message
        # requests.get(url)

        return facility_reading.id


class FacilityReadingListForm(BaseAPIForm):

    facility = forms.ModelChoiceField(queryset=Facility.objects.all(), required=False)

    def get_queryset(self):
        facility = self.cleaned_data.get('facility')
        object_list = FacilityReading.objects.get_queryset().order_by('-created_at')[:3]

        if facility:
            object_list = object_list.filter(facility=facility)

        return object_list



