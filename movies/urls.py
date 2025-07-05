from django.urls import path
from . import views

urlpatterns = [
    path('', views.movie_list_view, name='movie_list'),
    path('movie/<str:slug>/', views.movie_detail_view, name='movie_detail'),
    
    path('my-bookings/', views.view_bookings, name='view_bookings'),
    path('search/', views.SearchView, name='search_view'),

]
