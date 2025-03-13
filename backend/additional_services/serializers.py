# additional_services/serializers.py

from rest_framework import serializers
from .models import (
    Amenity, 
    AmenityCabinType, 
    AmenitiesTickets, 
    PaymentMethod, 
    Payment, 
    Baggage, 
    PaymentBaggage, 
    PaymentAmenity
)
from booking.models import Ticket, CabinType


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = '__all__'


class CabinTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CabinType
        fields = '__all__'


class AmenityCabinTypeSerializer(serializers.ModelSerializer):
    amenity = AmenitySerializer(read_only=True)
    amenity_id = serializers.PrimaryKeyRelatedField(
        queryset=Amenity.objects.all(),
        source='amenity',
        write_only=True
    )
    cabin_type = CabinTypeSerializer(read_only=True)
    cabin_type_id = serializers.PrimaryKeyRelatedField(
        queryset=CabinType.objects.all(),
        source='cabin_type',
        write_only=True
    )

    class Meta:
        model = AmenityCabinType
        fields = [
            'id', 'amenity', 'amenity_id',
            'cabin_type', 'cabin_type_id'
        ]


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'
        ref_name = 'AdditionalServicesTicket'


class AmenitiesTicketsSerializer(serializers.ModelSerializer):
    """
    При создании записи (добавлении услуги к билету) можно
    выполнять бизнес-логику в методе validate или create.
    """
    amenity = AmenitySerializer(read_only=True)
    amenity_id = serializers.PrimaryKeyRelatedField(
        queryset=Amenity.objects.all(),
        source='amenity',
        write_only=True
    )
    ticket = TicketSerializer(read_only=True)
    ticket_id = serializers.PrimaryKeyRelatedField(
        queryset=Ticket.objects.all(),
        source='ticket',
        write_only=True
    )

    class Meta:
        model = AmenitiesTickets
        fields = [
            'id', 'amenity', 'amenity_id',
            'ticket', 'ticket_id'
        ]

    def validate(self, attrs):
        """
        Пример валидации: проверяем, что до вылета рейса
        осталось > 24 часов.
        """
        ticket = attrs['ticket']
        flight = ticket.flight  # Предполагается, что в модели Ticket есть поле flight
        if flight.departure_time:
            from django.utils import timezone
            from datetime import timedelta

            if flight.departure_time <= timezone.now() + timedelta(hours=24):
                raise serializers.ValidationError(
                    "Нельзя добавить услугу менее чем за 24 часа до вылета."
                )
        return attrs


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    ticket = TicketSerializer(read_only=True)
    ticket_id = serializers.PrimaryKeyRelatedField(
        queryset=Ticket.objects.all(),
        source='ticket',
        write_only=True
    )
    payment_method = PaymentMethodSerializer(read_only=True)
    payment_method_id = serializers.PrimaryKeyRelatedField(
        queryset=PaymentMethod.objects.all(),
        source='payment_method',
        write_only=True
    )

    class Meta:
        model = Payment
        fields = [
            'id', 'ticket', 'ticket_id',
            'payment_method', 'payment_method_id',
            'payment_date', 'payment_amount',
            'payment_status'
        ]


class BaggageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Baggage
        fields = '__all__'


class PaymentBaggageSerializer(serializers.ModelSerializer):
    payment = PaymentSerializer(read_only=True)
    payment_id = serializers.PrimaryKeyRelatedField(
        queryset=Payment.objects.all(),
        source='payment',
        write_only=True
    )
    baggage = BaggageSerializer(read_only=True)
    baggage_id = serializers.PrimaryKeyRelatedField(
        queryset=Baggage.objects.all(),
        source='baggage',
        write_only=True
    )

    class Meta:
        model = PaymentBaggage
        fields = [
            'id', 'payment', 'payment_id',
            'baggage', 'baggage_id'
        ]


class PaymentAmenitySerializer(serializers.ModelSerializer):
    payment = PaymentSerializer(read_only=True)
    payment_id = serializers.PrimaryKeyRelatedField(
        queryset=Payment.objects.all(),
        source='payment',
        write_only=True
    )
    amenity = AmenitySerializer(read_only=True)
    amenity_id = serializers.PrimaryKeyRelatedField(
        queryset=Amenity.objects.all(),
        source='amenity',
        write_only=True
    )

    class Meta:
        model = PaymentAmenity
        fields = [
            'id', 'payment', 'payment_id',
            'amenity', 'amenity_id'
        ]
