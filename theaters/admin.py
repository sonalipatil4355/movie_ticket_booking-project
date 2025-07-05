from django.contrib import admin
from .models import Theater,Seat,Showtime

# Register your models here.
@admin.register(Theater)
class TheaterAdmin(admin.ModelAdmin):
    list_display = ('name','city','address')

@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('theater','seat_number','row_label','seat_type')

@admin.register(Showtime)
class ShowtimeAdmin(admin.ModelAdmin):
    list_display = ('theater','movie','showtime','silver_price','gold_price','recliner_price')


