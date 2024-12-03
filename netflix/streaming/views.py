from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Movie, Playlist, Recommendation
from .serializers import MovieSerializer, PlaylistSerializer, RecommendationSerializer
from django.http import JsonResponse
from .utils import fetch_popular_movies, fetch_movie_details, fetch_popular_series, search_movies, fetch_movies_from_tmdb, fetch_recommendations, fetch_top_rated_movies, fetch_upcoming_movies
from django.contrib.auth.views import LoginView

# Vista Home para plantillas
def home(request):
    """Vista principal que organiza los carruseles de películas y series."""
    try:
        # Películas populares
        top_rated_movies = fetch_movies_from_tmdb('movie/top_rated')['results']
        # Estrenos
        upcoming_movies = fetch_movies_from_tmdb('movie/upcoming')['results']
        # Series populares
        popular_series = fetch_movies_from_tmdb('tv/popular')['results']
        # Series mejor calificadas
        top_rated_series = fetch_movies_from_tmdb('tv/top_rated')['results']

        recommendations = fetch_recommendations(request.user.id) if request.user.is_authenticated else []

        context = {
            'top_rated_movies': top_rated_movies,
            'upcoming_movies': upcoming_movies,
            'popular_series': popular_series,
            'top_rated_series': top_rated_series,
            'recommended_movies': recommendations,
        }

        return render(request, 'streaming/home.html', context)

    except Exception as e:
        return render(request, 'streaming/home.html', {'error': str(e)})
    
def movie_search(request):
    """Vista para buscar películas."""
    genre_id = request.GET.get('genre', '')  # Obtén el ID del género
    query = request.GET.get('q', '')  # Término de búsqueda
    page = request.GET.get('page', 1)  # Página actual
    genre_name = ''  # Inicia vacío

    try:
        # Obtener todas las películas de un género
        if genre_id:
            genre_name = dict([(str(genre['id']), genre['name']) for genre in fetch_movies_from_tmdb('genre/movie/list')['genres']]).get(genre_id, '')
            data = fetch_movies_from_tmdb('discover/movie', {'with_genres': genre_id, 'page': int(page)})
        # Buscar películas por texto
        elif query:
            data = search_movies(query, page=int(page))
        else:
            data = {'results': []}  # No hay resultados si no hay géneros ni texto

        movies = data['results']
        return render(request, "streaming/search.html", {"movies": movies, "query": genre_name or query, "page": int(page)})
    except Exception as e:
        return render(request, "streaming/search.html", {'error': str(e), "query": genre_name or query})

   
    
def movie_details(request, movie_id):
    """Vista para obtener detalles de una película."""
    try:
        data = fetch_movie_details(movie_id)
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# Vistas para la API
class MovieListView(APIView):
    def get(self, request):
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

class MovieDetailView(APIView):
    def get(self, request, pk):
        try:
            movie = Movie.objects.get(pk=pk)
            serializer = MovieSerializer(movie)
            return Response(serializer.data)
        except Movie.DoesNotExist:
            return Response({"error": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)

class PlaylistView(APIView):
    def get(self, request):
        playlists = Playlist.objects.filter(user=request.user)
        serializer = PlaylistSerializer(playlists, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        playlist = Playlist.objects.create(name=data['name'], user=request.user)
        if 'movies' in data:
            for movie_id in data['movies']:
                movie = Movie.objects.get(id=movie_id)
                playlist.movies.add(movie)
        playlist.save()
        return Response(PlaylistSerializer(playlist).data, status=status.HTTP_201_CREATED)

class RecommendationView(APIView):
    def get(self, request):
        try:
            recommendation = Recommendation.objects.get(user=request.user)
            serializer = RecommendationSerializer(recommendation)
            return Response(serializer.data)
        except Recommendation.DoesNotExist:
            return Response({"message": "No recommendations found."}, status=status.HTTP_404_NOT_FOUND)



def popular_movies(request):
    """Vista para obtener películas populares."""
    try:
        data = fetch_popular_movies()
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)



def movies(request):
    """Vista para la página de películas."""
    try:
        # Obtener géneros
        genres_data = fetch_movies_from_tmdb('genre/movie/list')['genres']

        # Obtener películas de cada categoría
        top_rated_movies = fetch_top_rated_movies()['results']
        upcoming_movies = fetch_upcoming_movies()['results']

        # Buscar películas por género si se selecciona uno
        genre_id = request.GET.get('genre')
        genre_movies = []
        if genre_id:
            genre_movies = fetch_movies_from_tmdb('discover/movie', {'with_genres': genre_id})['results']

        context = {
            'top_rated_movies': top_rated_movies,
            'upcoming_movies': upcoming_movies,
            'genre_movies': genre_movies,
            'genres': genres_data,
        }

        return render(request, "streaming/movies.html", context)

    except Exception as e:
        return render(request, "streaming/movies.html", {'error': str(e)})
    

def series(request):
    """Muestra una lista de series populares en la plantilla `series.html`."""
    try:
        data = fetch_popular_series()  # Llama a la función que obtiene series populares
        series = data['results']  # La clave 'results' contiene las series
        return render(request, "streaming/series.html", {"series": series})
    except Exception as e:
        return render(request, "streaming/series.html", {"error": str(e)})

class CustomLoginView(LoginView):
    template_name = 'streaming/login.html'

class LogoutView(APIView):
    def get(self, request):
        logout(request)
        return redirect('streaming:home')



@login_required
def my_account(request):
    """Muestra la cuenta del usuario y sus recomendaciones."""
    try:
        # Obtiene las recomendaciones personalizadas para el usuario autenticado
        user_recommendations = fetch_recommendations(request.user.id)  # Basado en usuario
    except Exception as e:
        user_recommendations = []

    return render(request, 'streaming/my_account.html', {
        'recommended_movies': user_recommendations
    })


def register(request):
    """Registro de nuevos usuarios."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('streaming:login')
    else:
        form = UserCreationForm()
    return render(request, 'streaming/register.html', {'form': form})


