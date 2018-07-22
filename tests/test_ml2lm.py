import random
import pytest
from pprint import pprint
from hamcrest import *
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.urlresolvers import reverse

from plugins.ml2lm.models import Playlist, Movie


@pytest.mark.django_db
class TestAcceptance:

    @pytest.mark.parametrize('url, status_code', [
        ('/', 200),
    ])
    def test_views(self, client, url, status_code):
        c = client.get(url)
        assert c.status_code == status_code

    def test_shorten(self, client):
        response = client.post(
            reverse('regist'),
            {
                'url': 'http://www.nicovideo.jp/mylist/49117000',
            },
            follow=True
        )

        assert response.context['playlist_form'] != ''
        assert response.context['playlist'] != None

        playlist = Playlist.objects.all()

        assert playlist.count() == 1

        pl = playlist[0]

        assert pl.url == 'http://www.nicovideo.jp/mylist/49117000'
        assert pl.total_count == 0
        assert pl.movies.count() == 1
        assert pl.movies.all()[0].count == 0
