# booking/admin.py

from django.contrib import admin
from .models import CabinType, Ticket

# Регистрируем модель CabinType
@admin.register(CabinType)
class CabinTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

# Регистрируем модель Ticket
@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'schedule', 'first_name', 'last_name', 'email', 'phone', 'passport_number', 'booking_reference', 'confirmed')
    search_fields = ('first_name', 'last_name', 'email', 'passport_number', 'booking_reference')
    list_filter = ('confirmed', 'schedule', 'cabin_type')

