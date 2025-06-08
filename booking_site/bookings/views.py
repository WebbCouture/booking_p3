from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Booking
from .forms import BookingForm

# List all bookings
def booking_list(request):
    bookings = Booking.objects.all()
    return render(request, 'bookings/booking_list.html', {'bookings': bookings})

# Create new booking
def booking_create(request):
    form = BookingForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('booking_list')
    return render(request, 'bookings/booking_form.html', {'form': form})

# Update existing booking
def booking_update(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    form = BookingForm(request.POST or None, instance=booking)
    if form.is_valid():
        form.save()
        return redirect('booking_list')
    return render(request, 'bookings/booking_form.html', {'form': form})

# Delete a booking
def booking_delete(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if request.method == 'POST':
        booking.delete()
        return redirect('booking_list')
    return render(request, 'bookings/booking_confirm_delete.html', {'booking': booking})