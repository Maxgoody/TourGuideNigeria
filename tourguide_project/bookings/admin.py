from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'tourist', 'guide', 'experience', 'requested_date', 'status', 'created_at']
    list_filter = ['status', 'requested_date']
    search_fields = ['tourist__email', 'guide__email', 'experience__title']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
