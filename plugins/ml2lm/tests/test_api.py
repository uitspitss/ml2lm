import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestApi:
    @pytest.mark.parametrize(
        'url, status_code',
        [('/api/playlist/', 200), ('/api/movie/', 200), ('/api/', 404)],
    )
    def test_acceptance(self, url, status_code):
        r = APIClient().get(url)
        assert r.status_code == status_code

    def test_shoten_nicovideo(self, mocker):
        mocker.patch(
            'plugins.utils.nicovideo_fetcher.NicovideoFetcher.fetch_playlist_and_latest_movie',
            return_value={
                'playlist_title': "マイリスト Monty Python&#039;s Flying Circus‐ニコニコ動画",
                'playlist_url': "http://www.nicovideo.jp/mylist/58182633",
                'latest_movie_title': "まさかの時に『空飛ぶモンティ・パイソン』 【第40話】",
                'latest_movie_url': "http://www.nicovideo.jp/watch/sm30319165",
            },
        )

        r = APIClient().post(
            '/api/playlist/',
            {'url': "http://www.nicovideo.jp/mylist/58182633"},
            format='json',
        )
        assert r.status_code == 201

    def test_shoten_youtube(self, mocker):
        mocker.patch(
            'plugins.utils.youtube_fetcher.YoutubeFetcher.fetch_playlist_and_latest_movie',
            return_value={
                'playlist_title': "Top Tracks - Japan",
                'playlist_url': "https://www.youtube.com/playlist?list=PLFgquLnL59alxIWnf4ivu5bjPeHSlsUe9",
                'latest_movie_title': "星野源 - アイデア【Music Video】",
                'latest_movie_url': "https://www.youtube.com/watch?v=RlUb2F-zLxw&list=PLFgquLnL59alxIWnf4ivu5bjPeHSlsUe9",
            },
        )

        r = APIClient().post(
            '/api/playlist/',
            {
                'url': "https://www.youtube.com/playlist?list=PLFgquLnL59alxIWnf4ivu5bjPeHSlsUe9"
            },
            format='json',
        )
        assert r.status_code == 201
