# additional_services/views.py

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from django.utils import timezone
from datetime import timedelta

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

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
from .serializers import (
    AmenitySerializer,
    AmenityCabinTypeSerializer,
    AmenitiesTicketsSerializer,
    PaymentMethodSerializer,
    PaymentSerializer,
    BaggageSerializer,
    PaymentBaggageSerializer,
    PaymentAmenitySerializer
)

# -------------------------------
# ViewSet для дополнительной услуги
# -------------------------------
class AmenityViewSet(viewsets.ModelViewSet):
    """
    Эндпоинт для управления дополнительными услугами.
    Доступные методы: GET, POST, PUT, PATCH, DELETE.
    """
    queryset = Amenity.objects.all()
    serializer_class = AmenitySerializer

    @swagger_auto_schema(
        operation_summary="Получить список дополнительных услуг",
        operation_description="Возвращает список всех дополнительных услуг."
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Создать дополнительную услугу",
        operation_description="Создаёт новую дополнительную услугу."
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Получить детальную информацию об услуге",
        operation_description="Возвращает информацию о дополнительной услуге по её ID."
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Обновить дополнительную услугу",
        operation_description="Обновляет данные дополнительной услуги по её ID."
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Удалить дополнительную услугу",
        operation_description="Удаляет дополнительную услугу по её ID."
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


# -------------------------------
# ViewSet для связи услуги и типа кабины
# -------------------------------
class AmenityCabinTypeViewSet(viewsets.ModelViewSet):
    """
    Эндпоинт для управления связями между дополнительными услугами и типами кабин.
    """
    queryset = AmenityCabinType.objects.all()
    serializer_class = AmenityCabinTypeSerializer

    @swagger_auto_schema(
        operation_summary="Получить список связей услуги и типа кабины",
        operation_description="Возвращает список всех связей между услугами и типами кабин."
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Создать связь услуги с типом кабины",
        operation_description="Создаёт новую связь между услугой и типом кабины."
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Получить связь услуги с типом кабины",
        operation_description="Возвращает информацию по связи услуги и типа кабины по её ID."
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Обновить связь услуги с типом кабины",
        operation_description="Обновляет данные связи между услугой и типом кабины по её ID."
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Удалить связь услуги с типом кабины",
        operation_description="Удаляет связь между услугой и типом кабины по её ID."
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


# -------------------------------
# ViewSet для услуг, привязанных к билетам
# -------------------------------
class AmenitiesTicketsViewSet(viewsets.ModelViewSet):
    """
    Эндпоинт для управления дополнительными услугами, привязанными к билетам.
    """
    queryset = AmenitiesTickets.objects.all()
    serializer_class = AmenitiesTicketsSerializer

    @swagger_auto_schema(
        operation_summary="Получить список услуг для билетов",
        operation_description="Возвращает список всех услуг, привязанных к билетам."
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Создать услугу для билета",
        operation_description="Добавляет дополнительную услугу к конкретному билету."
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Получить услугу для билета",
        operation_description="Возвращает информацию о дополнительной услуге для билета по её ID."
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Обновить услугу для билета",
        operation_description="Обновляет данные дополнительной услуги для билета по её ID."
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Удалить услугу для билета",
        operation_description="Удаляет запись о дополнительной услуге, привязанной к билету, по её ID."
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


# -------------------------------
# ViewSet для методов оплаты
# -------------------------------
class PaymentMethodViewSet(viewsets.ModelViewSet):
    """
    Эндпоинт для управления методами оплаты.
    """
    queryset = PaymentMethod.objects.all()
    serializer_class = PaymentMethodSerializer

    @swagger_auto_schema(
        operation_summary="Получить список методов оплаты",
        operation_description="Возвращает список всех доступных методов оплаты."
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Создать метод оплаты",
        operation_description="Создаёт новый метод оплаты."
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Получить метод оплаты",
        operation_description="Возвращает информацию о методе оплаты по его ID."
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Обновить метод оплаты",
        operation_description="Обновляет данные метода оплаты по его ID."
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Удалить метод оплаты",
        operation_description="Удаляет метод оплаты по его ID."
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


# -------------------------------
# ViewSet для платежей с кастомными действиями
# -------------------------------
class PaymentViewSet(viewsets.ModelViewSet):
    """
    Эндпоинт для управления платежами.
    Доступные методы: GET, POST, PUT, PATCH, DELETE.
    Дополнительно доступны кастомные действия для оплаты услуг и багажа.
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    @swagger_auto_schema(
        operation_summary="Получить список платежей",
        operation_description="Возвращает список всех платежей."
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Создать платеж",
        operation_description="Создаёт новый платеж."
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Получить платеж",
        operation_description="Возвращает информацию о платеже по его ID."
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Обновить платеж",
        operation_description="Обновляет данные платежа по его ID."
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Удалить платеж",
        operation_description="Удаляет платеж по его ID."
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(
        method='post',
        operation_summary="Оплатить дополнительные услуги",
        operation_description=(
            "Эндпоинт для оплаты дополнительных услуг. "
            "Принимает список идентификаторов amenity_ids в теле запроса."
        ),
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'amenity_ids': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_INTEGER),
                    description="Список ID дополнительных услуг для оплаты"
                )
            }
        ),
        responses={200: openapi.Response(description="Дополнительные услуги успешно оплачены")}
    )
    @action(detail=True, methods=['post'])
    def pay_amenities(self, request, pk=None):
        """
        Добавляет оплату дополнительных услуг к выбранному платежу.
        """
        payment = self.get_object()
        amenity_ids = request.data.get('amenity_ids', [])
        for amenity_id in amenity_ids:
            PaymentAmenity.objects.create(
                payment=payment,
                amenity_id=amenity_id
            )
        return Response({"status": "Amenities added"}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        method='post',
        operation_summary="Оплатить багаж",
        operation_description=(
            "Эндпоинт для оплаты багажа. "
            "Принимает список идентификаторов baggage_ids в теле запроса."
        ),
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'baggage_ids': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_INTEGER),
                    description="Список ID багажа для оплаты"
                )
            }
        ),
        responses={200: openapi.Response(description="Багаж успешно оплачен")}
    )
    @action(detail=True, methods=['post'])
    def pay_baggage(self, request, pk=None):
        """
        Добавляет оплату багажа к выбранному платежу.
        """
        payment = self.get_object()
        baggage_ids = request.data.get('baggage_ids', [])
        for baggage_id in baggage_ids:
            PaymentBaggage.objects.create(
                payment=payment,
                baggage_id=baggage_id
            )
        return Response({"status": "Baggage added"}, status=status.HTTP_200_OK)


# -------------------------------
# ViewSet для вариантов багажа
# -------------------------------
class BaggageViewSet(viewsets.ModelViewSet):
    """
    Эндпоинт для управления вариантами багажа.
    """
    queryset = Baggage.objects.all()
    serializer_class = BaggageSerializer

    @swagger_auto_schema(
        operation_summary="Получить список вариантов багажа",
        operation_description="Возвращает список всех вариантов багажа."
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Создать вариант багажа",
        operation_description="Создаёт новый вариант багажа."
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Получить вариант багажа",
        operation_description="Возвращает информацию о варианте багажа по его ID."
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Обновить вариант багажа",
        operation_description="Обновляет данные варианта багажа по его ID."
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Удалить вариант багажа",
        operation_description="Удаляет вариант багажа по его ID."
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


# -------------------------------
# ViewSet для связи платежей и багажа
# -------------------------------
class PaymentBaggageViewSet(viewsets.ModelViewSet):
    """
    Эндпоинт для управления связями между платежами и вариантами багажа.
    """
    queryset = PaymentBaggage.objects.all()
    serializer_class = PaymentBaggageSerializer

    @swagger_auto_schema(
        operation_summary="Получить список связей платежей и багажа",
        operation_description="Возвращает список всех связей между платежами и вариантами багажа."
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Создать связь платежа и багажа",
        operation_description="Создаёт новую связь между платежом и вариантом багажа."
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Получить связь платежа и багажа",
        operation_description="Возвращает информацию о связи между платежом и вариантом багажа по её ID."
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Обновить связь платежа и багажа",
        operation_description="Обновляет данные связи между платежом и вариантом багажа по её ID."
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Удалить связь платежа и багажа",
        operation_description="Удаляет связь между платежом и вариантом багажа по её ID."
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


# -------------------------------
# ViewSet для связи платежей и услуг
# -------------------------------
class PaymentAmenityViewSet(viewsets.ModelViewSet):
    """
    Эндпоинт для управления связями между платежами и услугами.
    """
    queryset = PaymentAmenity.objects.all()
    serializer_class = PaymentAmenitySerializer

    @swagger_auto_schema(
        operation_summary="Получить список связей платежей и услуг",
        operation_description="Возвращает список всех связей между платежами и услугами."
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Создать связь платежа и услуги",
        operation_description="Создаёт новую связь между платежом и услугой."
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Получить связь платежа и услуги",
        operation_description="Возвращает информацию о связи между платежом и услугой по её ID."
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Обновить связь платежа и услуги",
        operation_description="Обновляет данные связи между платежом и услугой по её ID."
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Удалить связь платежа и услуги",
        operation_description="Удаляет связь между платежом и услугой по её ID."
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


# -------------------------------
# Отчёт по услугам на рейсе
# -------------------------------
class FlightAmenitiesReportView(APIView):
    """
    Эндпоинт для формирования отчёта по услугам, заказанным на конкретном рейсе.
    """
    @swagger_auto_schema(
        operation_summary="Получить отчёт по услугам рейса",
        operation_description=(
            "Возвращает список услуг, заказанных на выбранном рейсе. "
            "В URL передаётся идентификатор рейса (flight_id)."
        ),
        responses={200: AmenitiesTicketsSerializer(many=True)}
    )
    def get(self, request, flight_id):
        from booking.models import Flight, Ticket
        try:
            flight = Flight.objects.get(id=flight_id)
        except Flight.DoesNotExist:
            return Response({"detail": "Flight not found"}, status=404)

        tickets = Ticket.objects.filter(flight=flight)
        amenities_data = AmenitiesTickets.objects.filter(ticket__in=tickets)
        serializer = AmenitiesTicketsSerializer(amenities_data, many=True)
        return Response(serializer.data, status=200)
