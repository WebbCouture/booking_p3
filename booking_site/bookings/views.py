from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden
from .models import Booking, Tool
from .forms import BookingForm
from django.utils import timezone
import datetime


def home(request):
    context = {
        'info_text': (
            "Welcome to the Booking Site! Use the navigation bar to create, "
            "view, update, or delete your bookings."
        )
    }
    if request.user.is_authenticated:
        context['bookings'] = Booking.objects.filter(user=request.user)
        context['today'] = datetime.date.today()
    return render(request, 'bookings/home.html', context)


@login_required
def booking_list(request):
    return redirect('home')


@login_required
def booking_create(request):
    tool_id = request.GET.get('tool_id')
    initial_data = {
        'start_time': datetime.time(10, 0),
        'end_time': datetime.time(17, 0),
    }

    if tool_id:
        try:
            tool = Tool.objects.get(id=tool_id)
            initial_data['tool'] = tool
        except Tool.DoesNotExist:
            tool = None

    if request.method == 'POST':
        form = BookingForm(request.POST, initial=initial_data)
        if form.is_valid():
            date = form.cleaned_data['date']
            tool = form.cleaned_data['tool']
            send_email = form.cleaned_data.get('send_email', False)
            confirmation_email = form.cleaned_data.get('confirmation_email', '').strip()

            if send_email and not confirmation_email:
                messages.error(request, "Please enter your email address to receive confirmation.")
            else:
                if Booking.objects.filter(tool=tool, date=date).exists():
                    messages.error(request, "This tool is already booked for that day. Please choose another date.")
                else:
                    booking = form.save(commit=False)
                    booking.user = request.user
                    booking.start_time = datetime.time(10, 0)
                    booking.end_time = datetime.time(17, 0)
                    booking.save()

                    if send_email:
                        send_mail(
                            subject='Your Booking Confirmation',
                            message=(
                                f"Hi {request.user.username},\n\n"
                                f"Your booking for '{booking.tool.name}' on {booking.date} "
                                f"from 10:00 to 17:00 has been confirmed.\n\n"
                                f"Thank you for using our tool booking service!"
                            ),
                            from_email='no-reply@toolbooking.com',
                            recipient_list=[confirmation_email],
                            fail_silently=True,
                        )

                    messages.success(request, "Your booking was successful! Pick-up at 10:00, return by 17:00.")
                    return redirect('home')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = BookingForm(initial=initial_data)

    return render(request, 'bookings/booking_form.html', {'form': form})


@login_required
def booking_update(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)

    booking_end_datetime = datetime.datetime.combine(booking.date, booking.end_time)
    booking_end_datetime = timezone.make_aware(booking_end_datetime, timezone.get_current_timezone())
    now = timezone.localtime(timezone.now())

    if booking_end_datetime < now:
        return HttpResponseForbidden("You cannot edit past bookings.")

    form = BookingForm(request.POST or None, instance=booking)
    if form.is_valid():
        form.save()
        messages.success(request, "Your booking was updated successfully!")
        return redirect('home')

    return render(request, 'bookings/booking_form.html', {'form': form})


@login_required
def booking_delete(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)

    # Prevent deleting past bookings
    booking_end_datetime = datetime.datetime.combine(booking.date, booking.end_time)
    booking_end_datetime = timezone.make_aware(booking_end_datetime, timezone.get_current_timezone())
    now = timezone.localtime(timezone.now())

    if booking_end_datetime < now:
        return HttpResponseForbidden("You cannot delete past bookings.")

    if request.method == 'POST':
        booking.delete()
        messages.success(request, "Your booking was deleted.")
        return redirect('home')

    return render(request, 'bookings/booking_confirm_delete.html', {'booking': booking})


class CustomLoginView(LoginView):
    template_name = 'bookings/login.html'

    def get_success_url(self):
        return reverse_lazy('home')


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Your account was created and you're now logged in!")
            return redirect('home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            messages.error(request, "Please fix the errors below.")
    else:
        form = UserCreationForm()
    return render(request, 'bookings/register.html', {'form': form})


def tool_list(request):
    tools = Tool.objects.all()
    return render(request, 'bookings/tool_list.html', {'tools': tools})


def booked_dates_api(request, tool_id):
    bookings = Booking.objects.filter(tool_id=tool_id)
    booked_dates = list(bookings.values_list('date', flat=True))
    booked_str = [d.strftime('%Y-%m-%d') for d in booked_dates]
    return JsonResponse({'booked_dates': booked_str})
