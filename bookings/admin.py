# Django admin configuration for the bookings app
from django.contrib import admin
from .models import Tool, Booking, Location  # Importera Location

admin.site.register(Location)  # Registrera Location-modellen
admin.site.register(Tool)       # Registrera Tool-modellen
admin.site.register(Booking)    # Registrera Booking-modellen
