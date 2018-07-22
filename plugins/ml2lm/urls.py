from django.urls import path, include
from rest_framework import routers

from .views import PlaylistViewSet, MovieViewSet


router = routers.SimpleRouter()
router.register(r'playlist', PlaylistViewSet)
router.register(r'movie', MovieViewSet)

urlpatterns = [
    path('api/',
         include((router.urls, 'api'))),
]
