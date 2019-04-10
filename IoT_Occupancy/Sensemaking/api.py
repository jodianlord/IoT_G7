from Sensors.models import Sensor
from Sensemaking.models import Alert, Wastage
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
import pytz
from datetime import datetime, timedelta

ultra_threshold = 519
temp_threshold = 26
light_threshold = 18
percentage_threshold = 0.7

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

    if latest_ultra.last().value <= ultra_threshold:
        json = {
            "wastage_detected": False
        }
        if request is not None:
            return JsonResponse(json)
        else:
            return
    else:
        for ultra in latest_ultra:
            value = ultra.value
            if value > ultra_threshold:
                num_unoccupied_records = num_unoccupied_records + 1

    room_unoccupied = False

    # If more than 70% of the records say the room is unoccupied, set a flag to True
    if num_unoccupied_records / num_ultra_records > percentage_threshold:
        room_unoccupied = True

    # Check utilities wastage for light
    num_light_records = latest_light.count()
    num_light_on_records = 0

    for light in latest_light:
        value = light.value
        if value > light_threshold:
            num_light_on_records = num_light_on_records + 1

    lights_on = False
    if num_light_on_records / num_light_records > percentage_threshold:
        lights_on = True

    # Check utilities wastage for temperature
    num_temp_records = latest_temp.count()
    num_aircon_on_records = 0

    for temp in latest_temp:
        value = temp.value
        if value < temp_threshold:
            num_aircon_on_records = num_aircon_on_records + 1

    aircon_on = False
    if num_aircon_on_records / num_temp_records > percentage_threshold:
        aircon_on = True

    if room_unoccupied and (aircon_on or lights_on):
        json = {
            "wastage_detected": True,
            "lights_on": lights_on,
            "aircon_on": aircon_on
        }
        new_alert = Alert()
        new_alert.save()
        if request is not None:
            return JsonResponse(json)

    if request is not None:
        json = {
            "wastage_detected": False
        }
        return JsonResponse(json)

cost_kWh = 0.2279
light_consumption_kWh = 0.018 * 15
aircon_consumption_kWh = 5.5
light_hourly_cost = light_consumption_kWh * cost_kWh
aircon_hourly_cost = aircon_consumption_kWh * cost_kWh
@csrf_exempt
def cost_savings(request):
    day_offset = int(request.POST['days'])
    # Get current timestamp now and of 1 week ago
    time_now = pytz.timezone("Asia/Singapore").localize(datetime.now())
    time_before = time_now - timedelta(days=day_offset)

    # Retrieve records from last week into the database
    # light_records = Sensor.objects.filter(reading_type='light', created_at__range=(time_lastweek, time_now))
    # temp_records = Sensor.objects.filter(reading_type='temp', created_at__range=(time_lastweek, time_now))
    # ultra_records = Sensor.objects.filter(reading_type='ultra', created_at__range=(time_lastweek, time_now))

    # Find the earliest hour window given the time frame
    time_start = time_before
    time_end = time_before + timedelta(hours=1)

    # Store total number of wastage in hours for the duration
    light_wasted_hours = 0
    temp_wasted_hours = 0

    # Iterate through the records hourly
    while time_start < time_now:
        # Get records for each sensor
        light_records = Sensor.objects.filter(reading_type='light', created_at__range=(time_start, time_end))
        temp_records = Sensor.objects.filter(reading_type='temp', created_at__range=(time_start, time_end))
        ultra_records = Sensor.objects.filter(reading_type='ultra', created_at__range=(time_start, time_end))

        light_count = light_records.count()
        temp_count = temp_records.count()
        ultra_count = ultra_records.count()

        time_start = time_end
        time_end += timedelta(hours=1)

        # If no records, skip
        if light_count == 0 or temp_count == 0 or ultra_count == 0:
            continue

        # Store number of records
        ultra_unoccupied_counter = 0
        light_on_counter = 0
        aircon_on_counter = 0

        # Count how many records say that the room is unoccupied
        for ultra in ultra_records:
            if ultra.value > ultra_threshold:
                ultra_unoccupied_counter += 1

        # Count how many records say that the lights are on
        for light in light_records:
            if light.value > light_threshold:
                light_on_counter += 1

        # Count how many records say that the air conditioning is on
        for temp in temp_records:
            if temp.value < temp_threshold:
                aircon_on_counter += 1

        # Calculate the percentage of unoccupied records, light on records and aircon on records respectively
        ultra_percentage = float(ultra_unoccupied_counter) / ultra_count
        light_percentage = float(light_on_counter) / light_count
        aircon_percentage = float(aircon_on_counter) / temp_count

        # If percentage of utilities used is more than room occupancy over the hour, add to wastage
        if light_percentage > ultra_percentage:
            light_wasted_hours += (light_percentage - ultra_percentage)
        if aircon_percentage > ultra_percentage:
            temp_wasted_hours += (aircon_percentage - ultra_percentage)


        light_wasted = light_percentage - ultra_percentage
        temp_wasted = aircon_percentage - ultra_percentage
        if light_wasted <= 0:
            light_wasted = 0
        if temp_wasted <= 0:
            temp_wasted = 0

        # new_wastage = Wastage(time_wasted= time_start, aircon_wasted_hours=temp_wasted, light_wasted_hours=light_wasted)
        # new_wastage.save()

    light_wasted_cost = light_wasted_hours * light_hourly_cost
    aircon_wasted_cost = temp_wasted_hours * aircon_hourly_cost
    json = {
        "light_hours": light_wasted_hours,
        "temp_hours" : temp_wasted_hours,
        "light_cost_dollars": light_wasted_cost,
        "aircon_cost_dollars": aircon_wasted_cost
    }
    return JsonResponse(json)




