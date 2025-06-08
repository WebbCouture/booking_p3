from django.shortcuts import render, redirect, get_object_or_404 
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

from .models import Booking
from .forms import BookingForm

# List bookings only for the logged-in user
@login_required
def booking_list(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'bookings/booking_list.html', {'bookings': bookings})

# Create new booking - LOGIN REQUIRED
@login_required
def booking_create(request):
    form = BookingForm(request.POST or None)
    if form.is_valid():
        booking = form.save(commit=False)
        booking.user = request.user  # assign logged-in user
        booking.save()
        return redirect('booking_list')
    return render(request, 'bookings/booking_form.html', {'form': form})

# Update existing booking - LOGIN REQUIRED and ownership check
@login_required
def booking_update(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    form = BookingForm(request.POST or None, instance=booking)
    if form.is_valid():
        form.save()
        return redirect('booking_list')
    return render(request, 'bookings/booking_form.html', {'form': form})

# Delete a booking - LOGIN REQUIRED and ownership check
@login_required
def booking_delete(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    if request.method == 'POST':
        booking.delete()
        return redirect('booking_list')
    return render(request, 'bookings/booking_confirm_delete.html', {'booking': booking})

# Custom login view using Django's LoginView
class CustomLoginView(LoginView):
    template_name = 'bookings/login.html'

# Custom logout view using Django's LogoutView
class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')  # Redirect to login page after logout

# User registration view
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('booking_list')
    else:
        form = UserCreationForm()
    return render(request, 'bookings/register.html', {'form': form})
