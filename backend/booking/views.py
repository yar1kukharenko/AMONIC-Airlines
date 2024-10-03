# booking/views.py

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from flight.models import Schedule
from booking.serializers import FlightScheduleSerializer, FlightSearchSerializer, TicketSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from datetime import timedelta

# Поиск рейсов с возможностью выбора обратного полета
class FlightSearchView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('departure_airport', openapi.IN_QUERY, description="IATA код аэропорта отправления", type=openapi.TYPE_STRING),
            openapi.Parameter('arrival_airport', openapi.IN_QUERY, description="IATA код аэропорта прибытия", type=openapi.TYPE_STRING),
            openapi.Parameter('outbound_date', openapi.IN_QUERY, description="Дата вылета (YYYY-MM-DD)", type=openapi.TYPE_STRING),
            openapi.Parameter('return_date', openapi.IN_QUERY, description="Дата обратного рейса (YYYY-MM-DD, опционально)", type=openapi.TYPE_STRING),
            openapi.Parameter('cabin_type', openapi.IN_QUERY, description="Тип кабины (economy или business)", type=openapi.TYPE_STRING)
        ],
        responses={200: FlightScheduleSerializer(many=True)},
        operation_description="Эндпоинт для поиска рейсов с возможностью выбора обратного полета"
    )
    def get(self, request):
        serializer = FlightSearchSerializer(data=request.query_params)
        if serializer.is_valid():
            departure_airport = serializer.validated_data['departure_airport']
            arrival_airport = serializer.validated_data['arrival_airport']
            outbound_date = serializer.validated_data['outbound_date']
            return_date = serializer.validated_data.get('return_date')
            cabin_type = serializer.validated_data['cabin_type']

            # Поиск рейсов для даты вылета
            outbound_schedules = Schedule.objects.filter(
                route__departure_airport__IATA_code=departure_airport,
                route__arrival_airport__IATA_code=arrival_airport,
                date__range=[outbound_date - timedelta(days=3), outbound_date + timedelta(days=3)]
            )

            outbound_serializer = FlightScheduleSerializer(outbound_schedules, many=True)

            response_data = {
                'outbound_flights': outbound_serializer.data
            }

            # Если указана дата обратного рейса, добавляем поиск рейсов обратно
            if return_date:
                return_schedules = Schedule.objects.filter(
                    route__departure_airport__IATA_code=arrival_airport,
                    route__arrival_airport__IATA_code=departure_airport,
                    date__range=[return_date - timedelta(days=3), return_date + timedelta(days=3)]
                )
                return_serializer = FlightScheduleSerializer(return_schedules, many=True)
                response_data['return_flights'] = return_serializer.data

            return Response(response_data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Бронирование билета
class BookFlightView(APIView):
    @swagger_auto_schema(
        request_body=TicketSerializer,
        responses={201: 'Booking successful', 400: 'Error'},
        operation_description="Эндпоинт для бронирования рейса"
    )
    def post(self, request):
        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            ticket = serializer.save()
            return Response({'message': 'Booking successful', 'booking_reference': ticket.booking_reference}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
