# booking/urls.py

from django.urls import path
from .views import FlightSearchView, BookFlightView

urlpatterns = [
    path('search-flights/', FlightSearchView.as_view(), name='search-flights'),
    path('book-flight/', BookFlightView.as_view(), name='book-flight'),
]
