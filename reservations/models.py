from django.db import models
from django.utils import timezone

class Booking(models.Model):
    STATUS_CHOICES = [
        ("pending", "Ожидает оплаты"),
        ("paid", "Оплачено"),
        ("canceled", "Отменено"),
    ]

    full_name = models.CharField("ФИО", max_length=120)
    phone = models.CharField("Телефон", max_length=30)
    date = models.DateField("Дата")
    start_time = models.TimeField("Начало")
    end_time = models.TimeField("Конец")
    price_rub = models.PositiveIntegerField("Цена (₽)", default=1500)
    status = models.CharField("Статус", max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField("Создано", default=timezone.now)

    class Meta:
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.date} {self.start_time}-{self.end_time} ({self.full_name})"


class Payment(models.Model):
    PROVIDER_CHOICES = [
        ("beznal", "Безналичная оплата"),
        ('nal', "Наличная оплата"),
    ]
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name="payment", verbose_name='Бронирование')
    provider = models.CharField(verbose_name='Вид оплаты', max_length=30, choices=PROVIDER_CHOICES, default="test")
    amount_rub = models.PositiveIntegerField(verbose_name='Сумма', default=0)
    is_success = models.BooleanField(verbose_name='Оплачено', default=False)
    created_at = models.DateTimeField(verbose_name='Создано', default=timezone.now)
    external_id = models.CharField(max_length=120, blank=True, default="")

    def __str__(self):
        return f"Payment #{self.id} for booking #{self.booking_id}"

    class Meta:
        verbose_name = 'Оплата'
        verbose_name_plural = 'Оплаты'