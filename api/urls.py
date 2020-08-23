from django.urls import path

from api.views import *

urlpatterns = [
    path('', calendar, name="calendar"),
    path('validate/', validate_flight, name="validate_flight")
]
