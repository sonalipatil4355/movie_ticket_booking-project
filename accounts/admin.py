from django.contrib import admin
from .models import User

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone', 'is_theater_manager', 'is_approved', 'otp_verified')
    search_fields = ('username', 'email', 'phone')
    ordering = ('username',)
    
    
