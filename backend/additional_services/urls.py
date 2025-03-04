# additional_services/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    AmenityViewSet,
    AmenityCabinTypeViewSet,
    AmenitiesTicketsViewSet,
    PaymentMethodViewSet,
    PaymentViewSet,
    BaggageViewSet,
    PaymentBaggageViewSet,
    PaymentAmenityViewSet,
    FlightAmenitiesReportView
)

router = DefaultRouter()
router.register(r'amenities', AmenityViewSet, basename='amenities')
router.register(r'amenity-cabin-types', AmenityCabinTypeViewSet, basename='amenity-cabin-types')
router.register(r'amenities-tickets', AmenitiesTicketsViewSet, basename='amenities-tickets')
router.register(r'payment-methods', PaymentMethodViewSet, basename='payment-methods')
router.register(r'payments', PaymentViewSet, basename='payments')
router.register(r'baggage', BaggageViewSet, basename='baggage')
router.register(r'payment-baggage', PaymentBaggageViewSet, basename='payment-baggage')
router.register(r'payment-amenities', PaymentAmenityViewSet, basename='payment-amenities')

urlpatterns = [
    path('api/', include(router.urls)),
    # Пример отдельного пути для кастомного отчёта
    path('api/report/flight/<int:flight_id>/', FlightAmenitiesReportView.as_view(), name='flight-amenities-report'),
]
