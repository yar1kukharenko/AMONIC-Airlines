# booking/urls.py

from django.urls import path
from booking.views import BookFlightView, FlightSearchView, PaymentConfirmationView

urlpatterns = [
    # Маршрут для поиска рейсов
    path('search-flights/', FlightSearchView.as_view(), name='search-flights'),
    
    # Маршрут для бронирования билетов
    path('book-flight/', BookFlightView.as_view(), name='book-flight'),
    
    # Маршрут для подтверждения оплаты и выпуска билетов
    path('confirm-payment/', PaymentConfirmationView.as_view(), name='confirm-payment'),
]
