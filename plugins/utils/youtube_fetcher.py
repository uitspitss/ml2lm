import json
import logging
import requests
from django.conf import settings

logger = logging.getLogger(__name__)


class YoutubeFetcher:
    apikey = settings.YOUTUBE_API_KEY

    @classmethod
    def fetch_playlist(cls, playlist_id: str) -> dict:
        d = {}
        try:
            # get playlist info
            url = "https://www.googleapis.com/youtube/v3/playlists"
            p = {
                'part': 'snippet',
                'id': playlist_id,
                'key': cls.apikey
            }
            r = requests.get(url, params=p)
            playlist = json.loads(r.text)['items'][0]['snippet']
            d['playlist_title'] = playlist['title']
            d['playlist_url'] = f"https://www.youtube.com/playlist?list={playlist_id}"
        except Exception as e:
            logger.debug(e)
            logger.debug(f"playlist_id:{playlist_id}")
        finally:
            logger.debug(d)
            return d

    @classmethod
    def fetch_latest_movie(cls, playlist_id: str) -> dict:
        d = {}
        try:
            # get latest movie info of playlist
            url = "https://www.googleapis.com/youtube/v3/playlistItems"
            p = {
                'part': "snippet",
                'playlistId': playlist_id,
                'key': cls.apikey
            }
            r = requests.get(url, params=p)
            latest_movie = json.loads(r.text)['items'][0]['snippet']
            d['latest_movie_title'] = latest_movie['title']
            video_id = latest_movie['resourceId']['videoId']
            d['latest_movie_url'] = f"https://www.youtube.com/watch?v={video_id}&list={playlist_id}"
        except Exception as e:
            logger.debug(e)
            logger.debug(f"playlist_id:{playlist_id}")
        finally:
            logger.debug(d)
            return d

    @classmethod
    def fetch_playlist_and_latest_movie(cls, playlist_id: str) -> dict:
        d = {}
        d.update(cls.fetch_playlist(playlist_id))
        d.update(cls.fetch_latest_movie(playlist_id))
        return d
