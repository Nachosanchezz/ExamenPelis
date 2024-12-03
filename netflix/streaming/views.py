from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Movie, Playlist, Recommendation
from .serializers import MovieSerializer, PlaylistSerializer, RecommendationSerializer
from django.http import JsonResponse
from .utils import fetch_popular_movies, fetch_movie_details, fetch_popular_series, search_movies, fetch_movies_from_tmdb

# Vista Home para plantillas
def home(request):
    """Vista principal que organiza los carruseles de películas y series."""
    try:
        # Películas populares
        top_rated_movies = fetch_movies_from_tmdb('movie/top_rated')['results'][:20]
        # Estrenos
        upcoming_movies = fetch_movies_from_tmdb('movie/upcoming')['results'][:20]
        # Series populares
        popular_series = fetch_movies_from_tmdb('tv/popular')['results'][:20]
        # Series mejor calificadas
        top_rated_series = fetch_movies_from_tmdb('tv/top_rated')['results'][:20]

        context = {
            'top_rated_movies': top_rated_movies,
            'upcoming_movies': upcoming_movies,
            'popular_series': popular_series,
            'top_rated_series': top_rated_series,
        }

        return render(request, 'streaming/home.html', context)

    except Exception as e:
        return render(request, 'streaming/home.html', {'error': str(e)})
    
def movie_search(request):
    """Vista para buscar películas."""
    query = request.GET.get('q', '')  # Término de búsqueda
    page = request.GET.get('page', 1)  # Página actual
    try:
        data = search_movies(query, page=int(page))
        movies = data['results']
        return render(request, "streaming/search.html", {"movies": movies, "query": query, "page": int(page)})
    except Exception as e:
        return render(request, "streaming/search.html", {'error': str(e), "query": query})

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
    """Muestra una lista de películas populares en la plantilla `movies.html`."""
    try:
        data = fetch_popular_movies()  # Llama a la función que obtiene películas populares
        movies = data['results']  # La clave 'results' contiene las películas
        return render(request, "streaming/movies.html", {"movies": movies})
    except Exception as e:
        return render(request, "streaming/movies.html", {"error": str(e)})


def movie_details(request, movie_id):
    """Vista para obtener detalles de una película."""
    try:
        data = fetch_movie_details(movie_id)
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    

def series(request):
    """Muestra una lista de series populares en la plantilla `series.html`."""
    try:
        data = fetch_popular_series()  # Llama a la función que obtiene series populares
        series = data['results']  # La clave 'results' contiene las series
        return render(request, "streaming/series.html", {"series": series})
    except Exception as e:
        return render(request, "streaming/series.html", {"error": str(e)})
