# Django admin configuration for the bookings app
from django.contrib import admin
from .models import Tool, Booking  # Updated import

admin.site.register(Tool)         # Register Tool instead of Room
admin.site.register(Booking)
