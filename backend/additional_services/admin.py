# additional_services/admin.py

from django.contrib import admin
from .models import Amenity, AmenityCabinType, AmenitiesTickets, PaymentMethod, Payment, Baggage, PaymentBaggage, PaymentAmenity

@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'price')
    search_fields = ('title',)
    list_filter = ('price',)

@admin.register(AmenityCabinType)
class AmenityCabinTypeAdmin(admin.ModelAdmin):
    list_display = ('id','amenity', 'cabin_type')
    search_fields = ('amenity__title', 'cabin_type__name')
    list_filter = ('cabin_type',)

@admin.register(AmenitiesTickets)
class AmenitiesTicketsAdmin(admin.ModelAdmin):
    list_display = ('id','ticket', 'amenity')
    search_fields = ('ticket__booking_reference', 'amenity__title')

@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('id','method_name',)
    search_fields = ('method_name',)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id','ticket', 'payment_method', 'payment_date', 'payment_amount', 'payment_status')
    search_fields = ('ticket__booking_reference', 'payment_status')
    list_filter = ('payment_status', 'payment_method')

@admin.register(Baggage)
class BaggageAdmin(admin.ModelAdmin):
    list_display = ('id','weight', 'price')
    search_fields = ('weight',)
    list_filter = ('weight',)

@admin.register(PaymentBaggage)
class PaymentBaggageAdmin(admin.ModelAdmin):
    list_display = ('id','payment', 'baggage')
    search_fields = ('payment__id', 'baggage__weight')

@admin.register(PaymentAmenity)
class PaymentAmenityAdmin(admin.ModelAdmin):
    list_display = ('id','payment', 'amenity')
    search_fields = ('payment__id', 'amenity__title')
