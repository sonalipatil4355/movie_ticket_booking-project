from django.urls import path
from . import views

urlpatterns = [
    path('payment/<int:booking_id>/', views.Payment_View, name='payment'),
    path('success/<int:booking_id>/', views.Success_view, name='payment_success'),
    path('cancel/<int:booking_id>/', views.Cancel_view, name='payment_cancel'),
]