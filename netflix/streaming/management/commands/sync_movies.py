from django.core.management.base import BaseCommand
from streaming.utils import fetch_popular_movies
from streaming.models import Movie

class Command(BaseCommand):
    help = "Sincroniza películas populares desde la API de TMDb"

    def handle(self, *args, **kwargs):
        data = fetch_popular_movies()
        for movie_data in data['results']:
            Movie.objects.update_or_create(
                tmdb_id=movie_data['id'],
                defaults={
                    'title': movie_data['title'],
                    'description': movie_data['overview'],
                    'release_date': movie_data.get('release_date'),
                    'poster_url': f"https://image.tmdb.org/t/p/w500{movie_data['poster_path']}",
                    'backdrop_url': f"https://image.tmdb.org/t/p/w500{movie_data['backdrop_path']}",
                }
            )
        self.stdout.write(self.style.SUCCESS("Películas sincronizadas exitosamente."))
