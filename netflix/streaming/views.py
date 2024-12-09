from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Movie, Playlist, Recommendation
from .serializers import MovieSerializer, PlaylistSerializer, RecommendationSerializer
from django.http import JsonResponse
from .utils import (
    fetch_popular_movies,
    fetch_movie_details,
    fetch_popular_series,
    search_movies,
    fetch_movies_from_tmdb,
    fetch_recommendations,
    fetch_top_rated_movies,
    fetch_upcoming_movies,
    fetch_series_details,
)
from django.contrib.auth.decorators import login_required


def home(request):
    """Vista principal que organiza los carruseles de películas y series y el buscador."""
    try:
        top_rated_movies = fetch_movies_from_tmdb("movie/top_rated")["results"]
        upcoming_movies = fetch_movies_from_tmdb("movie/upcoming")["results"]
        popular_series = fetch_movies_from_tmdb("tv/popular")["results"]
        top_rated_series = fetch_movies_from_tmdb("tv/top_rated")["results"]

        recommendations = (
            fetch_recommendations(request.user.id)
            if request.user.is_authenticated
            else []
        )

        # Manejar búsqueda por nombre
        query = request.GET.get("q", "")
        search_results = []
        if query:
            # Buscar en películas y series
            movie_results = search_movies(query)["results"]
            series_results = fetch_movies_from_tmdb("search/tv", {"query": query})["results"]
            search_results = movie_results + series_results

        context = {
            "top_rated_movies": top_rated_movies,
            "upcoming_movies": upcoming_movies,
            "popular_series": popular_series,
            "top_rated_series": top_rated_series,
            "recommended_movies": recommendations,
            "search_results": search_results,
            "query": query,
        }

        return render(request, "streaming/home.html", context)

    except Exception as e:
        return render(request, "streaming/home.html", {"error": str(e)})


def search_by_name(request):
    """Vista para buscar películas o series por nombre."""
    query = request.GET.get("q", "").strip()
    page = request.GET.get("page", 1)

    try:
        movies = []
        series = []

        if query:
            # Buscar películas
            movie_data = search_movies(query, page=int(page))
            movies = movie_data.get("results", [])

            # Buscar series
            series_data = fetch_movies_from_tmdb("search/tv", {"query": query, "page": page})
            series = series_data.get("results", [])

        return render(
            request,
            "streaming/search_by_name.html",
            {
                "movies": movies,
                "series": series,
                "query": query,
                "page": int(page),
            },
        )
    except Exception as e:
        return render(
            request,
            "streaming/search_by_name.html",
            {
                "error": str(e),
                "movies": [],
                "series": [],
                "query": query,
            },
        )



def movie_search(request):
    """Vista para buscar películas."""
    genre_id = request.GET.get("genre", "")
    query = request.GET.get("q", "")
    page = request.GET.get("page", 1)
    genre_name = ""

    try:
        if genre_id:
            genre_name = dict(
                [
                    (str(genre["id"]), genre["name"])
                    for genre in fetch_movies_from_tmdb("genre/movie/list")["genres"]
                ]
            ).get(genre_id, "")
            data = fetch_movies_from_tmdb(
                "discover/movie", {"with_genres": genre_id, "page": int(page)}
            )
        elif query:
            data = search_movies(query, page=int(page))
        else:
            data = {"results": []}

        movies = data["results"]
        return render(
            request,
            "streaming/search.html",
            {"movies": movies, "query": genre_name or query, "page": int(page)},
        )
    except Exception as e:
        return render(
            request,
            "streaming/search.html",
            {"error": str(e), "query": genre_name or query},
        )



def movie_details(request, movie_id):
    """Vista para mostrar los detalles de una película."""
    try:
        movie = fetch_movie_details(movie_id)
        return render(request, "streaming/movie_details.html", {"movie": movie})
    except Exception as e:
        return render(request, "streaming/movie_details.html", {"error": str(e)})



def movies(request):
    """Vista para la página de películas."""
    try:
        genres_data = fetch_movies_from_tmdb("genre/movie/list")["genres"]
        top_rated_movies = fetch_top_rated_movies()["results"]
        upcoming_movies = fetch_upcoming_movies()["results"]

        genre_id = request.GET.get("genre")
        genre_movies = []
        if genre_id:
            genre_movies = fetch_movies_from_tmdb(
                "discover/movie", {"with_genres": genre_id}
            )["results"]

        context = {
            "top_rated_movies": top_rated_movies,
            "upcoming_movies": upcoming_movies,
            "genre_movies": genre_movies,
            "genres": genres_data,
        }

        return render(request, "streaming/movies.html", context)

    except Exception as e:
        return render(request, "streaming/movies.html", {"error": str(e)})


def series(request):
    """Muestra series populares o series filtradas por género."""
    try:
        genres_data = fetch_movies_from_tmdb("genre/tv/list")["genres"]  # Géneros de series
        genre_id = request.GET.get("genre")  # ID del género seleccionado

        if genre_id:
            # Series filtradas por género
            genre_series = fetch_movies_from_tmdb(
                "discover/tv", {"with_genres": genre_id}
            )["results"]
            return render(
                request,
                "streaming/series.html",
                {"genres": genres_data, "genre_series": genre_series},
            )
        else:
            # Series populares si no hay género seleccionado
            popular_series = fetch_popular_series()["results"]
            return render(
                request,
                "streaming/series.html",
                {"genres": genres_data, "popular_series": popular_series},
            )

    except Exception as e:
        return render(request, "streaming/series.html", {"error": str(e)})
    
def series_detail(request, series_id):
    try:
        series = fetch_series_details(series_id)
        return render(request, "streaming/series_detail.html", {"series": series})
    except Exception as e:
        return render(request, "streaming/series_detail.html", {"error": str(e)})



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
        """Obtener la Playlist del usuario actual en formato JSON."""
        playlists = Playlist.objects.filter(user=request.user)
        serializer = PlaylistSerializer(playlists, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Agregar una nueva película a la Playlist del usuario."""
        data = request.data
        playlist = Playlist.objects.create(
            user=request.user,
            movie_id=data["movie_id"],
            title=data["title"],
            poster_path=data.get("poster_path"),
            overview=data.get("overview"),
            release_date=data.get("release_date"),
            vote_average=data.get("vote_average"),
        )
        return Response(PlaylistSerializer(playlist).data, status=status.HTTP_201_CREATED)

class RecommendationView(APIView):
    def get(self, request):
        try:
            recommendation = Recommendation.objects.get(user=request.user)
            serializer = RecommendationSerializer(recommendation)
            return Response(serializer.data)
        except Recommendation.DoesNotExist:
            return Response({"message": "No recommendations found."}, status=status.HTTP_404_NOT_FOUND)


from random import choice
def advent_calendar(request):
    """Vista para mostrar una película diaria basada en el calendario de adviento."""
    import datetime  # Asegúrate de importar datetime
    try:
        # Obtén la fecha actual
        today = datetime.date.today()

        # Llama a la API para obtener una lista de películas populares
        api_response = fetch_movies_from_tmdb("movie/popular")
        all_movies = api_response.get("results", [])

        # Verifica si hay películas disponibles
        if all_movies:
            recommended_movie = all_movies[today.day % len(all_movies)]
        else:
            recommended_movie = None

        return render(request, "streaming/advent_calendar.html", {
            "today": today,
            "movie": recommended_movie,
        })

    except Exception as e:
        # Maneja cualquier excepción y muestra el error en el template
        return render(request, "streaming/advent_calendar.html", {
            "error": f"Error al obtener la película: {str(e)}"
        })



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def view_playlist(request):
    """Mostrar la Playlist del usuario actual."""
    playlist = Playlist.objects.filter(user=request.user)
    return render(request, "streaming/playlist.html", {"playlist": playlist})

from datetime import datetime

@login_required
def add_to_playlist(request, movie_id):
    """Agregar una película o serie a la Playlist usando un formulario."""
    if request.method == "POST":
        try:
            release_date = request.POST.get("release_date")
            
            # Intenta formatear la fecha, si es válida
            if release_date:
                try:
                    release_date = datetime.strptime(release_date, "%Y-%m-%d").date()
                except ValueError:
                    release_date = None  # Si no tiene un formato válido
            else:
                release_date = None  # Si está vacío

            movie_data = {
                "movie_id": movie_id,
                "title": request.POST.get("title"),
                "poster_path": request.POST.get("poster_path"),
                "overview": request.POST.get("overview"),
                "release_date": release_date,
                "vote_average": float(request.POST.get("vote_average").replace(",", ".")) if request.POST.get("vote_average") else None,
            }

            if not Playlist.objects.filter(user=request.user, movie_id=movie_id).exists():
                Playlist.objects.create(user=request.user, **movie_data)
            return redirect("streaming:playlist")

        except ValueError as e:
            return render(request, "streaming/error.html", {"error": str(e)})
        

@login_required
def remove_from_playlist(request, movie_id):
    """Eliminar una película de la playlist del usuario."""
    if request.method == "POST":
        try:
            # Buscar la película en la playlist del usuario
            movie = get_object_or_404(Playlist, user=request.user, movie_id=movie_id)
            movie.delete()  # Eliminar la película
        except Exception as e:
            # Puedes mostrar un mensaje de error en la plantilla si lo deseas
            print(f"Error al eliminar la película: {e}")
        return redirect("streaming:playlist")  # Redirigir de vuelta a la playlist
    return redirect("streaming:playlist")  # Si no es POST, redirigir igualmente
