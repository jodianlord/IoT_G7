from django.http import HttpResponse, JsonResponse
from django.forms.models import model_to_dict
from Sensors.models import Sensor
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, time, timedelta, tzinfo
from django.utils.timezone import make_aware

# Returns the latest record in the database
# Used to check if the sensors are still active
def latest(request):
    latest_record = Sensor.objects.last()
    dict_record = model_to_dict(latest_record)
    return JsonResponse(dict_record, content_type="application/json")

def status(request):
    latest_ultra = Sensor.objects.filter(reading_type='ultra').last()
    latest_light = Sensor.objects.filter(reading_type='light').last()
    latest_temp = Sensor.objects.filter(reading_type='temp').last()

    latest_ultra_time = latest_ultra.created_at
    latest_temp_time = latest_temp.created_at
    latest_light_time = latest_light.created_at

    # Get the latest time of the latest update among all the sensors
    latest_time = latest_ultra_time

    if latest_light_time > latest_time:
        latest_time = latest_light_time
    elif latest_temp_time > latest_time:
        latest_time = latest_temp_time

    # Determine if the room is occupied
    occupied = True

    if latest_ultra.value > 500:
        occupied = False

    # Determine if utilities are being used
    lights_on = True
    aircon_on = True

    if latest_light.value < 20:
        lights_on = False

    if latest_temp.value > 24:
        aircon_on = False

    to_return = {
        "occupancy": occupied,
        "lights_on": lights_on,
        "aircon_on": aircon_on,
        "ultra": latest_ultra.value,
        "light": latest_light.value,
        "temp": latest_temp.value,
        "time": latest_time
    }
    return JsonResponse(to_return, content_type="application/json")

class GMT8(tzinfo):
    def utcoffset(self, dt):
        return timedelta(hours=1)
    def dst(self, dt):
        return timedelta(0)
    def tzname(self,dt):
        return "Singapore"

# Get records and status at a certain time
@csrf_exempt
def status_time(request):
    if request.method == 'POST':
        try:
            # Parse form POST data
            date_received = request.POST['date']
            time_received = request.POST['time']
            date_parsed = datetime.strptime(date_received, "%d-%m-%Y").date()
            time_parsed = time(int(time_received[:2]), int(time_received[-2:]))

            # Get time stamp 1 hour before
            timestamp = datetime.combine(date_parsed, time_parsed)
            timestamp_thirty = timestamp - timedelta(minutes=60)

            # Add timezone data to the timestamp
            timestamp = make_aware(timestamp)
            timestamp_thirty = make_aware(timestamp_thirty)

            # Query database within this range and get the latest possible record
            latest_light = Sensor.objects.filter(reading_type='light',
                                                 created_at__range=(timestamp_thirty, timestamp)).last()
            latest_temp = Sensor.objects.filter(reading_type='temp',
                                                created_at__range=(timestamp_thirty, timestamp)).last()
            latest_ultra = Sensor.objects.filter(reading_type='ultra',
                                                 created_at__range=(timestamp_thirty, timestamp)).last()

            latest_ultra_time = latest_ultra.created_at
            latest_temp_time = latest_temp.created_at
            latest_light_time = latest_light.created_at

            # Get the latest time of the latest update among all the sensors
            latest_time = latest_ultra_time

            if latest_light_time > latest_time:
                latest_time = latest_light_time
            elif latest_temp_time > latest_time:
                latest_time = latest_temp_time

            # Determine if the room is occupied
            occupied = True

            if latest_ultra.value > 500:
                occupied = False

            # Determine if utilities are being used
            lights_on = True
            aircon_on = True

            if latest_light.value < 20:
                lights_on = False

            if latest_temp.value > 24:
                aircon_on = False

            to_return = {
                "occupancy": occupied,
                "lights_on": lights_on,
                "aircon_on": aircon_on,
                "ultra": latest_ultra.value,
                "light": latest_light.value,
                "temp": latest_temp.value,
                "time": latest_time
            }
            return JsonResponse(to_return, content_type="application/json")
        except (TypeError, ValueError):
            return HttpResponse(status=400)
        except AttributeError:
            # if no records available
            to_return = {
                "status": "Requested Information Not Available"
            }
            return JsonResponse(to_return, content_type="application/json")

    return HttpResponse(status=400)

