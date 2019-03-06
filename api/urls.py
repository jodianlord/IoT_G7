from django.urls import path, include


urlpatterns = [
    path('facility/', include(("api.facility.urls", "facility"), namespace="facility")),
]