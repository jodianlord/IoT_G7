"""IoT_Occupancy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Sensors import api
from Sensemaking import api as sense

urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls),

    # GET, get the latest records for all of the sensors
    path('get_latest', api.latest),

    # GET, get the current occupancy and utilities status based on thresholds
    path('get_latest_status', api.status),

    # POST, 2 variables: 'date' in format 28-03-2019, 'time' in format 21:58. Gets status at current time.
    # If no records, return 500 HTTP Status
    path('get_status_at', api.status_time),

    # POST, updates database with record
    # 'reading_type': light, temp or ultra sensors
    # 'value': float value of the readings
    # 'facility_id': facility of the update
    path('update', api.update_records),

    # POST, retrieves history going back x minutes
    # 'minutes': number of minutes to go back
    path('get_history', api.history),

    # GET, gets alert status for utilities wastage
    path('alert', sense.alert)
]
