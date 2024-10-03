# booking/models.py

from django.db import models
from flight.models import Schedule
from user.models import User, Country

# Модель для типов кабины
class CabinType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Модель для билетов
class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    cabin_type = models.ForeignKey(CabinType, on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    passport_number = models.CharField(max_length=20)
    passport_country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    booking_reference = models.CharField(max_length=100)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"Ticket {self.booking_reference} for {self.first_name} {self.last_name}"

