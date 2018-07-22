from rest_framework import serializers

from .models import Playlist, Movie


class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ('url', 'title', 'total_count')


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('url', 'title', 'count')
