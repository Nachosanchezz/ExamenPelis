from django.urls import path
from . import views
from .views import (
    MovieListView,
    MovieDetailView,
    PlaylistView,
    RecommendationView,
    home,
    movies,
    movie_details,
    series,
    movie_search,
    search_by_name,
    view_playlist,
    add_to_playlist,
    
)

app_name = "streaming"

urlpatterns = [
    path("", home, name="home"),
    path("search/", movie_search, name="movie-search"),
    path("search_by_name/", search_by_name, name="search-by-name"),
    path("movies/", movies, name="movies"),
    path("series/", series, name="series"),
    path("api/movie/<int:movie_id>/", movie_details, name="movie-details"),
    path("api/movies/", MovieListView.as_view(), name="movie-list"),
    path("api/movies/<int:pk>/", MovieDetailView.as_view(), name="movie-detail"),
    path("api/playlists/", PlaylistView.as_view(), name="playlist"),
    path("api/recommendations/", RecommendationView.as_view(), name="recommendation"),
    path("series/<int:series_id>/", views.series_detail, name="series-detail"),
    path("advent-calendar/", views.advent_calendar, name="advent_calendar"),
    path("playlist/", view_playlist, name="playlist"),
    path("add-to-playlist/<int:movie_id>/", add_to_playlist, name="add-to-playlist"),


   
]


