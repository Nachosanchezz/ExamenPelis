from django.urls import path
from . import views
from .views import MovieListView, MovieDetailView, PlaylistView, RecommendationView, home, movies, my_account, popular_movies, movie_details, series, movie_search, CustomLoginView, LogoutView


app_name = 'streaming'


urlpatterns = [
    path('', home, name='home'),
    path('search/', movie_search, name='movie-search'),
    path('movies/', movies, name='movies'), 
    path('series/', series, name='series'),
    path('my_account/', my_account, name='my_account'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('api/popular/', popular_movies, name='popular-movies'),
    path('api/movie/<int:movie_id>/', movie_details, name='movie-details'),
    path('api/movies/', MovieListView.as_view(), name='movie-list'),
    path('api/movies/<int:pk>/', MovieDetailView.as_view(), name='movie-detail'),
    path('api/playlists/', PlaylistView.as_view(), name='playlist'),
    path('api/recommendations/', RecommendationView.as_view(), name='recommendation'),
    
]