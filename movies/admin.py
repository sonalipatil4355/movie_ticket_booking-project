from django.contrib import admin
from .models import Movie, Cast

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'language', 'status', 'release_date', 'created_at')

@admin.register(Cast)
class CastAdmin(admin.ModelAdmin):
    list_display = ('movie', 'name', 'role')
