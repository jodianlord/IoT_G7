from django.urls import path
from api.facility import views

urlpatterns = [
    # /api/facility/

    # facility Management
    # path('<int:pk>/', views.FacilityLCView.as_view(), name="details"),
    path('reading/', views.FacilityReadingLCView.as_view(), name="list-create"),
    # path('', views.FacilityLCView.as_view(), name="list-create-facility")



]
