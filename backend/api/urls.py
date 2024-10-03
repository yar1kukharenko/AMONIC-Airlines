from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from api.views import ItemViewSet
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

urlpatterns = [
    path('user/', include('user.urls')),
    path('flight/', include('flight.urls')),
    path('booking/', include('booking.urls')),
]

