import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest
from .models import Booking, Payment
from .forms import BookingForm

PRICE_PER_HOUR_RUB = 1500

def _ceil_to_minutes(delta: datetime.timedelta, minutes: int = 30) -> int:
    total_minutes = int(delta.total_seconds() // 60)
    if total_minutes % minutes == 0:
        return total_minutes
    return total_minutes + (minutes - (total_minutes % minutes))

def home(request):
    bookings = Booking.objects.all()[:20]
    return render(request, "reservations/index.html", {"bookings": bookings})

def booking_create(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)

            start_dt = datetime.datetime.combine(booking.date, booking.start_time)
            end_dt = datetime.datetime.combine(booking.date, booking.end_time)

            minutes = _ceil_to_minutes(end_dt - start_dt, 30)
            booking.price_rub = int((minutes / 60) * PRICE_PER_HOUR_RUB)

            booking.status = "pending"
            booking.save()
            return redirect("payment_start", booking_id=booking.id)
    else:
        form = BookingForm()

    return render(request, "reservations/booking_create.html", {"form": form})

def booking_detail(request, booking_id: int):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, "reservations/booking_detail.html", {"booking": booking})

def payment_start(request, booking_id: int):
    booking = get_object_or_404(Booking, id=booking_id)
    payment, _ = Payment.objects.get_or_create(
        booking=booking,
        defaults={"amount_rub": booking.price_rub, "provider": "test"},
    )

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "success":
            payment.is_success = True
            payment.save()
            booking.status = "paid"
            booking.save()
            return redirect("payment_success", booking_id=booking.id)
        if action == "fail":
            payment.is_success = False
            payment.save()
            return redirect("payment_fail", booking_id=booking.id)
        return HttpResponseBadRequest("Unknown action")

    return render(request, "reservations/payment_start.html", {"booking": booking, "payment": payment})

def payment_success(request, booking_id: int):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, "reservations/payment_success.html", {"booking": booking})

def payment_fail(request, booking_id: int):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, "reservations/payment_fail.html", {"booking": booking})

def stream(request):
    rutube_embed_url = "https://rutube.ru/play/embed/9f9c6b7b1f7a8f9e0c123456789abcd/"
    return render(request, "reservations/stream.html", {"rutube_embed_url": rutube_embed_url})