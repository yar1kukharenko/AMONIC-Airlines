from rest_framework import generics, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Schedule, Route
from .serializers import ScheduleSerializer, RouteSerializer
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend

# Представление для списка и фильтрации расписаний
class ScheduleListView(generics.ListCreateAPIView):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['route__departure_airport', 'route__arrival_airport', 'date', 'flight_number']

# Представление для редактирования расписания
class ScheduleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer

# Представление для отмены или подтверждения рейса
class UpdateScheduleStatusView(APIView):
    def patch(self, request, pk):
        schedule = get_object_or_404(Schedule, pk=pk)
        status = request.data.get('status')
        if status == "confirmed":
            schedule.confirmed = True
        elif status == "cancelled":
            schedule.confirmed = False
        else:
            return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)
        
        schedule.save()
        return Response(ScheduleSerializer(schedule).data)

import csv
from django.utils.dateparse import parse_date, parse_time
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from flight.models import Airport, Route, Aircraft, Schedule

class ImportScheduleChangesView(APIView):
    def post(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        applied, discarded, missing = 0, 0, 0
        
        # Чтение файла
        try:
            decoded_file = file.read().decode('utf-8').splitlines()
            reader = csv.reader(decoded_file)
            headers = next(reader)  # Пропустить заголовки
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        for row in reader:
            try:
                action, date_str, time_str, aircraft_code, departure_code, arrival_code, confirmed_status, price_str = row
                
                # Проверка на отсутствие обязательных данных
                if not all([action, date_str, time_str, aircraft_code, departure_code, arrival_code, price_str]):
                    missing += 1
                    continue
                
                date = parse_date(date_str)
                time = parse_time(time_str)
                price = float(price_str)
                confirmed = confirmed_status.upper() == "OK"

                # Получение аэропортов и самолета
                try:
                    departure_airport = Airport.objects.get(IATA_code=departure_code)
                    arrival_airport = Airport.objects.get(IATA_code=arrival_code)
                    aircraft = Aircraft.objects.get(make_model=aircraft_code)
                except (Airport.DoesNotExist, Aircraft.DoesNotExist):
                    missing += 1
                    continue

                # Получение маршрута (создание, если не существует)
                route, _ = Route.objects.get_or_create(
                    departure_airport=departure_airport,
                    arrival_airport=arrival_airport,
                    defaults={"distance": 1000, "flight_time": "01:00:00"}  # Примерные значения
                )

                # Если действие ADD, создаем запись
                if action == "ADD":
                    schedule, created = Schedule.objects.get_or_create(
                        flight_number=f"{aircraft_code}{date_str.replace('-', '')}",
                        date=date,
                        defaults={
                            'route': route,
                            'aircraft': aircraft,
                            'time': time,
                            'economy_price': price,
                            'confirmed': confirmed
                        }
                    )
                    if created:
                        applied += 1
                    else:
                        discarded += 1  # Если запись уже существует

                # Если действие EDIT, обновляем запись
                elif action == "EDIT":
                    try:
                        schedule = Schedule.objects.get(flight_number=f"{aircraft_code}{date_str.replace('-', '')}", date=date)
                        schedule.time = time
                        schedule.economy_price = price
                        schedule.confirmed = confirmed
                        schedule.save()
                        applied += 1
                    except Schedule.DoesNotExist:
                        missing += 1  # Если запись не найдена для редактирования

            except Exception as e:
                missing += 1
                continue  # Пропускаем строку с ошибкой

        return Response({
            "Successful Changes Applied": applied,
            "Duplicate Records Discarded": discarded,
            "Record with missing fields discarded": missing
        })
