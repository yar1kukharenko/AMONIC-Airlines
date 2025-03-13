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


class PassengerSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=20)
    passport_number = serializers.CharField(max_length=20)
    passport_country = serializers.IntegerField()

# Сериализатор для бронирования билетов
class TicketSerializer(serializers.ModelSerializer):
    passengers = PassengerSerializer(many=True)

    class Meta:
        model = Ticket
        fields = ['schedule', 'passengers', 'booking_reference', 'confirmed']

    def create(self, validated_data):
        passengers_data = validated_data.pop('passengers')
        tickets = []
        for passenger_data in passengers_data:
            ticket = Ticket.objects.create(**passenger_data, **validated_data)
            tickets.append(ticket)
        return tickets
    

class PaymentConfirmationSerializer(serializers.Serializer):
    booking_reference = serializers.CharField(max_length=10)  # Уникальный номер бронирования
    payment_method = serializers.ChoiceField(choices=[('credit_card', 'Credit Card'), ('cash', 'Cash'), ('voucher', 'Voucher')])

    def validate(self, data):
        """
        Проверяем, существует ли бронирование по данному номеру.
        """
        if not Ticket.objects.filter(booking_reference=data['booking_reference']).exists():
            raise serializers.ValidationError("Booking reference not found.")
        return data

    def process_payment(self, booking_reference, payment_method):
        """
        Обрабатываем оплату и выпускаем билеты.
        """
        # Получаем все билеты по номеру бронирования
        tickets = Ticket.objects.filter(booking_reference=booking_reference)
        total_amount = sum(ticket.schedule.economy_price for ticket in tickets)  # Подсчет суммы
        # После оплаты, меняем статус билетов на "выпущен"
        tickets.update(confirmed=True)
        return {
            'total_amount': total_amount,
            'tickets_issued': [ticket.id for ticket in tickets],
            'payment_method': payment_method
        }
