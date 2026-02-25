from django.contrib import admin
from .models import Booking, Payment

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("id", "date", "start_time", "end_time", "full_name", "phone", "price_rub", "status", "created_at")
    list_filter = ("status", "date")
    search_fields = ("full_name", "phone")

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "booking", "provider", "amount_rub", "is_success", "created_at")
    list_filter = ("provider", "is_success")
