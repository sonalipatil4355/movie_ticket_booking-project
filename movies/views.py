from django.shortcuts import render, get_object_or_404
from movies.models import Movie
from reviews.models import Review
from django.db.models import Avg, Count
from datetime import date
from datetime import datetime


def movie_list_view(request):
    movies = Movie.objects.all()
    return render(request, 'movies/movie_list.html', {'movies': movies})


def movie_detail_view(request, slug):
    movie = get_object_or_404(Movie, slug=slug)
    review_qs = Review.objects.filter(movie=movie).order_by('-created_at')

    no_users = review_qs.count()
    rating_data = review_qs.aggregate(avg_rating=Avg('rating'))
    avg_rating = round(rating_data['avg_rating'] or 0.0, 1)

    rating_counts = review_qs.values('rating').annotate(count=Count('rating')).order_by('-rating')

    context = {
        'movie': movie,
        'reviews': review_qs[:5],
        'rating': avg_rating,
        'no_users': no_users,
        'rating_counts': rating_counts,
        'today': datetime.today().date(),
    }
    return render(request, 'movies/movie_detail.html', context)

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from bookings.models import Booking

@login_required
def view_bookings(request):
    bookings = Booking.objects.filter(user=request.user).select_related(
        'showtime__movie',
        'showtime__theater',
    ).prefetch_related(
        'bookingseat_set__seat'
    ).order_by('-booking_time')

    return render(request, 'bookings/view_bookings.html', {'bookings': bookings})


# movies/views.py

from django.shortcuts import render, redirect
from .models import Movie
def SearchView(request):
    if request.method == "POST":
        search_query = request.POST.get('search_query', '')
        location = request.POST.get('location', '')

        movies = Movie.objects.all()

        if search_query:
            movies = movies.filter(title__icontains=search_query)

        if location:
            movies = movies.filter(theater__city__iexact=location)

        context = {
            'movies': movies,
            'search_term': search_query,
            'selected_location': location,
        }
        return render(request, 'movies/movie_list.html', context)

    return redirect('movie_list')



