from django.shortcuts import render, redirect, get_object_or_404 
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail  # ✅ Added

from .models import Booking, Tool
from .forms import BookingForm


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
    initial_data = {}

    if tool_id:
        try:
            tool = Tool.objects.get(id=tool_id)
            initial_data['tool'] = tool
        except Tool.DoesNotExist:
            tool = None  # Optional: handle invalid tool_id

    form = BookingForm(request.POST or None, initial=initial_data)

    if form.is_valid():
        booking = form.save(commit=False)
        booking.user = request.user
        booking.save()

        # ✅ Send confirmation email
        if request.user.email:
            send_mail(
                subject='Your Booking Confirmation',
                message=(
                    f"Hi {request.user.username},\n\n"
                    f"Your booking for '{booking.tool.name}' on {booking.date} "
                    f"from {booking.start_time} to {booking.end_time} has been confirmed.\n\n"
                    f"Thank you for using our tool booking service!"
                ),
                from_email='no-reply@toolbooking.com',  # Change in production
                recipient_list=[request.user.email],
                fail_silently=True,  # Prevent crash if email fails
            )

        return redirect('home')

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
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'bookings/register.html', {'form': form})


# -------------------------
# Tool list page
# -------------------------
def tool_list(request):
    tools = Tool.objects.all()
    return render(request, 'bookings/tool_list.html', {'tools': tools})
