from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib import messages
from django.http import JsonResponse
from .models import Booking, Tool
from .forms import BookingForm
import datetime


# -------------------------
# Home page view
# -------------------------
def home(request):
    context = {
        'info_text': (
            "Welcome to the Booking Site! Use the navigation bar to create, "
            "view, update, or delete your bookings."
        )
    }
    if request.user.is_authenticated:
        context['bookings'] = Booking.objects.filter(user=request.user)
    return render(request, 'bookings/home.html', context)


# -------------------------
# List bookings — just redirect to home
# -------------------------
@login_required
def booking_list(request):
    return redirect('home')


# -------------------------
# Create booking with optional tool_id
# -------------------------
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

            # Check for existing booking for the same tool and date
            if Booking.objects.filter(tool=tool, date=date).exists():
                messages.error(request, "This tool is already booked for that day. Please choose another date.")
            else:
                booking = form.save(commit=False)
                booking.user = request.user
                booking.start_time = datetime.time(10, 0)
                booking.end_time = datetime.time(17, 0)
                booking.save()

                if form.cleaned_data.get('send_email') and request.user.email:
                    send_mail(
                        subject='Your Booking Confirmation',
                        message=(
                            f"Hi {request.user.username},\n\n"
                            f"Your booking for '{booking.tool.name}' on {booking.date} "
                            f"from 10:00 to 17:00 has been confirmed.\n\n"
                            f"Thank you for using our tool booking service!"
                        ),
                        from_email='no-reply@toolbooking.com',
                        recipient_list=[request.user.email],
                        fail_silently=True,
                    )

                messages.success(request, "Your booking was successful! Pick-up at 10:00, return by 17:00.")
                return redirect('home')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = BookingForm(initial=initial_data)

    return render(request, 'bookings/booking_form.html', {'form': form})


# -------------------------
# Update existing booking
# -------------------------
@login_required
def booking_update(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    form = BookingForm(request.POST or None, instance=booking)
    if form.is_valid():
        form.save()
        messages.success(request, "Your booking was updated successfully!")
        return redirect('home')
    return render(request, 'bookings/booking_form.html', {'form': form})


# -------------------------
# Delete booking
# -------------------------
@login_required
def booking_delete(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    if request.method == 'POST':
        booking.delete()
        messages.success(request, "Your booking was deleted.")
        return redirect('home')
    return render(request, 'bookings/booking_confirm_delete.html', {'booking': booking})


# -------------------------
# Login / Logout / Register
# -------------------------
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


# -------------------------
# Tool list page
# -------------------------
def tool_list(request):
    tools = Tool.objects.all()
    return render(request, 'bookings/tool_list.html', {'tools': tools})


# -------------------------
# API: Get booked dates for a tool
# -------------------------
def booked_dates_api(request, tool_id):
    bookings = Booking.objects.filter(tool_id=tool_id)
    booked_dates = list(bookings.values_list('date', flat=True))
    booked_str = [d.strftime('%Y-%m-%d') for d in booked_dates]
    return JsonResponse({'booked_dates': booked_str})
