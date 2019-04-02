import re
import logging
from threading import Thread
from django.conf import settings
from django.views import View
from django.shortcuts import get_object_or_404, redirect, Http404
from django.core.management import call_command
from rest_framework import viewsets

from .models import Playlist, Movie
from .serializer import PlaylistSerializer, MovieSerializer

logger = logging.getLogger(__name__)


def redirect_latest_movie(request, short_id: str) -> str:
    logger.debug(short_id)
    playlist = get_object_or_404(Playlist, short_id=short_id)
    latest_movie = playlist.latest_movie
    latest_movie.count += 1
    latest_movie.save()
    playlist.count += 1
    playlist.save()
    return redirect(latest_movie.url)


def update_playlists(request) -> str:
    def command():
        call_command('update_playlists')

    logger.debug(request.META)
    if settings.DEBUG is True or request.get_host().split(':')[0] == '0.1.0.1':
        th = Thread(target=command)
        th.start()
        return redirect('/')
    else:
        raise Http404(request.META)


class PlaylistViewSet(viewsets.ModelViewSet):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer

    def get_queryset(self) -> Playlist:
        qs = Playlist.objects.all()
        url = self.request.query_params.get('url')
        if url is not None:
            if re.search(r'^https?://www.nicovideo.jp/mylist/', url):
                mo = re.search(r'(\d+?)\/*$', url)
                if mo:
                    playlist_id = mo[1]
                    url = f"http://www.nicovideo.jp/mylist/{playlist_id}"
            elif re.search(r'^https?://www.youtube.com/.*list=', url):
                mo = re.search(r'list=([^&]+)', url)
                if mo:
                    logger.debug(mo)
                    playlist_id = mo[1]
                    url = f"https://www.youtube.com/playlist?list={playlist_id}"
            qs = qs.filter(url=url)
        else:
            qs = qs.order_by('-updated_at')[:15]
        return qs


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
