# booking/views.py

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from flight.models import Airport, Schedule
from booking.serializers import FlightScheduleSerializer, FlightSearchSerializer, PaymentConfirmationSerializer, TicketSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from datetime import timedelta

# Поиск рейсов с возможностью выбора пересадки и обратного полета
class FlightSearchView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('departure_airport', openapi.IN_QUERY, description="IATA код аэропорта отправления", type=openapi.TYPE_STRING),
            openapi.Parameter('arrival_airport', openapi.IN_QUERY, description="IATA код аэропорта прибытия", type=openapi.TYPE_STRING),
            openapi.Parameter('outbound_date', openapi.IN_QUERY, description="Дата вылета (YYYY-MM-DD)", type=openapi.TYPE_STRING),
            openapi.Parameter('return_date', openapi.IN_QUERY, description="Дата обратного рейса (YYYY-MM-DD, опционально)", type=openapi.TYPE_STRING),
            openapi.Parameter('cabin_type', openapi.IN_QUERY, description="Тип кабины (economy или business)", type=openapi.TYPE_STRING),
            openapi.Parameter('include_stopovers', openapi.IN_QUERY, description="Включить рейсы с пересадками", type=openapi.TYPE_BOOLEAN)
        ],
        responses={200: FlightScheduleSerializer(many=True)},
        operation_description="Эндпоинт для поиска рейсов с пересадками и возможностью выбора обратного полета"
    )
    def get(self, request):
        serializer = FlightSearchSerializer(data=request.query_params)
        if serializer.is_valid():
            departure_airport = serializer.validated_data['departure_airport']
            arrival_airport = serializer.validated_data['arrival_airport']
            outbound_date = serializer.validated_data['outbound_date']
            return_date = serializer.validated_data.get('return_date')
            cabin_type = serializer.validated_data['cabin_type']
            include_stopovers = request.query_params.get('include_stopovers', 'false').lower() == 'true'

            response_data = {}

            # Поиск прямых рейсов для даты вылета
            outbound_schedules = Schedule.objects.filter(
                route__departure_airport__IATA_code=departure_airport,
                route__arrival_airport__IATA_code=arrival_airport,
                date__range=[outbound_date - timedelta(days=3), outbound_date + timedelta(days=3)]
            )

            outbound_serializer = FlightScheduleSerializer(outbound_schedules, many=True)
            response_data['outbound_flights'] = outbound_serializer.data

            # Если включены пересадки и прямые рейсы недостаточны
            if include_stopovers or not outbound_schedules.exists():
                stopover_flights = self.find_stopover_flights(departure_airport, arrival_airport, outbound_date)
                if stopover_flights:
                    response_data['stopover_outbound_flights'] = stopover_flights

            # Если указана дата обратного рейса, добавляем поиск рейсов обратно
            if return_date:
                return_schedules = Schedule.objects.filter(
                    route__departure_airport__IATA_code=arrival_airport,
                    route__arrival_airport__IATA_code=departure_airport,
                    date__range=[return_date - timedelta(days=3), return_date + timedelta(days=3)]
                )
                return_serializer = FlightScheduleSerializer(return_schedules, many=True)
                response_data['return_flights'] = return_serializer.data

                # Поиск обратных рейсов с пересадками
                if include_stopovers or not return_schedules.exists():
                    stopover_return_flights = self.find_stopover_flights(arrival_airport, departure_airport, return_date)
                    if stopover_return_flights:
                        response_data['stopover_return_flights'] = stopover_return_flights

            return Response(response_data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def find_stopover_flights(self, departure_airport_code, arrival_airport_code, flight_date):
        """
        Функция для поиска рейсов с пересадками.
        """
        stopover_flights = []

        # Находим все маршруты, которые могут быть промежуточными
        departure_airport = Airport.objects.get(IATA_code=departure_airport_code)
        arrival_airport = Airport.objects.get(IATA_code=arrival_airport_code)

        # 1-й сегмент: из аэропорта отправления в любой другой аэропорт (кроме аэропорта прибытия)
        first_leg_schedules = Schedule.objects.filter(
            route__departure_airport=departure_airport,
            date__range=[flight_date - timedelta(days=3), flight_date + timedelta(days=3)]
        ).exclude(route__arrival_airport=arrival_airport)

        for first_leg in first_leg_schedules:
            # 2-й сегмент: из промежуточного аэропорта в аэропорт прибытия
            second_leg_schedules = Schedule.objects.filter(
                route__departure_airport=first_leg.route.arrival_airport,
                route__arrival_airport=arrival_airport,
                date__range=[first_leg.date, first_leg.date + timedelta(days=1)]  # Рассматриваем рейсы с интервалом в один день
            )

            for second_leg in second_leg_schedules:
                stopover_flights.append({
                    'first_leg': FlightScheduleSerializer(first_leg).data,
                    'second_leg': FlightScheduleSerializer(second_leg).data
                })

        return stopover_flights


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
            # Если рейс с пересадками, бронируем оба сегмента
            if 'first_leg' in request.data and 'second_leg' in request.data:
                first_leg_schedule_id = request.data['first_leg']
                second_leg_schedule_id = request.data['second_leg']
                
                # Создаем билеты для первого сегмента
                first_leg_tickets = self.create_tickets_for_leg(serializer, first_leg_schedule_id, request.data['passengers'])
                
                # Создаем билеты для второго сегмента
                second_leg_tickets = self.create_tickets_for_leg(serializer, second_leg_schedule_id, request.data['passengers'])
                
                return Response({
                    'message': 'Booking successful for both segments',
                    'first_leg_tickets': [ticket.id for ticket in first_leg_tickets],
                    'second_leg_tickets': [ticket.id for ticket in second_leg_tickets]
                }, status=status.HTTP_201_CREATED)
            
            else:
                # Если рейс прямой, создаем билеты для одного сегмента
                tickets = serializer.save()
                return Response({
                    'message': 'Booking successful',
                    'tickets': [ticket.id for ticket in tickets]
                }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def create_tickets_for_leg(self, serializer, schedule_id, passengers):
        """
        Функция для создания билетов для указанного сегмента рейса (schedule).
        """
        schedule_data = {'schedule': schedule_id}
        tickets_data = [{'schedule': schedule_id, **passenger} for passenger in passengers]
        tickets = serializer.create({'schedule': schedule_id, 'passengers': passengers})
        return tickets
    


class PaymentConfirmationView(APIView):
    @swagger_auto_schema(
        request_body=PaymentConfirmationSerializer,
        responses={200: 'Payment confirmed and tickets issued', 400: 'Invalid data'},
        operation_description="Подтверждение оплаты и выпуск билетов"
    )
    def post(self, request):
        serializer = PaymentConfirmationSerializer(data=request.data)
        if serializer.is_valid():
            booking_reference = serializer.validated_data['booking_reference']
            payment_method = serializer.validated_data['payment_method']
            
            # Обрабатываем оплату и выпускаем билеты
            result = serializer.process_payment(booking_reference, payment_method)
            
            return Response({
                'message': 'Payment confirmed and tickets issued',
                'total_amount': result['total_amount'],
                'tickets_issued': result['tickets_issued'],
                'payment_method': result['payment_method']
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)