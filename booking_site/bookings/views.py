from django.shortcuts import render, redirect, get_object_or_404 
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

from .models import Booking, Tool  # 👈 Added Tool
from .forms import BookingForm

# Home page view
def home(request):
    context = {
        'info_text': (
            "Welcome to the Booking Site! Use the navigation bar to create, "
            "view, update, or delete your bookings."
        )
    }
    if request.user.is_authenticated:
        # Show bookings only for the logged-in user
        context['bookings'] = Booking.objects.filter(user=request.user)
    return render(request, 'bookings/home.html', context)

# List bookings only for the logged-in user
@login_required
def booking_list(request):
    return redirect('home')

# Create new booking - LOGIN REQUIRED
@login_required
def booking_create(request):
    form = BookingForm(request.POST or None)
    if form.is_valid():
        booking = form.save(commit=False)
        booking.user = request.user
        booking.save()
        return redirect('home')
    return render(request, 'bookings/booking_form.html', {'form': form})

# Update existing booking - LOGIN REQUIRED and ownership check
@login_required
def booking_update(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    form = BookingForm(request.POST or None, instance=booking)
    if form.is_valid():
        form.save()
        return redirect('home')
    return render(request, 'bookings/booking_form.html', {'form': form})

# Delete a booking - LOGIN REQUIRED and ownership check
@login_required
def booking_delete(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    if request.method == 'POST':
        booking.delete()
        return redirect('home')
    return render(request, 'bookings/booking_confirm_delete.html', {'booking': booking})

# Custom login view using Django's LoginView
class CustomLoginView(LoginView):
    template_name = 'bookings/login.html'
    def get_success_url(self):
        return reverse_lazy('home')

# Custom logout view using Django's LogoutView
class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')

# User registration view
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

# ✅ NEW: List all tools view
def tool_list(request):
    tools = Tool.objects.all()
    return render(request, 'bookings/tool_list.html', {'tools': tools})
