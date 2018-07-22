from django.views import View
from rest_framework import viewsets, filters

from .models import Playlist, Movie
from .serializer import PlaylistSerializer, MovieSerializer


class PlaylistViewSet(viewsets.ModelViewSet):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
