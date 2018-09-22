
import re
import time
import logging
from pathlib import Path
from django.core.management.base import BaseCommand
from django.conf import settings

from plugins.ml2lm.models import Playlist, Movie
from plugins.utils.nicovideo_fetcher import NicovideoFetcher
from plugins.utils.youtube_fetcher import YoutubeFetcher


logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def add_arguments(self, parser):
        pass

    def handle(self, *args: list, **options: dict):
        playlists = Playlist.objects.all()
        for playlist in playlists:
            updated = self._update_playlist(playlist)
            time.sleep(5)
            if updated is True:
                logger.info(f"updated {playlist.title}")

    def _update_playlist(self, playlist: Playlist) -> bool:
        latest_movie_url = playlist.latest_movie.url
        site = playlist.site
        if site == "nicovideo":
            playlist_id = playlist.playlist_id
            fetched_data = NicovideoFetcher.fetch_playlist_and_latest_movie(playlist_id)
        elif site == "youtube":
            playlist_id = playlist.playlist_id
            fetched_data = YoutubeFetcher.fetch_playlist_and_latest_movie(playlist_id)

        if latest_movie_url != fetched_data['latest_movie_url']:
            latest_movie = Movie.objects.create(
                url=fetched_data['latest_movie_url'],
                title=fetched_data['latest_movie_title'],
                playlist=playlist,
            )
            playlist.save()  # for updating updated_at of playlist
            return True

        return False
