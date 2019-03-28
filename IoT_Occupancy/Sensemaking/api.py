from Sensors.models import Sensor
from Sensemaking.models import Alert
from django.http import HttpResponse, JsonResponse
import pytz
from django.utils.timezone import localtime, make_aware
from datetime import datetime, time, timedelta

# Checks the last 30 minutes to see if an alert has to be sent
def alert(request):
    # Get timestamps of now and 30 minutes before
    time_now = pytz.timezone("Asia/Singapore").localize(datetime.now())
    time_thirty = time_now - timedelta(minutes=30)

    # Retrieve records from these 30 minutes from the database
    latest_light = Sensor.objects.filter(reading_type='light', created_at__range=(time_thirty, time_now))
    latest_temp = Sensor.objects.filter(reading_type='temp', created_at__range=(time_thirty, time_now))
    latest_ultra = Sensor.objects.filter(reading_type='ultra', created_at__range=(time_thirty, time_now))

    if latest_temp.last() is None or latest_light.last() is None or latest_ultra.last() is None:
        if request is not None:
            return HttpResponse(status=500)
        else:
            return

    # Determine occupancy of the room
    num_ultra_records = latest_ultra.count()
    num_unoccupied_records = 0

    if latest_ultra.last().value <= 500:
        json = {
            "status": False
        }
        if request is not None:
            return JsonResponse(json)
        else:
            return
    else:
        for ultra in latest_ultra:
            value = ultra.value
            if value > 500:
                num_unoccupied_records = num_unoccupied_records + 1

    room_unoccupied = False

    # If more than 70% of the records say the room is unoccupied, set a flag to True
    if num_unoccupied_records / num_ultra_records > 0.7:
        room_unoccupied = True

    # Check utilities wastage for light
    num_light_records = latest_light.count()
    num_light_on_records = 0

    for light in latest_light:
        value = light.value
        if value > 25:
            num_light_on_records = num_light_on_records + 1

    lights_on = False
    if num_light_on_records / num_light_records > 0.7:
        lights_on = True

    # Check utilities wastage for temperature
    num_temp_records = latest_temp.count()
    num_aircon_on_records = 0

    for temp in latest_temp:
        value = temp.value
        if value < 26:
            num_aircon_on_records = num_aircon_on_records + 1

    aircon_on = False
    if num_aircon_on_records / num_temp_records > 0.7:
        aircon_on = True

    if room_unoccupied and (aircon_on or lights_on):
        json = {
            "status": True,
            "lights_on": lights_on,
            "aircon_on": aircon_on
        }
        new_alert = Alert()
        new_alert.save()
        if request is not None:
            return JsonResponse(json)
    if request is not None:
        json = {
            "status": False
        }
        return JsonResponse(json)
