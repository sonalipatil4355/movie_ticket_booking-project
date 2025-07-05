from django.contrib import admin
from .models import Booking, BookingSeat

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'showtime', 'total_amount', 'booking_time', 'status')

@admin.register(BookingSeat)
class BookingSeatAdmin(admin.ModelAdmin):
    list_display = ('booking','seat','showtime')