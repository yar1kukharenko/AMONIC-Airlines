from rest_framework import serializers
from .models import Schedule, Route, Aircraft

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ['id', 'route', 'aircraft', 'date', 'time', 'flight_number', 'economy_price', 'confirmed']

class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ['id', 'departure_airport', 'arrival_airport', 'distance', 'flight_time']

class AircraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aircraft
        fields = ['id', 'name', 'make_model', 'total_seats', 'economy_seats', 'business_seats']
