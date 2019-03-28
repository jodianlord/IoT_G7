from django.http import HttpResponse, JsonResponse
from django.forms.models import model_to_dict
from Sensors.models import Sensor
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, time, timedelta
from django.utils.timezone import make_aware
from django.utils.timezone import localtime
from Sensemaking import api as al
import pytz

# Returns the latest record in the database
# Used to check if the sensors are still active
def latest(request):
    latest_record = Sensor.objects.last()
    dict_record = model_to_dict(latest_record)
    timestamp = dict_record['created_at']
    local = localtime(timestamp)
    dict_record['created_at'] = local
    return JsonResponse(dict_record, content_type="application/json")

# Get the latest status of the room
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

@csrf_exempt
def update_records(request):
    if request.method == 'POST':
        try:
            reading_type = request.POST['reading_type']
            value = request.POST['value']
            facility_id = request.POST['facility_id']
            new_record = Sensor(reading_type=reading_type, value=value, facility_id=facility_id)
            new_record.save()
            al.alert(None)
            return HttpResponse(status=200)
        except (TypeError, ValueError):
            return HttpResponse(status=400)
    return HttpResponse(status=400)


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
                "time": localtime(latest_time),
                "key": latest_light.id
            }
            return JsonResponse(to_return, content_type="application/json")
        except (TypeError, ValueError):
            return HttpResponse(status=400)
        except AttributeError:
            # if no records available
            return HttpResponse(status=500)
    return HttpResponse(status=400)

# Get history of records going back x minutes
@csrf_exempt
def history(request):
    if request.method == 'POST':
        try:
            # Generate timestamp before now for the number of minutes specified
            time_back = int(request.POST['minutes'])
            time_now = pytz.timezone("Asia/Singapore").localize(datetime.now())
            time_before = time_now - timedelta(minutes=time_back)

            # Query the latest records given the time frame
            latest_light = Sensor.objects.filter(reading_type='light',
                                                 created_at__range=(time_before, time_now))
            latest_ultra = Sensor.objects.filter(reading_type='ultra',
                                                 created_at__range=(time_before, time_now))
            latest_temp = Sensor.objects.filter(reading_type='temp',
                                                created_at__range=(time_before, time_now))

            # Prepare Dict object to store records
            json = {
                "light": [],
                "ultra": [],
                "temp": []
            }

            # Further filter data, convert to local time
            for light in latest_light:
                to_add = {
                    "created_at": localtime(light.created_at),
                    "value": light.value,
                }
                json['light'].append(to_add)

            for ultra in latest_ultra:
                to_add = {
                    "created_at": localtime(ultra.created_at),
                    "value": ultra.value,
                }
                json['ultra'].append(to_add)

            for temp in latest_temp:
                to_add = {
                    "created_at": localtime(temp.created_at),
                    "value": temp.value,
                }
                json['temp'].append(to_add)

            return JsonResponse(json)
        except AttributeError:
            return HttpResponse(status=500)
    return HttpResponse(status=400)

