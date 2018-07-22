from django.core.management.base import BaseCommand
from django.conf import settings

import re
import requests
from pathlib import Path
from sys import platform
from kawasemi.django import send
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

from plugins.ml2lm.models import Playlist, Movie


from logging import getLogger
logger = getLogger(__name__)

LOGIN_EMAIL = settings.NICO_EMAIL
LOGIN_PASS = settings.NICO_PASSWD

NICO_MYLIST_BASE = 'http://www.nicovideo.jp/mylist/'


class Command(BaseCommand):
    help = 'ml2lm commands'

    def add_arguments(self, parser):
        parser.add_argument(
            '-c',
            '--create',
            action='store',
            nargs='+',
            type=str,
            help='require mylist url or id'
        )
        parser.add_argument(
            '--update',
            action='store_true',
        )

    def handle(self, *args, **options):
        if options['create'] and len(options['create']) == 1:
            mylist_url = options['create'][0]
            mylist_id = re.search(r'(\d+)', mylist_url)[0]

            playlist = Playlist.objects.filter(
                url=mylist_url
            )

            if not playlist:
                self.driver = self.set_driver()
                self.login_nico()
                params = self.get_mylist_info(mylist_id)
                self.driver.close()

                self.save_playlist(params)

        if options['update']:
            self.driver = self.set_driver()
            self.login_nico()

            pls = Playlist.objects.all()
            for pl in pls:
                mylist_id = re.search(r'(\d+)', pl.url)[0]
                params = self.get_mylist_info(mylist_id)
                if params:
                    self.update_playlist(pl, params)
                else:
                    logger.error(f'can\'t update {pl.url}')

            self.driver.close()
            logger.info(f'updated {pls.count()} playlists')

    def update_playlist(self, pl: object, params: dict):
        latest_movie_url = pl.movies.order_by('-created_at')[0].url
        if latest_movie_url != params['latest_movie_url']:
            latest_movie = Movie(
                url=params['latest_movie_url'],
                title=params['latest_movie_title'],
                playlist=pl,
            )
            latest_movie.save()
            logger.info(f'updated latest movie of {pl.url}')
            send(f'updated latest movie of {pl.url}')

    def save_playlist(self, params: dict):
        playlist = Playlist(
            url=params['playlist_url'],
            title=params['playlist_title'],
        )
        playlist.save()

        latest_movie = Movie(
            url=params['latest_movie_url'],
            title=params['latest_movie_title'],
            playlist=playlist,
        )
        latest_movie.save()

        logger.info(
            f'saved {latest_movie.url} into {playlist.url}')

        return playlist

    def get_mylist_info(self, mylist_id: str):
        if not self.driver:
            raise 'Driver Not Found'

        playlist_url = NICO_MYLIST_BASE + mylist_id
        sort_param = '#+sort=1'

        self.driver.get(playlist_url + sort_param)

        try:
            playlist_title = self.driver.title

            latest_movie_url = self.driver.find_element_by_xpath(

                '//table/tbody/tr/td[2]/p[2]/a').get_attribute('href')
            latest_movie_title = self.driver.find_element_by_xpath(
                '//table/tbody/tr/td[2]/p[2]/a').text.strip()

            return {
                'playlist_url': playlist_url,
                'playlist_title': playlist_title,
                'latest_movie_url': latest_movie_url,
                'latest_movie_title': latest_movie_title,
            }
        except Exception as e:
            logger.error('incorrect mylist')
            logger.error(e)
            return False

    def set_driver(self):
        driver = webdriver.PhantomJS(
            executable_path=Path(
                settings.BASE_DIR, 'bin',
                'mac' if platform == 'darwin'
                else 'linux',
                'phantomjs'
            ),
            service_args=[
                "--ignore-ssl-errors=true",
                "--ssl-protocol=any",
                "--disk-cache=false",
                "--load-images=false",
            ]
        )
        driver.set_page_load_timeout(30)
        return driver

    def login_nico(self):
        self.driver.get('https://account.nicovideo.jp/login?site=niconico')

        mail_tel = self.driver.find_element_by_xpath(
            '//*[@id="input__mailtel"]')
        mail_tel.send_keys(LOGIN_EMAIL)

        password = self.driver.find_element_by_xpath(
            '//*[@id="input__password"]')
        password.send_keys(LOGIN_PASS)

        login_button = self.driver.find_element_by_xpath(
            '//*[@id="login__submit"]')
        login_button.click()

        return True
