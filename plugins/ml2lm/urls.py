from django.urls import path, include
from rest_framework import routers

from . import views


router = routers.SimpleRouter()
router.register(r'playlist', views.PlaylistViewSet)
router.register(r'movie', views.MovieViewSet)

urlpatterns = [
    path('<slug:short_id>', views.redirect_latest_movie, name='redirect_latest_movie'),
    path('api/', include((router.urls, 'api'))),
]
