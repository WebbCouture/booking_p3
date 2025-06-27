from django.contrib import admin
from django.utils.html import format_html
from .models import Tool, Booking

@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'image_preview')

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height: 50px;"/>', obj.image.url)
        return "-"
    image_preview.short_description = 'Image Preview'

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('tool', 'user', 'start_time', 'end_time')
