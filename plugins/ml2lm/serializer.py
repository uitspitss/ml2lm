from uuid import uuid4
from rest_framework import serializers

from .models import Playlist, Movie


class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ('url', 'title', 'count')

    def create(self, validated_data):
        f = lambda: str(uuid4().hex)[:6]
        rand_str = f()
        while Playlist.objects.filter(short_id=rand_str).first() is not None:
            rand_str = f()
        playlist = Playlist.objects.create(short_id=rand_str, **validated_data)
        return playlist


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('url', 'title', 'count')
