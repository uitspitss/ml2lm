import logging
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class NicovideoFetcher:

    @classmethod
    def fetch_playlist_and_latest_movie(cls, playlist_id: str) -> dict:
        d = {}
        try:
            # get playlist info
            url = f"http://www.nicovideo.jp/mylist/{playlist_id}?rss=2.0&numbers=1&sort=1"
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'xml')
            channel_item = soup.find('channel')
            d['playlist_title'] = channel_item.title.text
            d['playlist_url'] = channel_item.link.text

            # get latest movie info of playlist
            latest_item = soup.find('item')
            d['latest_movie_title'] = latest_item.title.text
            d['latest_movie_url'] = latest_item.link.text
        except Exception as e:
            logger.debug(e)
            logger.debug(f"playlist_id:{playlist_id}")
        finally:
            logger.debug(d)
            return d

