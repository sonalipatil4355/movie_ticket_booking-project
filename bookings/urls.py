from django.urls import path
from . import views

urlpatterns = [
   path('showtimes/<slug>/<date_str>/',views.Theater_Showtime_View,name='showtimes'),
    path('seat_selection/<int:show_id>/', views.seat_selection_view, name='seat_selection'),
    path('book_ticket/<int:show_id>/', views.BookTicketView, name='book_ticket'),
    path('your_order/<int:booking_id>/', views.view_bookings, name='your_order'),
    
]
