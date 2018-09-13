import re
import logging
from uuid import uuid4
from rest_framework import serializers

from .models import Playlist, Movie
from plugins.utils.nicovideo_fetcher import NicovideoFetcher
from plugins.utils.youtube_fetcher import YoutubeFetcher

logger = logging.getLogger(__name__)


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('url', 'title', 'count')
        read_only_fields = ('url', 'title', 'count')


class PlaylistSerializer(serializers.ModelSerializer):
    # movies = MovieSerializer(many=True)
    thumbnail_url = serializers.SerializerMethodField()

    class Meta:
        model = Playlist
        fields = ('short_id', 'url', 'title', 'count', 'thumbnail_url')
        read_only_fields = ('short_id', 'title', 'count', 'thumbnail_url')

    def get_thumbnail_url(self, obj):
        return obj.thumbnail_url

    def create(self, validated_data):
        f = lambda: str(uuid4().hex)[:6]
        rand_str = f()
        while Playlist.objects.filter(short_id=rand_str).exists() is True:
            rand_str = f()

        url = validated_data['url']
        if re.search(r'^https?://www.nicovideo.jp/mylist/', url):
            playlist_id = re.search(r'(\d+?)\/*$', url)[1]
            fetched_data = NicovideoFetcher.fetch_playlist_and_latest_movie(playlist_id)
        elif re.search(r'^https?://www.youtube.com/.*list=', url):
            playlist_id = re.search(r'list=([^&]+)', url)[1]
            fetched_data = YoutubeFetcher.fetch_playlist_and_latest_movie(playlist_id)
        else:
            return {'error': "invalid playlist url"}

        logger.debug(fetched_data)

        try:
            playlist = Playlist.objects.create(
                short_id=rand_str,
                url=fetched_data['playlist_url'],
                title=fetched_data['playlist_title']
            )

            latest_movie = Movie.objects.create(
                playlist=playlist,
                url=fetched_data['latest_movie_url'],
                title=fetched_data['latest_movie_title']
            )
        except Exception as e:
            return {'error': "shorten process is wrong"}

        return playlist

    def validate_url(self, url):
        url = url.strip()
        logger.info(url)
        return url
