# flight/models.py

from django.db import models

# Модель для стран
class Country(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Модель для аэропортов
class Airport(models.Model):
    country = models.ForeignKey('Country', on_delete=models.CASCADE)
    IATA_code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.IATA_code})"


# Модель для самолетов
class Aircraft(models.Model):
    name = models.CharField(max_length=100)
    make_model = models.CharField(max_length=100)
    total_seats = models.IntegerField()
    economy_seats = models.IntegerField()
    business_seats = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.make_model})"


# Модель для маршрутов
class Route(models.Model):
    departure_airport = models.ForeignKey('Airport', related_name='departure_routes', on_delete=models.CASCADE)
    arrival_airport = models.ForeignKey('Airport', related_name='arrival_routes', on_delete=models.CASCADE)
    distance = models.IntegerField()  # Расстояние в км
    flight_time = models.DurationField()  # Время полета

    def __str__(self):
        return f"Route from {self.departure_airport} to {self.arrival_airport}"


# Модель для расписания рейсов
class Schedule(models.Model):
    route = models.ForeignKey('Route', on_delete=models.CASCADE)
    aircraft = models.ForeignKey('Aircraft', on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    flight_number = models.CharField(max_length=10)
    economy_price = models.DecimalField(max_digits=10, decimal_places=2)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"Flight {self.flight_number} on {self.date}"
