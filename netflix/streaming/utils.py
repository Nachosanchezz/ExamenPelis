import requests
from django.conf import settings

def fetch_movies_from_tmdb(endpoint, params=None):
    """Función genérica para interactuar con la API de TMDb."""
    if not params:
        params = {}
    url = f'https://api.themoviedb.org/3/{endpoint}'
    params['api_key'] = settings.TMDB_API_KEY
    params['language'] = 'es-ES'

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        # Comprobamos si la respuesta incluye 'results' y cada objeto contiene 'overview'
        if "results" in data:
            for item in data["results"]:
                item["overview"] = item.get("overview", "Descripción no disponible.")
        return data
    else:
        raise Exception(f"Error en la API de TMDb: {response.status_code} - {response.text}")

# Funciones específicas que estás usando en tu proyecto:
def fetch_popular_movies(page=1):
    """Obtiene las películas populares desde TMDb."""
    return fetch_movies_from_tmdb('movie/popular', {'page': page})

def fetch_movie_details(movie_id):
    """Obtiene los detalles de una película por su ID."""
    return fetch_movies_from_tmdb(f'movie/{movie_id}')

def fetch_popular_series(page=1):
    """Obtiene las series populares desde TMDb."""
    return fetch_movies_from_tmdb('tv/popular', {'page': page})

def fetch_top_rated_series(page=1):
    """Obtiene las series mejor calificadas desde TMDb."""
    return fetch_movies_from_tmdb('tv/top_rated', {'page': page})

def fetch_upcoming_movies(page=1):
    """Obtiene las películas próximas a estrenarse."""
    return fetch_movies_from_tmdb('movie/upcoming', {'page': page})

# Opcional: Mantener búsqueda si tienes una funcionalidad de búsqueda
def search_movies(query, page=1):
    """Busca películas por título."""
    return fetch_movies_from_tmdb('search/movie', {'query': query, 'page': page})

def fetch_top_rated_movies(page=1):
    """Obtiene las películas mejor calificadas."""
    return fetch_movies_from_tmdb('movie/top_rated', {'page': page})

def fetch_recommendations(user_id):
        """Obtiene recomendaciones genéricas (por ejemplo, películas populares)."""
        try:
            # Usar películas populares como recomendaciones
            return fetch_movies_from_tmdb('movie/popular')['results']
        except Exception as e:
            print(f"Error al obtener recomendaciones: {str(e)}")
        return []
    
def fetch_genres():
    """Obtiene la lista de géneros desde TMDb."""
    return fetch_movies_from_tmdb('genre/movie/list')['genres']



def fetch_series_genres():
    """Obtiene la lista de géneros de series desde TMDb."""
    return fetch_movies_from_tmdb("genre/tv/list")["genres"]

def search_series_by_genre(genre_id, page=1):
    """Busca series por género utilizando la API de TMDb."""
    return fetch_movies_from_tmdb("discover/tv", {"with_genres": genre_id, "page": page})

def fetch_series_details(series_id):
    """Obtiene los detalles de una serie por su ID."""
    return fetch_movies_from_tmdb(f"tv/{series_id}")




