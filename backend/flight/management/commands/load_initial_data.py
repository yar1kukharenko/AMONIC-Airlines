import csv
from django.core.management.base import BaseCommand
from flight.models import Country, Airport, Aircraft, Route, Schedule
from django.utils.dateparse import parse_duration

class Command(BaseCommand):
    help = 'Loads initial data from CSV files into the database'

    def handle(self, *args, **kwargs):
        self.load_countries()
        self.load_airports()
        self.load_aircrafts()
        self.load_routes()
        self.load_schedules()

    def load_countries(self):
        countries_data = [
            (1, 'United Arab Emirates'),
            (2, 'Egypt'),
            (3, 'Bahrain'),
            (4, 'Yemen'),
            (5, 'Qatar'),
            (6, 'Saudi Arabia')
        ]
        
        for country_id, country_name in countries_data:
            Country.objects.get_or_create(id=country_id, defaults={'name': country_name})
        self.stdout.write(self.style.SUCCESS('Countries loaded successfully.'))

    def load_airports(self):
        with open('flight/data/airports.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                country = Country.objects.get(id=row['country_id'])
                Airport.objects.get_or_create(
                    IATA_code=row['IATA_code'],
                    defaults={'name': row['name'], 'country': country}
                )
        self.stdout.write(self.style.SUCCESS('Airports loaded successfully.'))

    def load_aircrafts(self):
        with open('flight/data/aircrafts.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Aircraft.objects.get_or_create(
                    name=row['name'],
                    defaults={
                        'make_model': row['make_model'],
                        'total_seats': row['total_seats'],
                        'economy_seats': row['economy_seats'],
                        'business_seats': row['business_seats'],
                    }
                )
        self.stdout.write(self.style.SUCCESS('Aircrafts loaded successfully.'))

    def load_routes(self):
        with open('flight/data/routes.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                departure_airport = Airport.objects.get(id=row['departure_airport_id'])
                arrival_airport = Airport.objects.get(id=row['arrival_airport_id'])
                Route.objects.get_or_create(
                    departure_airport=departure_airport,
                    arrival_airport=arrival_airport,
                    defaults={
                        'distance': row['distance'],
                        'flight_time': parse_duration(row['flight_time'])
                    }
                )
        self.stdout.write(self.style.SUCCESS('Routes loaded successfully.'))

    def load_schedules(self):
        with open('flight/data/schedules.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                route = Route.objects.get(id=row['route_id'])
                aircraft = Aircraft.objects.get(id=row['aircraft_id'])
                Schedule.objects.get_or_create(
                    flight_number=row['flight_number'],
                    defaults={
                        'route': route,
                        'aircraft': aircraft,
                        'date': row['date'],
                        'time': row['time'],
                        'economy_price': row['economy_price'],
                        'confirmed': row['confirmed'] == 'True'
                    }
                )
        self.stdout.write(self.style.SUCCESS('Schedules loaded successfully.'))
