# additional_services/models.py

from django.db import models
from booking.models import CabinType, Ticket


# Модель дополнительной услуги (Amenity)
class Amenity(models.Model):
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title


# Промежуточная таблица между услугами и типами кабины (для случаев,
# когда одна услуга может иметь разную стоимость или доступность в зависимости от типа кабины)
class AmenityCabinType(models.Model):
    amenity = models.ForeignKey(Amenity, on_delete=models.CASCADE)
    cabin_type = models.ForeignKey(CabinType, on_delete=models.CASCADE)

    # Если нужно хранить отличающуюся цену в зависимости от типа кабины, 
    # раскомментируйте или добавьте дополнительное поле:
    # price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.amenity.title} - {self.cabin_type.name}"


# Промежуточная таблица для связки "Услуги - Билет"
# (какие услуги добавлены к конкретному билету)
class AmenitiesTickets(models.Model):
    amenity = models.ForeignKey(Amenity, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.amenity.title} for ticket {self.ticket.booking_reference}"


# Модель для способов оплаты
class PaymentMethod(models.Model):
    method_name = models.CharField(max_length=100)

    def __str__(self):
        return self.method_name


# Модель для платежа
class Payment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=50)

    def __str__(self):
        return f"Payment for {self.ticket.booking_reference}"


# Модель для багажа (различные варианты: вес и цена)
class Baggage(models.Model):
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.weight} kg - {self.price}"


# Промежуточная таблица для связки "Платёж - Багаж"
# (какой багаж был оплачен конкретным платежом)
class PaymentBaggage(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    baggage = models.ForeignKey(Baggage, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.baggage} for payment {self.payment.id}"


# Промежуточная таблица для связки "Платёж - Услуга"
# (какая услуга была оплачена конкретным платежом)
class PaymentAmenity(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    amenity = models.ForeignKey(Amenity, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.amenity} for payment {self.payment.id}"