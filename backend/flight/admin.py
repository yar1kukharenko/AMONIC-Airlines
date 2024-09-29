# flight/admin.py

from django.contrib import admin
from .models import Airport, Aircraft, Route, Schedule, Country

@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    list_display = ('name', 'IATA_code', 'country')
    search_fields = ('name', 'IATA_code')
    list_filter = ('country',)

@admin.register(Aircraft)
class AircraftAdmin(admin.ModelAdmin):
    list_display = ('name', 'make_model', 'total_seats', 'economy_seats', 'business_seats')
    search_fields = ('name', 'make_model')
    list_filter = ('make_model',)

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('departure_airport', 'arrival_airport', 'distance', 'flight_time')
    search_fields = ('departure_airport__name', 'arrival_airport__name')
    list_filter = ('departure_airport', 'arrival_airport')

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('route', 'aircraft', 'date', 'time', 'flight_number', 'economy_price', 'confirmed')
    search_fields = ('flight_number',)
    list_filter = ('route', 'aircraft', 'date', 'confirmed')

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name',)
