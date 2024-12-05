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
]
