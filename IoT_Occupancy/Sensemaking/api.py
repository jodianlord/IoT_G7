from Sensors.models import Sensor
from django.http import HttpResponse, JsonResponse

# Checks the last 30 minutes to see if an alert has to be sennt
def alert(request):
    return HttpResponse(status=200)