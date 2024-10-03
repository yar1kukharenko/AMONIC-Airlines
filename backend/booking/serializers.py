# booking/serializers.py

from rest_framework import serializers
from flight.models import Schedule, Route
from booking.models import Ticket, CabinType

# Сериализатор для расписания рейсов
class FlightScheduleSerializer(serializers.ModelSerializer):
    route = serializers.StringRelatedField()  # Выводим маршрут как строку
    aircraft = serializers.StringRelatedField()

    class Meta:
        model = Schedule
        fields = ['id', 'route', 'aircraft', 'date', 'time', 'flight_number', 'economy_price', 'confirmed']


# Сериализатор для поиска рейсов
# Сериализатор для поиска рейсов с датой обратного полета
class FlightSearchSerializer(serializers.Serializer):
    departure_airport = serializers.CharField(max_length=3)
    arrival_airport = serializers.CharField(max_length=3)
    outbound_date = serializers.DateField()  # Дата вылета
    return_date = serializers.DateField(required=False, allow_null=True)  # Дата обратного рейса (опционально)
    cabin_type = serializers.ChoiceField(choices=[('economy', 'Economy'), ('business', 'Business')])

# Сериализатор для бронирования билетов
class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['user', 'schedule', 'first_name', 'last_name', 'email', 'phone', 'passport_number', 'passport_country', 'booking_reference', 'confirmed']
