import datetime
from django import forms
from .models import Booking

def _daterange_choices(days_ahead: int = 30):
    today = datetime.date.today()
    choices = []
    for i in range(days_ahead + 1):
        d = today + datetime.timedelta(days=i)
        label = d.strftime("%d.%m.%Y")
        choices.append((d.isoformat(), label))
    return choices

def _time_choices(start_hour: int = 6, end_hour: int = 23, step_minutes: int = 30):
    choices = []
    t = datetime.datetime(2000, 1, 1, start_hour, 0)
    last = datetime.datetime(2000, 1, 1, end_hour, 30)
    step = datetime.timedelta(minutes=step_minutes)
    while t <= last:
        val = t.time().strftime("%H:%M")
        choices.append((val, val))
        t += step
    return choices

class BookingForm(forms.ModelForm):
    date = forms.ChoiceField(label="Дата")
    start_time = forms.ChoiceField(label="Начало")
    end_time = forms.ChoiceField(label="Конец")

    class Meta:
        model = Booking
        fields = ["full_name", "phone", "date", "start_time", "end_time"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Ближайшие 30 дней
        self.fields["date"].choices = _daterange_choices(30)

        # Время с шагом 30 минут
        time_choices = _time_choices(6, 23, 30)
        self.fields["start_time"].choices = time_choices
        self.fields["end_time"].choices = time_choices

        for name in ["date", "start_time", "end_time"]:
            self.fields[name].widget.attrs.update({"class": "select"})

    def clean(self):
        cleaned = super().clean()

        date_str = cleaned.get("date")
        start_str = cleaned.get("start_time")
        end_str = cleaned.get("end_time")

        if not date_str or not start_str or not end_str:
            return cleaned

        date = datetime.date.fromisoformat(date_str)
        start = datetime.time.fromisoformat(start_str)
        end = datetime.time.fromisoformat(end_str)

        if date < datetime.date.today():
            raise forms.ValidationError("Нельзя бронировать прошедшую дату.")

        start_dt = datetime.datetime.combine(date, start)
        end_dt = datetime.datetime.combine(date, end)

        if end_dt <= start_dt:
            raise forms.ValidationError("Время окончания должно быть позже времени начала.")

        # Минимум 1 час
        if (end_dt - start_dt) < datetime.timedelta(hours=1):
            raise forms.ValidationError("Минимальная длительность брони — 1 час.")

        # Проверка пересечений
        overlaps = Booking.objects.filter(date=date).exclude(status="canceled")
        for b in overlaps:
            b_start = datetime.datetime.combine(date, b.start_time)
            b_end = datetime.datetime.combine(date, b.end_time)
            if not (end_dt <= b_start or start_dt >= b_end):
                raise forms.ValidationError("Этот слот пересекается с уже существующей бронью.")

        cleaned["date"] = date
        cleaned["start_time"] = start
        cleaned["end_time"] = end
        return cleaned