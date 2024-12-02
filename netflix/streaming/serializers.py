from rest_framework import serializers
from .models import Movie, Playlist, Recommendation

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

class PlaylistSerializer(serializers.ModelSerializer):
    movies = MovieSerializer(many=True, read_only=True)

    class Meta:
        model = Playlist
        fields = ['id', 'name', 'user', 'movies', 'created_at']

class RecommendationSerializer(serializers.ModelSerializer):
    recommended_movies = MovieSerializer(many=True, read_only=True)

    class Meta:
        model = Recommendation
        fields = ['id', 'user', 'recommended_movies']