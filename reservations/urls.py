from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("book/", views.booking_create, name="booking_create"),
    path("booking/<int:booking_id>/", views.booking_detail, name="booking_detail"),

    path("booking/<int:booking_id>/pay/", views.payment_start, name="payment_start"),
    path("booking/<int:booking_id>/pay/success/", views.payment_success, name="payment_success"),
    path("booking/<int:booking_id>/pay/fail/", views.payment_fail, name="payment_fail"),

    path("stream/", views.stream, name="stream"),
]
