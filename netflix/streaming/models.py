from django.db import models
from django.contrib.auth.models import User

class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    release_date = models.DateField()
    poster_url = models.URLField()
    backdrop_url = models.URLField()
    tmdb_id = models.IntegerField(unique=True)

    def __str__(self):
        return self.title

from django.contrib.auth.models import User
from django.db import models

class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="playlists")
    movie_id = models.IntegerField()
    title = models.CharField(max_length=255)
    poster_path = models.CharField(max_length=255, blank=True, null=True)
    overview = models.TextField(blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)
    vote_average = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} ({self.user.username})"


class Recommendation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='recommendation')
    recommended_movies = models.ManyToManyField(Movie, related_name='recommendations')

    def __str__(self):
        return f"Recommendations for {self.user.username}"