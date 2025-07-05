from django.shortcuts import render, get_object_or_404
from datetime import datetime, timedelta
from movies.models import Movie
from .models import Showtime, Seat
from django.conf import settings
from django.http import JsonResponse
import stripe
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from bookings.models import Booking
from django.http import HttpResponse, Http404
from bookings.models import BookingSeat
from theaters.models import Theater
from django.utils import timezone
from django.shortcuts import redirect
from datetime import date
from django.conf import settings

# Initialize Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

from django.shortcuts import render
from theaters.models import Theater,Showtime, Seat
from bookings.models import Booking, BookingSeat
from accounts.models import User
from movies.models import Movie
from django.http import HttpResponse
from datetime import datetime,timedelta
import json
from django.contrib.auth.decorators import login_required
from django.conf import settings

# Create your views here.

def Theater_Showtime_View(request, slug, date_str):
    movie = get_object_or_404(Movie, slug=slug)
    selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    today = date.today()
    next_7_days = [today + timedelta(days=i) for i in range(7)]
    current_time = datetime.now().time()

    theater_showtimes = []
    for theater in Theater.objects.all():
        showtimes = Showtime.objects.filter(
            movie=movie,
            showtime__date=selected_date,  # ✅ CORRECT FIELD NAME
            theater=theater
        )

        if selected_date == today:
            showtimes = showtimes.filter(showtime__gt=datetime.now()) 

        showtimes = showtimes.order_by('showtime')

        if showtimes.exists():
            theater_showtimes.append(showtimes)

    context = {
        'movie': movie,
        'theater_showtimes': theater_showtimes,
        'selected_date': selected_date,
        'next_7_days': next_7_days,
    }

    return render(request, 'theaters/showtime.html', context)
def seat_selection_view(request, show_id):
    showtime = Showtime.objects.get(id=show_id)
    theater = showtime.theater
    movie = showtime.movie
    seats = Seat.objects.filter(theater=theater).order_by('-row_label', 'seat_number')

    seat_rows = {}
    booked_seats = [BookingSeat.seat for BookingSeat in BookingSeat.objects.filter(showtime=showtime)]
    for seat in seats:
        row = (seat.row_label,seat.seat_type)
        if row not in seat_rows:
            seat_rows[row] = []
        if seat not in booked_seats:
            seat_rows[row].append(seat)
        else:
            seat_rows[row].append(0)

    context = {
        'movie' : movie,
        'theater' : theater,
        'seats' : seats,
        'showtime' : showtime,
        'seat_rows' : seat_rows
    }    

    return render(request, 'bookings/seat_layout.html', context)


@login_required
def BookTicketView(request,show_id):
    if request.method == 'POST':
        selected_seats = json.loads(request.POST['selected_seats'])
        total_amount = eval(request.POST['total_amount'])
        tickets = []
        user = User.objects.get(username = request.user.username)
        showtime = Showtime.objects.get(id=show_id)
        convenience_fee = total_amount *0.1
        sub_total = total_amount + convenience_fee
        booking = Booking.objects.create(user=user,
                                        showtime=showtime,
                                        total_amount=sub_total)
        for seat in selected_seats:
            tickets.append(seat['key'])
            id = seat['id']
            seat_obj = Seat.objects.get(id=id)
            BookingSeat.objects.create(booking=booking, 
                                       seat=seat_obj,
                                       showtime=showtime
                                       )
        context={
            'tickets':tickets,
            'convenience_fee':convenience_fee,
            'sub_total':sub_total,
            'total_amount':total_amount,
            'showtime':showtime,
            'booking':booking,
            'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY
        }
        return render(request,'bookings/payment.html',context)
    return HttpResponse('Invalid Request')

# @login_required
# def your_order_view(request, booking_id):
#     booking = get_object_or_404(Booking, id=booking_id, user=request.user)
#     booking_seats = BookingSeat.objects.filter(booking=booking).select_related('seat')

#     context = {
#         'booking': booking,
#         'booking_seats': booking_seats
#     }
#     return render(request, 'bookings/your_order.html', context)


@login_required
def view_bookings(request):
    bookings = Booking.objects.filter(user=request.user).select_related(
        'showtime__movie',
        'showtime__theater',
    ).prefetch_related(
        'bookingseat_set__seat'
    ).order_by('-booking_time')

    movie_title = request.GET.get('movie')
    if movie_title:
        bookings = bookings.filter(showtime__movie__title__icontains=movie_title)

    return render(request, 'bookings/view_bookings.html', {'bookings': bookings})
